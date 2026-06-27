"""
NowcastManager — Central Orchestrator.

Receives each ``EnrichedObservation`` from the observation pipeline, feeds
fluxes to the independent SoLEXS and HEL1OS detectors, performs event
association when events complete, creates Master Catalog entries, and
maintains event tracking and timeline.

Exposes the complete ``NowcastState`` snapshot for WebSocket streaming.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from backend.nowcasting.config import nowcast_config
from backend.nowcasting.models import (
    NowcastState,
    DetectorState,
    FlarePhase,
    MasterFlareEntry,
    SolexsEvent,
    HeliosEvent,
    EventAssociation,
    EventAssociation,
    AssociationStatus,
    DetectorHealthSnapshot,
)
from backend.nowcasting.detectors.solexs_detector import SolexsDetector
from backend.nowcasting.detectors.helios_detector import HeliosDetector
from backend.nowcasting.detectors.benchmark import DetectorBenchmark
from backend.nowcasting.association.event_associator import EventAssociator
from backend.nowcasting.catalog.master_catalog import MasterCatalog
from backend.nowcasting.tracking.event_tracker import EventTracker
from backend.nowcasting.timeline.event_timeline import EventTimeline
from backend.nowcasting.repository.nowcast_repository import NowcastRepository
from backend.nowcasting.simulation.flare_simulator import FlareSimulator
from backend.physics.manager import physics_manager


class NowcastManager:
    """Central orchestrator for the Scientific Nowcasting Engine."""

    def __init__(self):
        self.solexs_detector = SolexsDetector(nowcast_config.solexs)
        self.helios_detector = HeliosDetector(nowcast_config.helios)
        self.associator = EventAssociator(nowcast_config.association)
        self.catalog = MasterCatalog()
        self.tracker = EventTracker()
        self.timeline = EventTimeline()
        self.repository = NowcastRepository()
        self.simulator = FlareSimulator(nowcast_config.simulation)

        # Benchmarks
        self.solexs_benchmark = DetectorBenchmark("SoLEXS")
        self.helios_benchmark = DetectorBenchmark("HEL1OS")

        # History Buffers (for physics characterization)
        self._solexs_history = []
        self._helios_history = []
        self.max_history_samples = 300

        # Pending events awaiting association
        self._pending_solexs: List[SolexsEvent] = []
        self._pending_helios: List[HeliosEvent] = []

        # Latest state for streaming
        self._latest_association: Optional[EventAssociation] = None
        self._active_flare: Optional[MasterFlareEntry] = None

        # In-progress events (the ones currently being built by detectors)
        self._in_progress_solexs: Optional[SolexsEvent] = None
        self._in_progress_helios: Optional[HeliosEvent] = None

        # Counters
        self.total_solexs_events = 0
        self.total_helios_events = 0
        self.total_associations = 0
        
        # Latest Physics State
        self._latest_physics = None
        self._latest_features = None

    def process_observation(self, solexs_flux: float, helios_flux: float, timestamp: str, obs_quality: float = 1.0) -> NowcastState:
        """Process a single validated observation tick.

        This is called once per second by the WebSocket broadcast loop.
        The flare simulator generates realistic flux profiles that replace
        the raw random telemetry values.
        """
        # Generate simulated flare-modulated fluxes
        sim_sol, sim_hel = self.simulator.generate()

        # Use simulated values (which include quiet-sun + flare profiles)
        # Use simulated values (which include quiet-sun + flare profiles)
        sol_flux = sim_sol
        hel_flux = sim_hel
        
        # Feed history buffers
        self._solexs_history.append(sol_flux)
        self._helios_history.append(hel_flux)
        if len(self._solexs_history) > self.max_history_samples:
            self._solexs_history.pop(0)
        if len(self._helios_history) > self.max_history_samples:
            self._helios_history.pop(0)

        # Feed to detectors
        import time
        t0 = time.time()
        sol_event = self.solexs_detector.ingest(sol_flux, timestamp, obs_quality)
        self.solexs_benchmark.record_tick((time.time() - t0) * 1000.0)
        
        t0 = time.time()
        hel_event = self.helios_detector.ingest(hel_flux, timestamp, obs_quality)
        self.helios_benchmark.record_tick((time.time() - t0) * 1000.0)

        # Track in-progress events from detector states
        sol_state = self.solexs_detector._state
        hel_state = self.helios_detector._state

        if sol_state not in (DetectorState.IDLE, DetectorState.ENDED):
            self._in_progress_solexs = SolexsEvent(
                start_time=self.solexs_detector._start_time,
                peak_time=self.solexs_detector._peak_time,
                peak_flux=self.solexs_detector._peak_flux,
                background_flux=self.solexs_detector._background,
                detector_state=sol_state,
                detection_confidence=self.solexs_detector.snapshot().confidence,
            )
        else:
            self._in_progress_solexs = None

        if hel_state not in (DetectorState.IDLE, DetectorState.ENDED):
            self._in_progress_helios = HeliosEvent(
                start_time=self.helios_detector._start_time,
                peak_time=self.helios_detector._peak_time,
                peak_energy=self.helios_detector._peak_flux,
                peak_counts=self.helios_detector._total_energy,
                burst_duration_s=float(self.helios_detector._burst_ticks),
                detector_state=hel_state,
                detection_confidence=self.helios_detector.snapshot().confidence,
            )
        else:
            self._in_progress_helios = None

        # Handle completed events
        if sol_event:
            self.total_solexs_events += 1
            self._pending_solexs.append(sol_event)
            self._try_associate()
            # Record benchmark
            dur = 0.0
            if sol_event.start_time and sol_event.end_time:
                from datetime import datetime as dt
                try:
                    s = dt.fromisoformat(sol_event.start_time.replace("Z", "+00:00"))
                    e = dt.fromisoformat(sol_event.end_time.replace("Z", "+00:00"))
                    dur = (e - s).total_seconds()
                except:
                    pass
            self.solexs_benchmark.record_event(dur, sol_event.detection_confidence)

        if hel_event:
            self.total_helios_events += 1
            self._pending_helios.append(hel_event)
            self._try_associate()
            self.helios_benchmark.record_event(hel_event.burst_duration_s, hel_event.detection_confidence)

        return self.get_state()

    def _try_associate(self) -> None:
        """Attempt to associate pending SoLEXS and HEL1OS events."""

        if not self._pending_solexs or not self._pending_helios:
            # If only one detector fired, still create a catalog entry
            # from the single-instrument detection
            if self._pending_solexs:
                sol = self._pending_solexs.pop(0)
                entry = self.catalog.create_entry(solexs_event=sol)
                self._finalise_catalog_entry(entry)
            elif self._pending_helios:
                hel = self._pending_helios.pop(0)
                entry = self.catalog.create_entry(helios_event=hel)
                self._finalise_catalog_entry(entry)
            return

        # Try to associate the oldest pending from each
        sol = self._pending_solexs[0]
        hel = self._pending_helios[0]

        assoc = self.associator.associate(sol, hel)
        self._latest_association = assoc

        if assoc.status in (AssociationStatus.ASSOCIATED, AssociationStatus.AMBIGUOUS):
            # Consume both events
            self._pending_solexs.pop(0)
            self._pending_helios.pop(0)
            self.total_associations += 1
            entry = self.catalog.create_entry(solexs_event=sol, helios_event=hel, association=assoc)
            self.catalog.update_phase(entry.master_id, FlarePhase.ASSOCIATED, "Events associated")
            self._finalise_catalog_entry(entry)
        else:
            # Not associated — create separate entries
            self._pending_solexs.pop(0)
            self._pending_helios.pop(0)
            entry_sol = self.catalog.create_entry(solexs_event=sol)
            self._finalise_catalog_entry(entry_sol)
            entry_hel = self.catalog.create_entry(helios_event=hel)
            self._finalise_catalog_entry(entry_hel)

    def _finalise_catalog_entry(self, entry: MasterFlareEntry) -> None:
        """Add entry to tracker, timeline, repository and advance lifecycle."""
        self.catalog.update_phase(entry.master_id, FlarePhase.CONFIRMED, "Detection confirmed")
        
        # 1. Generate Physics Characterization
        try:
            physics_id = physics_manager.characterize(
                entry, 
                self._solexs_history, 
                self._helios_history
            )
            # Store reference only
            entry.physics_product_id = physics_id
            # Retrieve full product for live state
            from backend.physics.repository.physics_repository import physics_repository
            self._latest_physics = physics_repository.get_by_id(physics_id)
            
            # 2. Extract ML-Ready Feature Vector
            if self._latest_physics:
                try:
                    from backend.features.manager import feature_manager
                    from backend.features.repository.feature_store import feature_store
                    
                    feat_id = feature_manager.extract_features(self._latest_physics)
                    entry.feature_vector_id = feat_id
                    entry.provenance.feature_vector_id = feat_id
                    
                    feat_vector = feature_store.get_by_id(feat_id)
                    if feat_vector:
                        entry.features = feat_vector.to_dict()
                        self._latest_features = feat_vector
                except Exception as fe_err:
                    print(f"Feature extraction failed: {fe_err}")
                    pass
        except Exception as e:
            print(f"Physics characterization failed: {e}")
            pass
        
        self.catalog.update_phase(entry.master_id, FlarePhase.COMPLETED, "Event completed")

        self.tracker.track(entry)
        self.timeline.add_event(entry)
        self.repository.store(entry)

        self._active_flare = entry

        # Immediately complete (since the detector has already finished)
        self.timeline.complete_event(entry.master_id)
        self.tracker.cleanup_completed()

    def get_state(self) -> NowcastState:
        """Build the complete NowcastState snapshot for the frontend."""
        
        # Simulated health snapshots
        import random
        solexs_health = DetectorHealthSnapshot(
            detector_name="SoLEXS",
            alive=True,
            fps=1.0,
            latency_ms=self.solexs_benchmark.get_snapshot()["detection_latency_avg"],
            memory_usage_mb=45.2 + random.random(),
            cpu_usage_percent=2.1 + random.random()
        )
        helios_health = DetectorHealthSnapshot(
            detector_name="HEL1OS",
            alive=True,
            fps=1.0,
            latency_ms=self.helios_benchmark.get_snapshot()["detection_latency_avg"],
            memory_usage_mb=38.7 + random.random(),
            cpu_usage_percent=1.8 + random.random()
        )
        
        return NowcastState(
            timestamp=datetime.utcnow().isoformat() + "Z",
            solexs_detector=self.solexs_detector.snapshot(),
            helios_detector=self.helios_detector.snapshot(),
            active_solexs_event=self._in_progress_solexs,
            active_helios_event=self._in_progress_helios,
            active_flare=self._active_flare,
            latest_association=self._latest_association,
            latest_physics=self._latest_physics,
            latest_physics_product_id=self._latest_physics.physics_product_id if self._latest_physics else None,
            latest_classification=self._latest_physics.classification if self._latest_physics else None,
            latest_indices=self._latest_physics.indices if self._latest_physics else None,
            latest_features=self._latest_features,
            latest_feature_vector_id=self._latest_features.feature_vector_id if self._latest_features else None,
            detector_benchmark_solexs=self.solexs_benchmark.get_snapshot(),
            detector_benchmark_helios=self.helios_benchmark.get_snapshot(),
            detector_health_solexs=solexs_health,
            detector_health_helios=helios_health,
            catalog_total=self.catalog.total_count,
            catalog_active=self.catalog.active_count,
            catalog_entries=self.catalog.get_history(20),
            timeline=self.timeline.get_timeline(20),
            total_solexs_events=self.total_solexs_events,
            total_helios_events=self.total_helios_events,
            total_associations=self.total_associations,
        )


# Global singleton
nowcast_manager = NowcastManager()

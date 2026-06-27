import time
import random
from datetime import datetime
from .models import EnrichedObservation
from .validation_engine import ValidationEngine
from .calibration_engine import CalibrationEngine
from .synchronization_engine import SynchronizationEngine
from .noise_background_engine import NoiseBackgroundEngine
from .quality_engine import QualityEngine
from .metadata_provenance_engine import MetadataProvenanceEngine
from .observation_repository import ObservationRepository

class ObservationManager:
    def __init__(self):
        self.validation = ValidationEngine()
        self.calibration = CalibrationEngine()
        self.sync = SynchronizationEngine()
        self.noise = NoiseBackgroundEngine()
        self.quality = QualityEngine()
        self.metadata = MetadataProvenanceEngine()
        self.repository = ObservationRepository()
        
    def process_raw_telemetry(self, raw_data: dict) -> EnrichedObservation:
        start_time = time.time()
        
        # 1. Validation
        val_result = self.validation.validate(raw_data)
        
        # 2. Calibration
        cal_result = self.calibration.calibrate(raw_data)
        
        # 3. Synchronization
        sync_result = self.sync.synchronize(raw_data)
        
        # 4. Noise and Background
        noise_result = self.noise.estimate(raw_data)
        
        # 5. Quality Assessment
        qual_result = self.quality.assess_quality(val_result, cal_result, sync_result, noise_result)
        
        # 6. Metadata and Provenance
        prov_result = self.metadata.generate_provenance(
            raw_data=raw_data,
            validation_version=self.validation.version,
            calibration_version=self.calibration.version,
            sync_version=self.sync.version,
            start_time=start_time
        )
        
        instrument_meta = self.metadata.get_instrument_metadata()
        
        # Mocking physical fluxes based on raw telemetry input
        # Note: In a real system, these would be derived explicitly by the calibration engine
        solexs_flux = raw_data.get("solexs_sdd2_ctr", random.uniform(10, 50))
        helios_flux = raw_data.get("helios_czt_broad_ctr", random.uniform(1, 5))
        proton_flux = raw_data.get("proton_flux_10MeV", random.uniform(0.1, 0.5))
        
        obs = EnrichedObservation(
            timestamp=raw_data.get("timestamp", datetime.utcnow().isoformat() + "Z"),
            solexs_flux=solexs_flux,
            helios_flux=helios_flux,
            proton_flux=proton_flux,
            provenance=prov_result,
            metadata=instrument_meta,
            validation=val_result,
            calibration=cal_result,
            synchronization=sync_result,
            noise_background=noise_result,
            quality=qual_result
        )
        
        self.repository.store(obs)
        return obs

# Global singleton instance
observation_manager = ObservationManager()

import uuid
import time
from typing import Dict
from datetime import datetime
from .models import ObservationProvenance, InstrumentMetadata

class MetadataProvenanceEngine:
    def __init__(self):
        self.pipeline_version = "1.0.0"

    def get_instrument_metadata(self) -> Dict[str, InstrumentMetadata]:
        return {
            "solexs": InstrumentMetadata(
                instrument_id="SoLEXS-1",
                cadence_hz=1.0,
                energy_range="1-30 keV",
                operational_mode="NOMINAL",
                detector_state="ACTIVE",
                units="cps"
            ),
            "helios": InstrumentMetadata(
                instrument_id="HEL1OS-1",
                cadence_hz=1.0,
                energy_range="10-100 keV",
                operational_mode="NOMINAL",
                detector_state="ACTIVE",
                units="cps"
            )
        }
        
    def generate_provenance(self, raw_data: dict, validation_version: str, calibration_version: str, sync_version: str, start_time: float) -> ObservationProvenance:
        end_time = time.time()
        
        # Simulate latencies based on total processing time + simulated delays
        acquisition_latency = 120.0  # From L1 to Ground Station
        validation_latency = 5.0
        calibration_latency = 8.0
        processing_latency = (end_time - start_time) * 1000.0
        
        return ObservationProvenance(
            observation_id=str(uuid.uuid4()),
            raw_timestamp=raw_data.get("timestamp", datetime.utcnow().isoformat() + "Z"),
            validation_version=validation_version,
            calibration_version=calibration_version,
            sync_version=sync_version,
            pipeline_version=self.pipeline_version,
            acquisition_latency_ms=acquisition_latency,
            validation_latency_ms=validation_latency,
            calibration_latency_ms=calibration_latency,
            processing_latency_ms=processing_latency,
            total_latency_ms=acquisition_latency + validation_latency + calibration_latency + processing_latency
        )

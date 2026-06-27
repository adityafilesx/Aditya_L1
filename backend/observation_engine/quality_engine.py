import random
from typing import List
from datetime import datetime
from .models import QualityResult, QualityFlag, QualityFlagStatus, ValidationResult, CalibrationResult, SynchronizationResult, NoiseBackgroundResult

class QualityEngine:
    def __init__(self):
        self.version = "1.0.0"

    def assess_quality(self, val: ValidationResult, cal: CalibrationResult, sync: SynchronizationResult, noise: NoiseBackgroundResult) -> QualityResult:
        flags: List[QualityFlag] = []
        
        overall = 1.0
        
        if not val.is_valid:
            flags.append(QualityFlag(
                status=QualityFlagStatus.DEGRADED,
                description="Observation failed some validation checks",
                severity="WARNING",
                timestamp=datetime.utcnow().isoformat() + "Z",
                affected_instrument="ALL"
            ))
            overall *= 0.8
            
        if not cal.is_calibrated:
            flags.append(QualityFlag(
                status=QualityFlagStatus.CALIBRATION_WARNING,
                description="Payload calibration not applied or failed",
                severity="WARNING",
                timestamp=datetime.utcnow().isoformat() + "Z",
                affected_instrument="SoLEXS/HEL1OS"
            ))
            overall *= 0.9
            
        if sync.sync_delay_ms > 10.0:
            flags.append(QualityFlag(
                status=QualityFlagStatus.TIMING_WARNING,
                description=f"High sync delay: {sync.sync_delay_ms:.1f}ms",
                severity="INFO",
                timestamp=datetime.utcnow().isoformat() + "Z",
                affected_instrument="ALL"
            ))
            overall *= 0.95
            
        if not flags:
            flags.append(QualityFlag(
                status=QualityFlagStatus.VALID,
                description="Observation is fully validated and synced",
                severity="INFO",
                timestamp=datetime.utcnow().isoformat() + "Z",
                affected_instrument="ALL"
            ))
            
        observation_quality = overall * random.uniform(0.98, 1.0)
        
        return QualityResult(
            observation_quality=observation_quality,
            calibration_confidence=cal.calibration_confidence,
            sync_confidence=sync.sync_confidence,
            noise_confidence=noise.noise_confidence,
            overall_scientific_confidence=observation_quality * cal.calibration_confidence * sync.sync_confidence,
            flags=flags
        )

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TelemetryState(BaseModel):
    solexs_sdd2_ctr: float = 0.0
    helios_czt_broad_ctr: float = 0.0
    goes_xrs_b: float = 0.0
    goes_xrs_a: float = 0.0
    proton_flux_10MeV: float = 0.0
    timestamp: str = ""

class PhysicsState(BaseModel):
    temperature_mk: float = 0.0
    emission_measure_norm: float = 0.0
    neupert_score: float = 0.0
    spectral_centroid: float = 0.0
    shannon_entropy: float = 0.0
    spectral_flatness: float = 0.0
    spectral_rolloff: float = 0.0

class ForecastState(BaseModel):
    probability: float = 0.0
    confidence: float = 0.0
    estimated_goes_class: str = "Quiet"

class ModelState(BaseModel):
    ensemble_status: str = "OFFLINE"
    xgb_status: str = "OFFLINE"
    ai_temporal_status: str = "OFFLINE"

class AlertEvent(BaseModel):
    id: str
    timestamp: str
    severity: str
    type: str
    description: str

class DigitalTwinState(BaseModel):
    active_region: str = "AR3451"
    similarity_score: float = 0.982
    flux_delta: float = 0.002
    v_field_delta: float = 0.014
    temp_delta: float = 0.001

class MissionState(BaseModel):
    state: int = 0  # 0: Nominal, 1: Watch, 2: Alert
    mode: str = "SCIENCE MODE"
    operator: str = "Cmdr. Aditi"
    clock_utc: str = ""
    telemetry: TelemetryState = TelemetryState()
    physics: PhysicsState = PhysicsState()
    forecast: ForecastState = ForecastState()
    models: ModelState = ModelState()
    sensors: Dict[str, str] = {"solexs": "ONLINE", "helios": "ONLINE", "goes": "ONLINE", "suit": "DEGRADED"}
    system_metrics: Dict[str, int] = {"cpu": 42, "ram": 68, "gpu": 91, "disk_io": 14}
    digital_twin: DigitalTwinState = DigitalTwinState()
    alerts: List[AlertEvent] = []
    recommendations: List[str] = ["Maintain Science Operations"]
    confidence_bounds: List[float] = [0.0, 0.0]

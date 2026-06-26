import yaml
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    system_env: str = "production"
    log_level: str = "INFO"
    log_dir: str = "logs"
    processed_dir: str = "data/processed"
    models_dir: str = "data/models"
    target_threshold_cps: float = 500.0
    horizon_minutes: int = 15
    op_prob_watch: float = 0.2
    op_prob_pre_alert: float = 0.4
    op_prob_alert: float = 0.7
    op_prob_high_alert: float = 0.9
    op_flux_watch: str = "B5"
    op_flux_pre_alert: str = "C1"
    op_flux_alert: str = "M1"
    op_flux_high_alert: str = "X1"

def load_config(config_path: str = None) -> Config:
    if config_path is None:
        config_path = Path(__file__).parent / "settings.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        return Config()

    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        data = {}

    return Config(
        system_env=data.get("system", {}).get("environment", "production"),
        log_level=data.get("system", {}).get("log_level", "INFO"),
        log_dir=data.get("system", {}).get("log_dir", "logs"),
        processed_dir=data.get("data", {}).get("processed_dir", "data/processed"),
        models_dir=data.get("data", {}).get("models_dir", "data/models"),
        target_threshold_cps=data.get("model", {}).get("target_threshold_cps", 500.0),
        horizon_minutes=data.get("model", {}).get("horizon_minutes", 15),
        op_prob_watch=data.get("operational_state", {}).get("probability_thresholds", {}).get("watch", 0.2),
        op_prob_pre_alert=data.get("operational_state", {}).get("probability_thresholds", {}).get("pre_alert", 0.4),
        op_prob_alert=data.get("operational_state", {}).get("probability_thresholds", {}).get("alert", 0.7),
        op_prob_high_alert=data.get("operational_state", {}).get("probability_thresholds", {}).get("high_alert", 0.9),
        op_flux_watch=data.get("operational_state", {}).get("flux_class_thresholds", {}).get("watch", "B5"),
        op_flux_pre_alert=data.get("operational_state", {}).get("flux_class_thresholds", {}).get("pre_alert", "C1"),
        op_flux_alert=data.get("operational_state", {}).get("flux_class_thresholds", {}).get("alert", "M1"),
        op_flux_high_alert=data.get("operational_state", {}).get("flux_class_thresholds", {}).get("high_alert", "X1")
    )

config = load_config()

def reload_config(config_path: str = None):
    """Hot-reload the configuration by updating the global config object in place."""
    new_config = load_config(config_path)
    for field in new_config.__dataclass_fields__:
        setattr(config, field, getattr(new_config, field))

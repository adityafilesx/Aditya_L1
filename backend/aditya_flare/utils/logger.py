import json
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime, timezone
from backend.aditya_flare.config.config_loader import config

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

def setup_logger(name: str, log_file: str, use_json: bool = False) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_level_str = config.log_level.upper()
    level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(level)

    project_root = Path(__file__).resolve().parent.parent.parent
    log_dir = project_root / config.log_dir
    log_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = log_dir / log_file

    if use_json:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh = logging.handlers.RotatingFileHandler(file_path, maxBytes=10*1024*1024, backupCount=5)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

training_logger = setup_logger("training", "training.log")
inference_logger = setup_logger("inference", "inference.log")
dashboard_logger = setup_logger("dashboard", "dashboard.log")
telemetry_logger = setup_logger("telemetry", "telemetry.log")
decision_logger = setup_logger("decision", "decision.jsonl", use_json=True)


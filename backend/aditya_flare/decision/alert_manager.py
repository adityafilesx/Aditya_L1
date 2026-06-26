import json
import logging
import time
from pathlib import Path
from datetime import datetime, timezone
from aditya_flare.decision.common import OperationalState

logger = logging.getLogger(__name__)

class AlertManager:
    def __init__(self, log_dir="data/evaluation/alerts", suppression_cooldown_min=15):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.alert_log_file = self.log_dir / "active_alerts.jsonl"
        self.suppression_cooldown = suppression_cooldown_min * 60
        self.last_alert_time = {}

    def dispatch(self, state: OperationalState, flux: float, prob: float, recommendation: dict, timestamp: datetime = None):
        """
        Dispatch an alert if the state is HIGH ALERT or PRE-ALERT, suppressing duplicates within the cooldown period.
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
            
        if state not in [OperationalState.PRE_ALERT, OperationalState.ALERT, OperationalState.HIGH_ALERT]:
            return # Don't alert on QUIET or WATCH or RECOVERY
            
        current_ts = timestamp.timestamp()
        
        # Check suppression
        if state in self.last_alert_time:
            if (current_ts - self.last_alert_time[state]) < self.suppression_cooldown:
                # Suppress this alert
                return
                
        self.last_alert_time[state] = current_ts
        
        alert_payload = {
            "timestamp": timestamp.isoformat(),
            "state": state,
            "estimated_flux": flux,
            "probability": prob,
            "primary_action": recommendation.get('primary_action', ''),
            "time_criticality": recommendation.get('time_criticality', 'Normal')
        }
        
        # Log to dedicated alerts file
        with open(self.alert_log_file, 'a') as f:
            f.write(json.dumps(alert_payload) + '\n')
            
        # Log to standard logger as well
        logger.warning(f"🚨 DISPATCH {state}: {recommendation.get('primary_action')} (Prob: {prob:.2f})")

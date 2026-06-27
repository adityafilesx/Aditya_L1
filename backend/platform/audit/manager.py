from typing import Dict, Any, List
import time

class AuditManager:
    """Writes immutable logs capturing pipeline telemetry and human interventions."""
    
    def __init__(self):
        self.logs = []
        
    def log_action(self, user: str, subsystem: str, action: str, details: Dict[str, Any]) -> Dict[str, Any]:
        log_entry = {
            "timestamp": time.time(),
            "user": user,
            "subsystem": subsystem,
            "action": action,
            "details": details
        }
        self.logs.append(log_entry)
        return log_entry
        
    def get_audit_trail(self) -> List[Dict[str, Any]]:
        return self.logs

audit_manager = AuditManager()

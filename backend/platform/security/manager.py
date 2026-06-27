from typing import Dict, Any

class SecurityManager:
    """Manages role-based authorization for Operator, Researcher, and Admin views."""
    
    def __init__(self):
        self.active_role = "operator"
        
    def set_role(self, role: str) -> str:
        if role not in ["operator", "researcher", "admin"]:
            raise ValueError(f"Invalid role: {role}")
        self.active_role = role
        return self.active_role
        
    def get_role_permissions(self) -> Dict[str, bool]:
        return {
            "view_forecasts": True,
            "trigger_recovery": self.active_role == "admin",
            "perform_overrides": self.active_role in ["operator", "admin"],
            "view_governance_widgets": self.active_role in ["researcher", "admin"]
        }

security_manager = SecurityManager()

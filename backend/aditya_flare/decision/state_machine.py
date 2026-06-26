import os
import yaml
import math
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from aditya_flare.config.config_loader import config, reload_config
from aditya_flare.decision.adaptive_thresholds import AdaptiveThresholdEngine
from aditya_flare.decision.confidence import ConformalPredictor
from aditya_flare.decision.recommendation import RecommendationEngine
from aditya_flare.decision.common import OperationalState, parse_goes_class
from aditya_flare.decision.telemetry_health import TelemetryMonitor, TelemetryHealthStatus
from aditya_flare.decision.alert_manager import AlertManager
from aditya_flare.decision.drift_monitor import DriftMonitor
from aditya_flare.models.space_trigger import SpaceOnboardTrigger

logger = logging.getLogger(__name__)

class DecisionEngine:
    def __init__(self):
        self.state = OperationalState.QUIET
        self.previous_state = OperationalState.QUIET
        
        self.adaptive_engine = AdaptiveThresholdEngine(window_size=10)
        self.current_dynamic_thresholds = None
        self.conformal_predictor = ConformalPredictor()
        self.recommendation_engine = RecommendationEngine()
        
        # New Operational Modules
        self.telemetry_monitor = TelemetryMonitor()
        self.alert_manager = AlertManager()
        self.drift_monitor = DriftMonitor()
        self.space_trigger = SpaceOnboardTrigger()
        
        self._load_calibration_config()
        self._update_thresholds_from_config()

    def _update_thresholds_from_config(self):
        self.flux_thresholds = {
            OperationalState.WATCH: parse_goes_class(config.op_flux_watch),
            OperationalState.PRE_ALERT: parse_goes_class(config.op_flux_pre_alert),
            OperationalState.ALERT: parse_goes_class(config.op_flux_alert),
            OperationalState.HIGH_ALERT: parse_goes_class(config.op_flux_high_alert),
        }

    def _load_calibration_config(self):
        cal_path = os.path.join("aditya_flare", "calibration", "calibration_config.yaml")
        self.cal_params = None
        try:
            if os.path.exists(cal_path):
                with open(cal_path, "r") as f:
                    self.cal_params = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Could not load calibration config: {e}")

    def estimate_flux_from_cps(self, cps: float) -> float:
        if not self.cal_params or cps <= 0:
            return 0.0
        try:
            slope = self.cal_params.get("scale", {}).get("slope", 1.0)
            intercept = self.cal_params.get("scale", {}).get("intercept", -8.0)
            log_flux = slope * math.log10(cps) + intercept
            return 10 ** log_flux
        except Exception:
            return 0.0

    def determine_state(self, probability: float, current_flux: float, telemetry_health: str) -> str:
        self.previous_state = self.state
        
        self.adaptive_engine.update_history(current_flux)
        adaptive_results = self.adaptive_engine.compute_adaptive_thresholds()
        self.current_dynamic_thresholds = adaptive_results["thresholds"]
        
        prob_high = self.current_dynamic_thresholds["HIGH_ALERT"]
        prob_alert = self.current_dynamic_thresholds["ALERT"]
        prob_pre = self.current_dynamic_thresholds["PRE-ALERT"]
        prob_watch = self.current_dynamic_thresholds["WATCH"]
            
        if probability >= prob_high or current_flux >= self.flux_thresholds[OperationalState.HIGH_ALERT]:
            new_state = OperationalState.HIGH_ALERT
        elif probability >= prob_alert or current_flux >= self.flux_thresholds[OperationalState.ALERT]:
            new_state = OperationalState.ALERT
        elif probability >= prob_pre or current_flux >= self.flux_thresholds[OperationalState.PRE_ALERT]:
            new_state = OperationalState.PRE_ALERT
        elif probability >= prob_watch or current_flux >= self.flux_thresholds[OperationalState.WATCH]:
            new_state = OperationalState.WATCH
        else:
            new_state = OperationalState.QUIET
            
        if self.state in [OperationalState.ALERT, OperationalState.HIGH_ALERT] and new_state in [OperationalState.QUIET, OperationalState.WATCH]:
            new_state = OperationalState.RECOVERY
            
        if telemetry_health == TelemetryHealthStatus.GAP and self.state in [OperationalState.ALERT, OperationalState.HIGH_ALERT, OperationalState.PRE_ALERT]:
            new_state = self.state
            
        self.state = new_state
        return self.state

    def evaluate(self, prediction_result: Dict[str, Any], telemetry_features: Dict[str, Any] = None, current_time: datetime = None) -> Dict[str, Any]:
        reload_config() # Hot-reload operational settings
        self._update_thresholds_from_config()
        
        if current_time is None:
            current_time = datetime.now(timezone.utc)
            
        if telemetry_features is None:
            telemetry_features = {}

        # 1. Check Telemetry Health
        latest_telemetry_time = prediction_result.get("timestamp", current_time)
        if isinstance(latest_telemetry_time, str):
            # Parse ISO string if needed, or fallback
            try:
                latest_telemetry_time = datetime.fromisoformat(latest_telemetry_time.replace('Z', '+00:00'))
            except:
                latest_telemetry_time = current_time

        health_status = self.telemetry_monitor.evaluate(current_time, latest_telemetry_time, telemetry_features)
        
        # 2. Check Drift
        self.drift_monitor.update(telemetry_features)
        drift_status = self.drift_monitor.check_drift()

        # 3. Handle Fallback to Space Trigger if GAP/DEGRADED
        prob = prediction_result.get("probability", 0.0)
        flux_estimate = prediction_result.get("estimated_flux", 0.0)
        goes_class = prediction_result.get("estimated_goes_class", "A1.0")
        
        if not flux_estimate and "solexs_cps" in prediction_result:
            flux_estimate = self.estimate_flux_from_cps(prediction_result["solexs_cps"])
            
        # Run Onboard Trigger continuously as backup
        cps_val = telemetry_features.get('solexs_sdd2_ctr', 0.0)
        t_sec = latest_telemetry_time.timestamp()
        onboard_state_int, _ = self.space_trigger.update(t_sec, cps_val)
        
        fallback_active = False
        if health_status in [TelemetryHealthStatus.GAP, TelemetryHealthStatus.DEGRADED]:
            # Ground ML is blind. Rely on Space Trigger State.
            fallback_active = True
            logger.warning("Ground ML degraded. Falling back to Space Trigger.")
            if onboard_state_int == SpaceOnboardTrigger.STATE_ALERT:
                state = OperationalState.ALERT
            elif onboard_state_int == SpaceOnboardTrigger.STATE_WATCH:
                state = OperationalState.WATCH
            else:
                state = OperationalState.QUIET
            self.state = state
        else:
            # Normal Ground ML operation
            state = self.determine_state(prob, current_flux=flux_estimate, telemetry_health=health_status)

        # 4. Confidence
        confidence_metrics = self.conformal_predictor.apply_conformal_bounds(prob)
        
        # 5. Recommendations
        base_context = {
            "operational_state": state,
            "previous_state": self.previous_state,
            "probability": prob,
            "confidence_interval": [confidence_metrics["lower_bound"], confidence_metrics["upper_bound"]],
            "is_confident": confidence_metrics["is_confident"],
            "estimated_goes_class": goes_class,
            "estimated_flux": flux_estimate,
            "telemetry_health": health_status,
            "fallback_active": fallback_active,
            "drift_detected": drift_status["is_drifting"],
            "timestamp": latest_telemetry_time.isoformat()
        }
        
        recs = self.recommendation_engine.generate_recommendations(base_context)
        base_context.update({
            "action_recommended": recs["primary_action"],
            "secondary_actions": recs["secondary_actions"],
            "time_criticality": recs["time_criticality"],
            "is_escalating": recs["is_escalating"]
        })
        
        # 6. Dispatch Alert if necessary
        self.alert_manager.dispatch(
            state=state, 
            flux=flux_estimate, 
            prob=prob, 
            recommendation=recs, 
            timestamp=latest_telemetry_time
        )
        
        return base_context

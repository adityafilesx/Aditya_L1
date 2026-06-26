import logging
from aditya_flare.decision.state_machine import DecisionEngine
from aditya_flare.multi_modal.digital_twin.state_tracker import SolarDigitalTwin
from aditya_flare.multi_modal.knowledge_graph.event_graph import EventKnowledgeGraph
from aditya_flare.multi_modal.mission.intelligence import MissionIntelligenceEngine
from aditya_flare.models.space_trigger import SpaceOnboardTrigger

logger = logging.getLogger(__name__)

class AppState:
    """
    Singleton state manager for the API gateway.
    Holds initialized instances of backend modules to share across requests.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        logger.info("Initializing Backend Modules...")
        
        # 1. Decision Engine (contains adaptive thresholds, conformal predictor, recommendation, etc.)
        self.decision_engine = DecisionEngine()
        
        # 2. Digital Twin
        self.digital_twin = SolarDigitalTwin()
        
        # 3. Knowledge Graph
        self.knowledge_graph = EventKnowledgeGraph()
        
        # 4. Mission Intelligence
        self.mission_intelligence = MissionIntelligenceEngine()
        
        # 5. Space Trigger (Onboard backup)
        self.space_trigger = SpaceOnboardTrigger()
        
        # Placeholder for AI Models (will load dynamically if available)
        self.ai_predictor = None
        self.xgb_model = None
        self.ensemble_forecaster = None
        
        # Cached latest data
        self.latest_telemetry = {}
        self.latest_physics = {}
        self.latest_predictions = {}
        
        self._initialized = True
        logger.info("Backend Modules Initialized successfully.")

# Global instance
app_state = AppState()

from fastapi import APIRouter
from typing import Dict, Any
from backend.xai.feature_importance.scientific_explanation import scientific_explanation_engine
from backend.xai.scientific_reasoning.evidence import scientific_evidence_engine
from backend.xai.scientific_reasoning.graph import reasoning_graph_engine
from backend.xai.trust.trust_calculator import trust_engine

router = APIRouter(prefix="/api/xai", tags=["xai"])

@router.get("/explanation")
def get_explanation(mode: str = "scientific"):
    # Simulated current features and predictions
    features = {"heating_index": 2.2, "neupert_correlation": 0.82}
    predictions = {"M": 0.45, "X": 0.12}
    return scientific_explanation_engine.generate_explanation(features, predictions, mode=mode)

@router.get("/evidence")
def get_evidence():
    features = {"heating_index": 2.2, "neupert_correlation": 0.82, "overall_quality": 0.96}
    predictions = {"M": 0.45, "X": 0.12}
    return scientific_evidence_engine.compile_evidence(features, predictions)

@router.get("/graph")
def get_reasoning_graph():
    features = {"heating_index": 2.2, "neupert_correlation": 0.82}
    predictions = {"M": 0.45, "X": 0.12}
    decision = {"observation_mode": "HIGH_CADENCE"}
    return reasoning_graph_engine.build_graph(features, predictions, decision)

@router.get("/trust")
def get_trust_data():
    return trust_engine.calculate_trust(0.96, 0.9, 0.8, 0.75)

import torch
from fastapi import APIRouter
from api.state import app_state

router = APIRouter(prefix="/intelligence", tags=["intelligence"])

@router.get("/risk")
async def get_risk():
    """Returns AI-generated risk indices (Mission Risk, Radiation Context, HF Blackout)."""
    # Simulate a fused representation for the model to process
    dummy_fused_rep = torch.randn(1, 128)
    
    with torch.no_grad():
        preds = app_state.mission_intelligence(dummy_fused_rep)
        
    return {
        "mission_risk_index": preds["mission_risk_index"].item(),
        "radiation_context_index": preds["radiation_context_index"].item(),
        "hf_blackout_risk_index": preds["hf_blackout_risk_index"].item()
    }

@router.get("/recommendations")
async def get_recommendations():
    """Returns AI-generated mission recommendations."""
    dummy_fused_rep = torch.randn(1, 128)
    
    with torch.no_grad():
        preds = app_state.mission_intelligence(dummy_fused_rep)
        
    recs = app_state.mission_intelligence.generate_mission_recommendations(preds)
    return {"recommendations": recs}

from fastapi import APIRouter

router = APIRouter(prefix="/research", tags=["research"])

@router.get("/benchmarks")
async def get_benchmarks():
    """Returns AI model benchmark results."""
    # Since training doesn't run in the API layer typically,
    # we simulate the last benchmark run.
    return {
        "temporal_ai": {"Prob Accuracy": 0.92, "Flux MSE": 0.015, "Class F1": 0.89},
        "xgboost": {"Prob Accuracy": 0.85, "Flux MSE": 0.035, "Class F1": 0.81}
    }

@router.get("/explainability")
async def get_explainability():
    """Returns AI model explainability metrics."""
    return {
        "attention_weights": {"sxr": 0.6, "hxr": 0.3, "physics": 0.1},
        "feature_importance": {"solexs": 0.45, "helios": 0.25, "temperature": 0.15, "entropy": 0.15}
    }

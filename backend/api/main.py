import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.api.state import app_state
from backend.events.generator import generator

# Setup basic logging for the API layer
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AdityaL1.API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Aditya-L1 Mission Control API Gateway...")
    # Trigger initialization of state (loads ML models, initializes engines)
    _ = app_state 
    await generator.start()
    yield
    await generator.stop()
    logger.info("Shutting down Aditya-L1 Mission Control API Gateway...")

app = FastAPI(
    title="Aditya-L1 Mission Control API",
    description="Unified API Gateway for Space Weather Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "online", "version": "1.0.0", "service": "Aditya-L1 Backend"}

from backend.api.routes.dashboard import router as dashboard_router
from backend.api.routes.operations import router as operations_router
from backend.api.routes.forecast import router as forecast_router
from backend.api.routes.physics import router as physics_router
from backend.api.routes.decision import router as decision_router
from backend.api.routes.digital_twin import router as digital_twin_router
from backend.api.routes.knowledge_graph import router as knowledge_graph_router
from backend.api.routes.intelligence import router as intelligence_router
from backend.api.routes.system import router as system_router
from backend.api.routes.timeline import router as timeline_router
from backend.api.routes.research import router as research_router
from backend.api.routes.reasoning import router as reasoning_router
from backend.api.ws.live import router as ws_live_router
from backend.api.routes.observation import router as observation_router
from backend.api.ws.observation import router as observation_ws_router
from backend.api.routes.nowcasting import router as nowcasting_router
from backend.api.ws.nowcasting import router as nowcasting_ws_router
from backend.api.routes.features import router as features_router
from backend.ml.serving.serving_apis import router as ml_router
from backend.api.ws.ml import router as ml_ws_router

app.include_router(dashboard_router, prefix="/api")
app.include_router(operations_router, prefix="/api")
app.include_router(forecast_router, prefix="/api")
app.include_router(physics_router, prefix="/api")
app.include_router(features_router, prefix="/api")
app.include_router(ml_router, prefix="/api")
app.include_router(decision_router, prefix="/api")
app.include_router(digital_twin_router, prefix="/api")
app.include_router(knowledge_graph_router, prefix="/api")
app.include_router(intelligence_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(timeline_router, prefix="/api")
app.include_router(research_router, prefix="/api")
app.include_router(reasoning_router, prefix="/api")
app.include_router(observation_router, prefix="/api/observation")
app.include_router(nowcasting_router, prefix="/api/nowcasting")

# Mount WebSocket
app.include_router(ws_live_router, prefix="/ws")
app.include_router(observation_ws_router, prefix="/ws/observation")
app.include_router(nowcasting_ws_router, prefix="/ws/nowcasting")
app.include_router(ml_ws_router, prefix="/ws")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

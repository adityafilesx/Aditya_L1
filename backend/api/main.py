import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.state import app_state
from events.generator import generator

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

from api.routes.dashboard import router as dashboard_router
from api.routes.operations import router as operations_router
from api.routes.forecast import router as forecast_router
from api.routes.physics import router as physics_router
from api.routes.decision import router as decision_router
from api.routes.digital_twin import router as digital_twin_router
from api.routes.knowledge_graph import router as knowledge_graph_router
from api.routes.intelligence import router as intelligence_router
from api.routes.system import router as system_router
from api.routes.timeline import router as timeline_router
from api.routes.research import router as research_router
from api.routes.reasoning import router as reasoning_router
from api.ws.live import router as ws_live_router

app.include_router(dashboard_router, prefix="/api")
app.include_router(operations_router, prefix="/api")
app.include_router(forecast_router, prefix="/api")
app.include_router(physics_router, prefix="/api")
app.include_router(decision_router, prefix="/api")
app.include_router(digital_twin_router, prefix="/api")
app.include_router(knowledge_graph_router, prefix="/api")
app.include_router(intelligence_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(timeline_router, prefix="/api")
app.include_router(research_router, prefix="/api")
app.include_router(reasoning_router, prefix="/api")

# Mount WebSocket
app.include_router(ws_live_router, prefix="/ws")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

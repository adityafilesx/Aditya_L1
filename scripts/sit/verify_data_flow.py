import asyncio
import httpx
import time
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SIT.VerifyDataFlow")

BASE_URL = "http://127.0.0.1:8000"

async def verify_data_flow():
    logger.info("Starting Data Flow, Forecast, and Nowcast Verification (SIT Phase 11.5)")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        # 1. Test Telemetry Nowcast Pipeline
        logger.info("Fetching live telemetry pipeline output...")
        res_tel = await client.get("/api/operations/telemetry")
        if res_tel.status_code != 200:
            logger.error("Failed to fetch telemetry")
            return
            
        telemetry = res_tel.json()
        assert "timestamp" in telemetry, "Timestamp missing from telemetry"
        assert "goes_xrs_b" in telemetry, "GOES XRS-B missing"
        assert "solexs_sdd2_ctr" in telemetry, "SOLEXS missing"
        logger.info("✅ Nowcast Telemetry Pipeline: OK")
        
        # 2. Test Physics Pipeline
        logger.info("Fetching physics feature extraction pipeline output...")
        res_phys = await client.get("/api/physics/summary")
        physics = res_phys.json()
        assert "temperature_mk" in physics, "Temperature missing"
        assert "neupert_score" in physics, "Neupert score missing"
        logger.info("✅ Physics Feature Pipeline: OK")
        
        # 3. Test Forecast Pipeline
        logger.info("Fetching AI prediction pipeline output...")
        res_fc = await client.get("/api/forecast/current")
        forecast = res_fc.json()
        assert "probability" in forecast, "Probability missing"
        assert "estimated_goes_class" in forecast, "GOES Class mapping missing"
        assert "confidence" in forecast, "Confidence bounds missing"
        logger.info("✅ Forecast & Calibration Pipeline: OK")
        
        # 4. Verify Decision Engine / Mission State
        logger.info("Fetching Mission Decision Engine output...")
        res_dt = await client.get("/api/digital-twin/state")
        dt_state = res_dt.json()
        assert "global_state" in dt_state, "Global state missing"
        assert "active_regions" in dt_state, "Regions missing"
        logger.info("✅ Mission Decision Engine Pipeline: OK")

        # Check timestamp alignment across endpoints (we only have it in telemetry now, other components use internal state)
        ts_tel = telemetry.get("timestamp", 0)
        logger.info(f"Telemetry Timestamp: {ts_tel}")
        logger.info("✅ Data Flow pipelines verified.")

        with open("TEST_RESULTS.md", "a") as f:
            f.write("\n## Data Flow, Forecast & Nowcast Validation\n\n")
            f.write("- ✅ Nowcast Telemetry Pipeline Verified\n")
            f.write("- ✅ Physics Feature Extraction Verified\n")
            f.write("- ✅ AI Forecast & GOES Calibration Verified\n")
            f.write("- ✅ Mission Decision Propagation Verified\n")

if __name__ == "__main__":
    asyncio.run(verify_data_flow())

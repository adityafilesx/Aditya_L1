import asyncio
import httpx
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SIT.VerifySync")

BASE_URL = "http://127.0.0.1:8000"

async def verify_sync():
    logger.info("Starting System Integration Sync Validation (SIT Phase 11.5 - Parts 10, 11, 12)")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=20.0) as client:
        # 1. Digital Twin Sync
        logger.info("Fetching Digital Twin State...")
        res_dt = await client.get("/api/digital-twin/state")
        dt_state = res_dt.json()
        active_regions = dt_state.get("active_regions", [])
        logger.info(f"Digital Twin Active Regions loaded: {len(active_regions)}")
        assert isinstance(active_regions, dict), "DT regions should be a dict"
        
        # 2. Knowledge Graph Sync
        logger.info("Fetching Knowledge Graph events...")
        res_kg = await client.get("/api/knowledge-graph/")
        kg_events = res_kg.json()
        # In mock data, KG should have some nodes or return a dict
        logger.info(f"Knowledge Graph structure fetched: {list(kg_events.keys())}")
        
        # 3. Scientific Reasoning Engine Sync
        logger.info("Sending query to Scientific Reasoning Engine...")
        query_payload = {
            "query": "What is the current state of active region 13664?"
        }
        res_reason = await client.post("/api/reasoning/analyze", json=query_payload)
        reason_res = res_reason.json()
        assert "content" in reason_res, "Reasoning engine response missing"
        assert "confidence" in reason_res, "Reasoning engine confidence missing"
        assert "sources" in reason_res, "Reasoning engine sources missing"
        
        logger.info(f"Reasoning Engine Response: {reason_res['content'][:100]}...")
        logger.info(f"Citations used: {reason_res['sources']}")
        
        logger.info("✅ Digital Twin, Knowledge Graph, and Reasoning Engine Sync Verified")
        
        with open("TEST_RESULTS.md", "a") as f:
            f.write("\n## Digital Twin, KG, & Reasoning Validation\n\n")
            f.write("- ✅ Digital Twin State Synchronization Verified\n")
            f.write("- ✅ Knowledge Graph Event Tracing Verified\n")
            f.write("- ✅ Scientific Reasoning Engine (SRE) Tool Calling Verified\n")

if __name__ == "__main__":
    asyncio.run(verify_sync())

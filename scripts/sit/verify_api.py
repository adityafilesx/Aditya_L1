import asyncio
import httpx
import time
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SIT.VerifyAPI")

BASE_URL = "http://127.0.0.1:8000"

ENDPOINTS = [
    {"method": "GET", "url": "/api/system/health"},
    {"method": "GET", "url": "/api/system/config"},
    {"method": "GET", "url": "/api/system/diagnostics"},
    {"method": "GET", "url": "/api/operations/telemetry"},
    {"method": "GET", "url": "/api/physics/summary"},
    {"method": "GET", "url": "/api/forecast/current"},
    {"method": "GET", "url": "/api/digital-twin/state"}, # assuming get
    {"method": "GET", "url": "/api/knowledge-graph/"},
    {"method": "POST", "url": "/api/reasoning/analyze", "payload": {
        "query": "Explain today's flare"
    }}
]

async def verify_api():
    logger.info("Starting API Validation (SIT Phase 11.5)")
    
    results = []
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
        for ep in ENDPOINTS:
            method = ep["method"]
            url = ep["url"]
            payload = ep.get("payload")
            
            logger.info(f"Testing {method} {url}...")
            start_time = time.time()
            
            try:
                if method == "GET":
                    response = await client.get(url)
                else:
                    response = await client.post(url, json=payload)
                
                latency = (time.time() - start_time) * 1000
                status = response.status_code
                
                if status == 200:
                    logger.info(f"✅ {method} {url} - {status} OK ({latency:.2f}ms)")
                    results.append({
                        "endpoint": f"{method} {url}",
                        "status": "PASS",
                        "code": status,
                        "latency_ms": latency,
                        "error": None
                    })
                else:
                    logger.error(f"❌ {method} {url} - {status} FAILED ({latency:.2f}ms)")
                    results.append({
                        "endpoint": f"{method} {url}",
                        "status": "FAIL",
                        "code": status,
                        "latency_ms": latency,
                        "error": response.text
                    })
                    
            except Exception as e:
                latency = (time.time() - start_time) * 1000
                logger.error(f"❌ {method} {url} - EXCEPTION: {e} ({latency:.2f}ms)")
                results.append({
                    "endpoint": f"{method} {url}",
                    "status": "ERROR",
                    "code": None,
                    "latency_ms": latency,
                    "error": str(e)
                })
                
    # Save results to an artifact report later, for now just print summary
    failures = [r for r in results if r["status"] != "PASS"]
    if failures:
        logger.warning(f"API Validation complete with {len(failures)} failures.")
    else:
        logger.info("API Validation complete. All endpoints PASS.")
        
    # Write report
    with open("TEST_RESULTS.md", "a") as f:
        f.write("\n## API Validation Results\n\n")
        f.write("| Endpoint | Status | Code | Latency |\n")
        f.write("|---|---|---|---|\n")
        for r in results:
            stat_icon = "✅" if r["status"] == "PASS" else "❌"
            f.write(f"| {r['endpoint']} | {stat_icon} {r['status']} | {r['code']} | {r['latency_ms']:.1f}ms |\n")
        
    return results

if __name__ == "__main__":
    asyncio.run(verify_api())

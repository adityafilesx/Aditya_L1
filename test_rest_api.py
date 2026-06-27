import urllib.request
import json

endpoints = [
    "/api/operations/telemetry",
    "/api/operations/physics",
    "/api/operations/models",
    "/api/system/health",
    "/api/features",
    "/api/features/store",
    "/api/models/registry",
    "/api/models/serving"
]

for ep in endpoints:
    url = f"http://localhost:8000{ep}"
    print(f"\n--- {ep} ---")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(json.dumps(data, indent=2)[:500] + "...")
    except Exception as e:
        print(f"Error: {e}")


from backend.api.main import app

for route in app.routes:
    print(route.path)

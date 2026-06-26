# Deployment Architecture

## Phase FE-6 Target Architecture

### Containerization
The entire monorepo will be packaged into a highly cohesive dockerized environment:
- **Frontend Container:** An Nginx or Caddy server serving the Vite-built static files (from `frontend/dist`).
- **Backend Container:** A Uvicorn/FastAPI server hosting the Python Intelligence Engine and REST endpoints.
- **Message Broker:** A Redis container facilitating pub/sub for WebSocket scalability and physics state-sharing across potential multiple backend workers.

### Continuous Integration (CI)
GitHub Actions (or GitLab CI) should define two primary matrix paths:
1. `path-filter: backend/**` → Triggers `pytest`, Flake8, and Backend Docker build.
2. `path-filter: frontend/**` → Triggers `npm run lint`, `npm run build`, and Frontend Docker build.

More detailed orchestration files will be introduced in the `/docker` directory shortly.

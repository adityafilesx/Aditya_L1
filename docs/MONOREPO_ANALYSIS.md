# Monorepo Analysis Report

## 1. Overview
This document analyzes the structural integration of the Aditya-L1 backend and frontend projects into a single enterprise monorepo. The goal is to establish a unified codebase that supports independent builds, while preparing for a shared contract and API service layer in Phase FE-5.

## 2. Architectures

### 2.1 Backend Architecture
- **Language/Environment:** Python 3.14+, `venv`-based dependency management.
- **Key Subsystems:**
  - `aditya_flare/`: Core decision engine, Multi-modal twin, AI components.
  - `physics_engine/`: FFT, Wavelets, Neupert effect, Thermodynamics.
  - `scripts/`: Data ingestion, training pipelines, daemons.
  - `tests/`: Automated `pytest` suite.
- **Execution Strategy:** Synchronous scripts and future asynchronous daemons via FastAPI. It runs independently of the frontend layer.

### 2.2 Frontend Architecture
- **Language/Environment:** TypeScript, Node.js, Vite, React 19.
- **Key Subsystems:**
  - `src/features/`: Domain-specific UI segments (`physics`, `mission`, `digitalTwin`, etc.).
  - `src/styles/`: Custom Design System using CSS Variables and Tailwind.
  - `src/services/` (Planned): API client layer.
- **Execution Strategy:** CSR (Client-Side Rendering) via React Router, executing exclusively in the browser.

## 3. Folder Structure

The newly adopted monorepo structure guarantees total isolation between Python and Node runtimes:
```
project-root/
├── backend/            # Python source, models, and scripts
├── frontend/           # React/Vite source, styles, and static assets
├── docs/               # Monorepo and architectural documentation
├── docker/             # Future containerization definitions
├── shared/             # Future shared schemas and API contracts
├── .env.example        # Root environment template
├── .gitignore          # Root git exclusion rules
├── LICENSE
└── README.md
```

## 4. Potential Conflicts & Risks

### 4.1 Duplicate Files
- **Documentation Overlap:** Both original projects had their own `README.md` and `DESIGN_SYSTEM.md`. 
  - *Resolution:* Consolidate high-level info into `project-root/README.md`. Move domain-specific docs to `docs/`.
- **Environment Variables:** Both backend (`.env`) and frontend (`.env` or `.env.local`) manage secrets independently.
  - *Resolution:* Root-level variables manage orchestration (e.g. docker-compose). Application-level variables stay isolated in `backend/` and `frontend/`.

### 4.2 Package Conflicts
- Python's `pip` and Node's `npm` operate in fundamentally different directories (`backend/venv` and `frontend/node_modules`).
- *Risk:* Running global linting or formatting tools (e.g., Prettier, Flake8) at the project root without careful `.ignore` files could cause cross-language parsing errors.

### 4.3 Build Conflicts
- CI/CD pipelines must be configured carefully to only trigger backend builds on `backend/` changes, and frontend builds on `frontend/` changes.
- *Risk:* A monorepo build script could unintentionally run `npm build` when only a python file changed, wasting compute time.

## 5. Future Integration Points (FE-5 & FE-6)

1. **Shared Types (`shared/types/`):** Python Pydantic models will correspond directly to TypeScript interfaces for DTOs.
2. **API Service Layer (`frontend/src/services/`):** Frontend React hooks will map to FastAPI REST endpoints and WebSockets defined in the backend.
3. **Container Orchestration (`docker/`):** A unified `docker-compose.yml` will launch the FastAPI backend, a web server (Nginx/Caddy) for the frontend, and Redis for pub/sub websocket management.

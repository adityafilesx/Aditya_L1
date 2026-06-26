# Development Guide

## Environment Setup

### 1. Root Orchestration
In Phase FE-5, a root `package.json` with `concurrently` (or a `Makefile`) will be provided to boot both environments seamlessly. For now, they must be started independently.

### 2. Frontend Local Server
```bash
cd frontend
npm install
npm run dev
# The site will be available at http://localhost:5173
```

### 3. Backend Local Environment
```bash
cd backend
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Run automated tests
pytest
# Start the AI decision engine daemon (example)
python scripts/run_operations_daemon.py
```

## Shared Folder Strategy
During the Service Integration Phase, you will heavily utilize the `shared/` directory to manage common resources:
- DTOs and Data Models (Typescript `Interfaces` ↔ Python `Pydantic`)
- Constants (e.g. `INSTRUMENT_THRESHOLDS`)
- Event schemas for WebSocket payloads.

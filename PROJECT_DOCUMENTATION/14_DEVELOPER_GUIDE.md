# 14. Developer Guide

This guide details onboarding instructions, local testing setup, and procedures for extending the codebases.

---

## 🛠️ System Prerequisites
*   **Operating System**: macOS (verified), Linux.
*   **Python**: Version 3.14+.
*   **Node.js**: Version 18+.

---

## 🔧 Local Development Bootstrapping

### 1. Backend Environment Setup
Navigate to `/backend` and create your python virtual environment:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Frontend Environment Setup
Navigate to `/frontend` and install Node dependencies:
```bash
cd ../frontend
npm install
```

### 3. Running Services
*   **Start Backend**:
    ```bash
    cd backend
    source venv/bin/activate
    uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
    ```
*   **Start Frontend**:
    ```bash
    cd frontend
    npm run dev
    ```

---

## 🔬 Running Test Suites

### 1. Automated System Integration Tests
Execute the custom verification suite from the project root:
```bash
# Verify API Response Schemas
python3 scripts/sit/verify_api.py

# Verify Data Ingestion Pipeline
python3 scripts/sit/verify_data_flow.py

# Verify Model Inference and Conformal Bounds
python3 scripts/sit/verify_models.py

# Verify WebSocket Live Streams
python3 scripts/sit/verify_streaming.py

# Verify Twin Sync Coordinates
python3 scripts/sit/verify_sync.py
```

---

## ➕ Adding a New API Endpoint

1.  **Define Route**: Add your path function in a router file (e.g. `backend/api/routes/physics.py`):
    ```python
    @router.get("/entropy")
    async def get_entropy():
        return {"entropy_score": app_state.latest_physics.shannon_entropy}
    ```
2.  **Mount Router**: Ensure the router is registered inside `backend/api/main.py`.

---

## 🧠 Adding a New AI Model

1.  **Module Creation**: Save your neural model definition inside `backend/aditya_flare/ai_engine/models/`.
2.  **Register Model**: Import and load your weights during gateway startup (`backend/api/main.py`), registering it to the dynamic `app_state` object.
3.  **Update Prediction Pipeline**: Edit `backend/aditya_flare/models/forecaster.py` to compile your model's outputs into the ensemble probability.

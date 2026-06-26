# Aditya-L1 Mission Control — Unified Data Ingestion Engine

![Aditya-L1 Mission Control](https://img.shields.io/badge/Status-Operational-success) ![License](https://img.shields.io/badge/License-ISRO_Internal-blue)

The **Aditya-L1 Mission Control** is a next-generation, real-time web platform designed to monitor, forecast, and analyze solar activity using data from India's Aditya-L1 solar observatory. It features a high-performance **Unified Data Ingestion Engine** that processes live telemetry, physical models, and AI-driven forecasts, streaming them via WebSockets to a React-based Operations Center.

---

## 🌟 Key Features

*   **Real-Time Telemetry Streaming**: High-frequency processing of Soft X-Ray (SoLEXS) and Hard X-Ray (HEL1OS) fluxes.
*   **AI Decision & Forecasting Engine**: Autonomous prediction of solar flares (M-Class, X-Class) using an ensemble of models (XGBoost, Temporal-CN, Transformer-S, Hybrid-Alpha) with conformal confidence scoring.
*   **Physics Engine**: Derives critical parameters like Neupert Score, Coronal Temperature (MK), and Emission Measures in real-time.
*   **Solar Digital Twin**: Monitors active regions and provides real-time similarity scoring and field delta tracking.
*   **Autonomous Alerting**: A 3-state escalation machine (NOMINAL → WATCH → ALERT) that automatically recommends operational mode changes (e.g., SUIT High-Cadence Sequence).
*   **Interactive Workstations**: Includes Spectral Analysis, Sensor Inspector, and Mission Timeline dashboards.

---

## 🏗️ Architecture

The platform is built on a modern, decoupled architecture:

*   **Backend (`/backend`)**: FastAPI, Python 3.10+, `asyncio` Pub/Sub Event Bus (`MissionBus`), Pydantic models, and WebSocket streaming.
*   **Frontend (`/frontend`)**: React 19, Vite, TypeScript, Zustand (`streamStore` for high-frequency state management), Tailwind CSS, and Plotly.js for time-series visualization.

---

## 🚀 Installation & Download Guide

This guide covers setup for **macOS**, **Linux**, and **Windows**.

### Prerequisites (All OS)

Before installing, ensure you have the following installed on your system:
1.  **Python 3.10 or higher**: [Download Python](https://www.python.org/downloads/)
2.  **Node.js 18 or higher** (includes `npm`): [Download Node.js](https://nodejs.org/)
3.  **Git**: [Download Git](https://git-scm.com/downloads)

### Step 1: Download the Repository

Open your terminal or command prompt and clone the repository:

```bash
git clone https://github.com/your-org/aditya-l1-mission-control.git
cd "aditya-l1-mission-control"
```

---

### Step 2: Backend Setup (FastAPI)

The backend requires Python dependencies to run the API server and the real-time simulation generator.

#### For macOS & Linux:
```bash
cd backend
# Create a virtual environment
python3 -m venv venv
# Activate the virtual environment
source venv/bin/activate
# Install API dependencies
pip install -r requirements-api.txt
# (Optional) Install full ML/Data dependencies if running model training
pip install -r requirements.txt
cd ..
```

#### For Windows (Command Prompt / PowerShell):
```cmd
cd backend
:: Create a virtual environment
python -m venv venv
:: Activate the virtual environment
venv\Scripts\activate
:: Install API dependencies
pip install -r requirements-api.txt
:: (Optional) Install full ML/Data dependencies if running model training
pip install -r requirements.txt
cd ..
```

---

### Step 3: Frontend Setup (React/Vite)

The frontend is a Vite-powered React application.

#### For All OS (macOS / Linux / Windows):
```bash
cd frontend
# Install Node dependencies
npm install
cd ..
```

---

## 🏃‍♂️ Running the Application

You need to run both the backend and frontend simultaneously in separate terminal windows.

### Terminal 1: Start the Backend

#### macOS & Linux:
```bash
cd backend
source venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

#### Windows:
```cmd
cd backend
venv\Scripts\activate
uvicorn api.main:app --host 0.0.0.0 --port 8000
```
*The backend API and WebSocket stream will be available at `ws://localhost:8000/ws/live`.*

### Terminal 2: Start the Frontend

#### All OS:
```bash
cd frontend
npm run dev
```

*The frontend application will start on **`http://localhost:5173`**. Open this URL in your web browser (Chrome, Edge, or Firefox recommended).*

---

## 📁 Project Structure

```text
Unified Data Ingestion Engine/
│
├── backend/                  # Python FastAPI Server
│   ├── api/                  # REST and WebSocket endpoints
│   ├── events/               # MissionStateGenerator, Pub/Sub Bus, Models
│   ├── reasoning/            # AI Reasoning and Workflow Engine
│   ├── physics_engine/       # Core physics calculations
│   └── requirements-api.txt  # Core backend dependencies
│
├── frontend/                 # React 19 + Vite UI
│   ├── src/
│   │   ├── app/              # Router and App Providers
│   │   ├── features/         # Page components (Nowcasting, Forecasting, etc.)
│   │   ├── realtime/         # WebSocket manager (socket.ts) & Zustand store
│   │   └── design-system/    # Reusable UI components
│   └── package.json          # Node dependencies
│
└── PROJECT_DOCUMENTATION/    # Architecture & Phase documentation
```

---

## 🛠️ Troubleshooting

*   **"System Offline" / "Waiting for live data handshake"**: Ensure the backend is running. The frontend relies on the WebSocket connection to port 8000. If the backend restarts, the frontend will automatically attempt to reconnect.
*   **Port 8000 / 5173 is in use**: If another process is using these ports, you can specify different ports. For FastAPI: `uvicorn api.main:app --port 8080`. For Vite: `npm run dev -- --port 3000`. Update `.env` variables if you change default ports.

---
*Developed for the Aditya-L1 Mission Operations Team.*

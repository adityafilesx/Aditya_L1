# Aditya-L1 Space Weather Intelligence Platform
## Technical Encyclopedia & Mission Documentation

Welcome to the central technical documentation index for the **Aditya-L1 Space Weather Intelligence Platform**. This encyclopedia serves as the definitive reference manual for system architecture, physics engines, neural networks, frontend interfaces, and operational procedures. It is designed to enable future researchers, software engineers, and ISRO scientists to maintain and expand the platform autonomously.

---

## 📚 Documentation Chapters

| Chapter | Document Title | Description |
|:---|:---|:---|
| **01** | [01_PROJECT_OVERVIEW.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/01_PROJECT_OVERVIEW.md) | Mission vision, objectives, scientific motivation, and platform constraints. |
| **02** | [02_COMPLETE_SYSTEM_ARCHITECTURE.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/02_COMPLETE_SYSTEM_ARCHITECTURE.md) | End-to-end architecture diagrams, layers, and Mermaid data flows. |
| **03** | [03_REPOSITORY_GUIDE.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/03_REPOSITORY_GUIDE.md) | Directory structure, module ownership, and repository dependency mapping. |
| **04** | [04_BACKEND_DOCUMENTATION.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/04_BACKEND_DOCUMENTATION.md) | In-depth technical breakdown of all Python backend modules, classes, and workflows. |
| **05** | [05_FRONTEND_DOCUMENTATION.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/05_FRONTEND_DOCUMENTATION.md) | Breakdown of frontend views: Overview, Operations, Physics, Twin, Graph, and SRE UI. |
| **06** | [06_ENGINE_DOCUMENTATION.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/06_ENGINE_DOCUMENTATION.md) | Mathematical and algorithmic descriptions of all 11 core background engines. |
| **07** | [07_AI_MODEL_DOCUMENTATION.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/07_AI_MODEL_DOCUMENTATION.md) | Neural network architectures (Transformer, TCN), XGBoost, and Conformal Predictor. |
| **08** | [08_FEATURE_ENCYCLOPEDIA.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/08_FEATURE_ENCYCLOPEDIA.md) | Complete reference of user features, UI layouts, backend APIs, and error handling. |
| **09** | [09_DATA_FLOW_DOCUMENTATION.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/09_DATA_FLOW_DOCUMENTATION.md) | Unified telemetry-to-reasoning data flow pipeline across all systems. |
| **10** | [10_API_REFERENCE.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/10_API_REFERENCE.md) | Comprehensive API endpoints, payloads, JSON schemas, and response profiles. |
| **11** | [11_FRONTEND_COMPONENT_GUIDE.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/11_FRONTEND_COMPONENT_GUIDE.md) | Reusable React component documentation, properties, and usage. |
| **12** | [12_DATABASE_AND_MODELS.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/12_DATABASE_AND_MODELS.md) | Static assets, model checkpoints, scale parameters, and database schemas. |
| **13** | [13_USER_MANUAL.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/13_USER_MANUAL.md) | User manual for payload operators, researchers, and mission directors. |
| **14** | [14_DEVELOPER_GUIDE.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/14_DEVELOPER_GUIDE.md) | Local environment setup, coding guidelines, testing suites, and onboarding. |
| **15** | [15_DEPLOYMENT_GUIDE.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/15_DEPLOYMENT_GUIDE.md) | Containerization, environment variables, reverse proxies, and production architecture. |
| **16** | [16_TESTING_AND_VALIDATION.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/16_TESTING_AND_VALIDATION.md) | Testing frameworks, SIT validation results, and historical flare backtesting. |
| **17** | [17_TROUBLESHOOTING_GUIDE.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/17_TROUBLESHOOTING_GUIDE.md) | Incident reports, network disconnect recoveries, and known issues. |
| **18** | [18_GLOSSARY.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/18_GLOSSARY.md) | Scientific glossary defining astrophysics, solar physics, and system engineering terms. |
| **19** | [19_FUTURE_ROADMAP.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/19_FUTURE_ROADMAP.md) | Future extensions, including PINNs, GNNs, GraphRAG, and foundation models. |
| **20** | [20_COMPLETE_FEATURE_MATRIX.md](file:///Users/aditya1981/Documents/Unified%20Data%20Ingestion%20Engine/PROJECT_DOCUMENTATION/20_COMPLETE_FEATURE_MATRIX.md) | High-level master matrix of system readiness and feature connections. |

---

## 🛠 Platform At-A-Glance
* **Backend Stack**: Python 3.14+, FastAPI, Uvicorn, LangGraph, PyTorch, SymPy, NumPy, Pandas, Scikit-learn.
* **Frontend Stack**: TypeScript, React 19, Vite, Zustand, Tailwind CSS, Three.js / React Three Fiber, React Flow, Plotly.js.
* **Core Goal**: Connect solar instrument telemetry (SoLEXS, HEL1OS, GOES) with physics engines and transformer forecasting algorithms to provide real-time nowcasts, multi-horizon predictions (up to 6 hours ahead), and interactive solar models for space weather operations.

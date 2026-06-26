# 02. Complete System Architecture

This document details the software architecture, data flow paths, and structural layouts of the Aditya-L1 Space Weather Intelligence Platform.

---

## 🏗 End-to-End System Architecture

The platform follows a split-environment, decoupled architecture:
1.  **FastAPI Backend Gateway**: Orchestrates background workers, maintains in-memory states, processes queries, and runs the AI/Physics pipelines.
2.  **Vite/React Frontend**: Serves as a pure presentation layer, consuming live data streams via WebSockets and REST APIs, rendering interactive visualizations with Three.js and Plotly.

```mermaid
graph TD
    %% Spacecraft & External Instruments
    subgraph Spacecraft [Telemetry Sources]
        AL1[Aditya-L1 Spacecraft]
        SOLEXS[SoLEXS Soft X-rays]
        HEL1OS[HEL1OS Hard X-rays]
        GOES[GOES XRS-B Flux]
    end

    %% Ingestion & Processing Layer
    subgraph Ingestion [Backend Ingestion & Processing]
        IB[Mission Event Bus]
        PP[Physics Feature Pipeline]
        AE[AI Forecast Engine]
        DTB[Digital Twin Backend]
        KGB[Knowledge Graph Engine]
    end

    %% Gateway & Streaming
    subgraph Gateway [API Gateway & Streaming]
        API[FastAPI REST Router]
        WS[WebSocket Manager /ws/live]
        SRE[Scientific Reasoning Engine]
    end

    %% Presentation Layer
    subgraph Presentation [React Frontend Clients]
        WEB[Vite Dev Web App]
        DTF[Three.js Solar Twin UI]
        KGF[React Flow Knowledge Graph]
        AIS[AI Scientist Chat UI]
    end

    %% Data connections
    AL1 --> |Raw Downlink| SOLEXS & HEL1OS
    SOLEXS & HEL1OS & GOES --> |CSV/Fits/API| IB
    IB --> |Telemetry Stream| PP
    PP --> |Physics Vectors| AE
    AE --> |Forecast Results| DTB & KGB & SRE
    DTB --> |3D Mapping Data| WS
    KGB --> |RDF/Network States| WS
    WS --> |Live JSON Packets| WEB
    API --> |HTTP REST endpoints| WEB
    SRE --> |Reasoning / Context| API
    WEB --> DTF & KGF & AIS
```

---

## 🗂 Layered Architecture Breakdown

The codebase is organized into five logical tiers:

```
+-------------------------------------------------------------+
|                     PRESENTATION TIER                       |
|  React 19, Vite, Three.js, React Flow, Plotly.js, Zustand   |
+-------------------------------------------------------------+
                              | (REST / WebSockets)
                              v
+-------------------------------------------------------------+
|                       GATEWAY TIER                          |
|         FastAPI REST Routers, WebSocket Endpoint            |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                      REASONING TIER                         |
|   Scientific Reasoning Engine (SRE), LangGraph, Router      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                   ANALYTICS & CORE TIER                     |
|  Physics Pipeline (wavelets, thermodynamics), Ensemble AI   |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                     INGESTION TIER                          |
|      Mission Event Bus (PubSub), Background Generator       |
+-------------------------------------------------------------+
```

---

## 📡 Live Streaming Pipeline Sequence

This diagram shows how a raw telemetry packet propagates from ingestion to the UI in real time:

```mermaid
sequenceDiagram
    autonumber
    participant Source as Telemetry Source (GOES/SoLEXS)
    participant Bus as Mission Event Bus
    participant Physics as Physics Engine
    participant Forecast as AI Forecast Engine
    participant KG as Knowledge Graph
    participant WS as WebSocket Endpoint
    participant UI as React Dashboard

    Source->>Bus: Publish Raw Telemetry (1s cadence)
    Bus->>WS: Forward "TELEMETRY" type to WS Clients
    WS->>UI: Stream Telemetry packet
    Bus->>Physics: Process Raw Flux (5s cadence)
    Physics->>Physics: Extract wavelets, EM, Temperature
    Physics->>Bus: Publish Physics Vector
    Bus->>WS: Forward "PHYSICS" type to WS Clients
    WS->>UI: Stream Physics packet
    Bus->>Forecast: Execute Multi-Horizon Inference (5s cadence)
    Forecast->>Forecast: XGBoost + Transformer Ensemble
    Forecast->>Bus: Publish Prediction Probability & Conformal Bounds
    Bus->>WS: Forward "FORECAST" type to WS Clients
    WS->>UI: Stream Forecast packet
    Forecast->>KG: Insert Flare node and link parameters
    KG->>Bus: Publish Updated Graph Topology
    Bus->>WS: Forward "SYSTEM" & "MISSION_STATE"
    WS->>UI: Stream Mission State updates
```

---

## 🧬 Scientific Reasoning Engine (SRE) Architecture

The AI Scientist feature runs on a dynamic multi-agent context assembly engine:

```mermaid
flowchart TD
    Q[User Prompt: e.g. "Explain today's flare"] --> P[SRE Planner/Router]
    P --> |Query| CB[Context Builder]
    CB --> |Read State| AS[App State Reference]
    CB --> |Read Graph| KG[Knowledge Graph Store]
    AS --> |Current Physics & Forecast| Context[Assembled Context Object]
    KG --> |Historical Analogs| Context
    Context --> |Context + Prompt| R[Reasoner LLM/Model]
    R --> |Stream Response| WS[WebSocket/Response Chunk]
    WS --> UI[Research Workspace Chat Panel]
```

Every arrow in this diagram represents:
*   **Prompt Entry**: The user inputs a query via the `ResearchConversation.tsx` component.
*   **Context Retrieval**: `ContextBuilder` inspects `app_state` (which holds active values for temperature, entropy, emission measure, and ensemble predictions) and queries `KnowledgeGraph` for linked active region states.
*   **Response Generation**: The accumulated telemetry and historical context are combined to form the system prompt sent to the LLM router, streaming Markdown and LaTeX formulas back to the client.

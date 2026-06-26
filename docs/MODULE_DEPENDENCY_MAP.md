# Module Dependency Map — Aditya-L1 Space Weather Platform

This document outlines the dependencies and import relations of the core packages within the platform.

---

## 1. Dependency Graph

Below is the visualization of the data and compute paths across modules:

```mermaid
graph TD
    %% Base Data Ingestion
    Processing[aditya_flare.processing] --> Dataset[aditya_flare.models.dataset]
    Dataset --> Calibration[aditya_flare.calibration]
    
    %% Compute Branches
    Calibration --> Physics[physics_engine]
    Calibration --> AI[aditya_flare.ai_engine]
    
    %% Physics Engine Imports
    subgraph Physics_Modules [physics_engine Modules]
        Physics --> Thermodynamics[physics_engine.thermodynamics]
        Physics --> Spectral[physics_engine.spectral]
        Physics --> Wavelets[physics_engine.wavelets]
        Physics --> Neupert[physics_engine.neupert]
    end
    
    %% AI Engine Imports
    subgraph AI_Modules [aditya_flare.ai_engine Modules]
        AI --> Registry[aditya_flare.ai_engine.registry]
        AI --> Hybrid[aditya_flare.ai_engine.hybrid_ensemble]
        AI --> Predict[aditya_flare.ai_engine.predict]
        Predict --> Explain[aditya_flare.ai_engine.explainability]
    end
    
    %% Fusion Engine
    Explain --> MultiModal[aditya_flare.multi_modal]
    Thermodynamics --> MultiModal
    
    subgraph Multi_Modal_Modules [aditya_flare.multi_modal Modules]
        MultiModal --> CrossAttention[aditya_flare.multi_modal.fusion.cross_modal]
        MultiModal --> Twin[aditya_flare.multi_modal.digital_twin.state_tracker]
        MultiModal --> Graph[aditya_flare.multi_modal.knowledge_graph.event_graph]
    end
    
    %% Decision & Control Engine
    CrossAttention --> Decision[aditya_flare.decision]
    Twin --> Decision
    Graph --> Decision
    
    subgraph Decision_Modules [aditya_flare.decision Modules]
        Decision --> StateMach[aditya_flare.decision.state_machine]
        Decision --> Alerts[aditya_flare.decision.alert_manager]
        Decision --> Drift[aditya_flare.decision.drift_monitor]
        Decision --> Recomm[aditya_flare.decision.recommendation]
    end
```

---

## 2. Core Modules Architecture

1.  **Ingestion & In-Memory Pipeline (`aditya_flare.processing` & `dataset`):**
    *   No external package imports besides `pandas`, `numpy`, and `pathlib`.
    *   Responsible for converting raw Parquet streams into aligned multi-column datasets.
2.  **Physics Analytics (`physics_engine`):**
    *   Purely scientific NumPy/SciPy operations.
    *   Provides feature matrix vectors to the ML pipeline.
3.  **Machine Learning Engine (`aditya_flare.ai_engine`):**
    *   Depends on `scikit-learn`, `xgboost`, `lightgbm`, and `torch`.
    *   Loads models registered under `registry.py` and returns probability vectors.
4.  **Decision Controls (`aditya_flare.decision`):**
    *   Consumes the physics metrics and AI model probability outputs.
    *   Maintains the spacecraft state machine.
5.  **Multi-Modal Fusion (`aditya_flare.multi_modal`):**
    *   Acts as the aggregator connecting physical states (digital twin), mission logs (knowledge graph), and models.

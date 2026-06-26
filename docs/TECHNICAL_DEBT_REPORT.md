# Technical Debt Report — Aditya-L1 Space Weather Platform

This document catalogs code smells, architectural vulnerabilities, hardcoded values, deprecated scripts, testing deficits, and deployment bottlenecks across the Aditya-L1 Space Weather Intelligence Platform.

---

## 1. Hardcoded Values & Environment Traps

The codebase contains numerous absolute paths locked to the developer's local username (`aditya1981`) and dynamic Gemini Conversation IDs. This makes the system fragile when deployed on other nodes or CI systems.

### 1.1 Local Path Configurations (Traps)
*   **`scripts/predict_nowcast.py#L79`**: Hardcoded artifact path targeting a specific sandbox run:
    ```python
    artifact_dir = "/Users/aditya1981/.gemini/antigravity-ide/brain/5a27e10c-eb48-466f-a4bc-32c7071db0fe"
    ```
*   **`scripts/predict_forecast.py#L87`**: Points to a different conversation folder:
    ```python
    artifact_dir = "/Users/aditya1981/.gemini/antigravity-ide/brain/ead5211d-dfba-45f4-a3a2-adaf18c4ec59"
    ```
*   **`libs/chspec/readTable.h#L29`**: Hardcoded C macro linking compiled libraries to user workspace:
    ```c
    #define CHSPEC_TABLEPATH "/Users/aditya1981/Documents/Unified Data Ingestion Engine/libs/chspec/tables/"
    ```
*   **`libs/chspec/lpack_chspec.cxx#L28`**: Hardcoded path to a temporal subagent compilation directory:
    ```c++
    ("/Users/aditya1981/.gemini/antigravity-ide/brain/ead5211d-dfba-45f4-a3a2-adaf18c4ec59/chspec_build/lmodel_chspec.dat");
    ```
*   **`scripts/generate_flare_images.py`**, `scripts/visualize_20240212_flare.py`, `scripts/extract_time_resolved_params.py`: Multiple instances where spectra files, calibration response matrices (`.rmf`), and effective area files (`.arf`) are hardcoded to `/Users/aditya1981/Downloads/solexs_tools-1.1/...` or `/Users/aditya1981/Documents/Solex dataset`.

---

## 2. Code Duplication & Overlap

*   **Spectral Param Extraction Scripts:** `scripts/extract_time_resolved_params.py` and `scripts/extract_flare_params.py` share roughly 80% of their logic. Both script sets instantiate Heasoft/Xspec commands, import custom C bindings, parse identical fits/pi directories, and output CSV data columns.
*   **Aesthetic Visualization Scripts:** The files `scripts/visualize_advanced_fit.py`, `scripts/visualize_flare_spectra.py`, and `scripts/visualize_20240212_flare.py` contain redundant spectral plot parameters, label mappings, and canvas setup functions.

---

## 3. Architecture & Performance Issues

### 3.1 Synchronous Xspec Dependencies
*   Solar flare spectral diagnostic tools (Heasoft Xspec wrapper) run as synchronous, blocking sub-processes. During intense flare occurrences where time-resolved analysis is run at 1-minute steps, these calculations cause substantial pipeline backpressure (~30 to 45 seconds per step).
*   **Remedy:** Decouple spectral fitting into an asynchronous queue (e.g., Celery, Redis) or convert custom C++ code into pre-compiled Python binaries.

### 3.2 In-Memory Graph Nodes
*   The Knowledge Graph module (`aditya_flare/multi_modal/knowledge_graph/event_graph.py`) stores active regions and solar event connections using basic in-memory networkx structures. There is no persistent backend database. When the process restarts, all node relationships must be completely rebuilt from scratch.

---

## 4. Testing & Verification Deficits

While the core modules pass unit verification (`pytest` checks pass 29/29), several critical areas remain untested:
*   **Deep Learning Models:** There are no active assertions verifying learning behaviors or gradient ranges inside `aditya_flare/ai_engine/models/transformer.py` or `tcn.py`.
*   **Decision Engine Actions:** The alert dispatcher state transitions are verified with simulated inputs but lack integration assertions mapping to live hardware loop overrides.
*   **Drift Monitor Verification:** No unit tests are configured to validate Kolmogorov-Smirnov drift alarms or feature distribution checks under realistic noise.

---

## 5. Security & Secret Exposure Vectors

*   **Environment Settings:** The app currently relies on hardcoded variables inside script headers. There is no centralized configuration loader (like `python-dotenv` or dynamic OS environment checks) for local system API keys or paths.
*   **Authentication API Absence:** The Python API layer lacks token validation, query rate limits, or spacecraft operator authentication mechanisms.

---

## 6. Risk Assessment Matrix

| Vector | Risk Tier | Impact | Description | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Path Fragility** | 🔴 Critical | High | Docker build or external server startup will fail due to missing `/Users/aditya1981` folders. | Migrate paths to configuration schemas under `aditya_flare/config/`. Use path resolving via `pathlib.Path(__file__)`. |
| **Xspec Blocking** | 🟡 Medium | High | High-cadence pipeline execution delays state machine notifications during solar storms. | Migrate fitting computations to background workers. |
| **Graph Volatility**| 🟡 Medium | Low | Knowledge graph updates are lost upon process crashes. | Bind NetworkX graphs to a lightweight SQLite database or local JSON serialization wrapper. |
| **Secret Gaps** | 🟡 Medium | Medium | Missing credentials manager will block migration to public hosting platforms. | Configure a `.env` template and set up Python's `dotenv` loader. |

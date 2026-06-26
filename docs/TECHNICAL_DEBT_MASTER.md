# Technical Debt Master Registry — Aditya-L1 Platform

This document consolidates and prioritizes all architectural limitations, code quality issues, configuration vulnerabilities, and test coverage gaps across the Aditya-L1 Space Weather Intelligence Platform.

---

## 1. High Severity (Critical Refactoring Targets)

### 1.1 Local Path Traps
*   **Vulnerability:** Core prediction scripts, visualization files, and C++ header targets contain hardcoded local folders pointing to `/Users/aditya1981/...` and dynamic sandbox IDs.
*   **Impact:** Running this codebase on standard Docker instances or different host accounts causes execution failures due to missing local directories.
*   **Resolution Strategy:**
    1.  Add centralized file system paths in `aditya_flare/config/settings.yaml`.
    2.  Use `pathlib.Path(__file__).parent` references for relative project paths.

### 1.2 Missing Production API Wrappers
*   **Vulnerability:** Interface commands (data resampler, physics engine, state machine, forecast runs) are written as local in-process Python calls.
*   **Impact:** The system cannot serve external requests or communicate with web client interfaces.
*   **Resolution Strategy:** Wrap the interface codebases in a FastAPI router layer.

---

## 2. Medium Severity (Performance & Logic Enhancements)

### 2.1 Blocking Xspec Processes
*   **Vulnerability:** Physics spectral modeling wrappers execute standard Heasoft XSPEC command strings synchronously.
*   **Impact:** Running time-resolved fits over large telemetry blocks blocks the main thread, introducing delays (~30s) that can delay alert notifications.
*   **Resolution Strategy:** Move heavy calculations to background task queues (e.g. Celery / Redis).

### 2.2 Volatile In-Memory Graph Nodes
*   **Vulnerability:** Event graph relationships are generated using in-memory NetworkX models.
*   **Impact:** A service restart clears all nodes and edges, requiring a full historical telemetry rebuild.
*   **Resolution Strategy:** Store relations in an SQLite database.

### 2.3 SUIT Alignment Verification Gaps
*   **Vulnerability:** SUIT UV telemetry coordinates are loaded, but automatic solar disk centering and limb alignment logic are not tested.
*   **Impact:** Visual features may be misaligned in multi-modal models.
*   **Resolution Strategy:** Add validation tests for SUIT coordinates.

---

## 3. Low Severity (Quality & Testing Polish)

### 3.1 Gaps in Deep Model Assertions
*   **Vulnerability:** Unit tests focus on telemetry loaders and basic physics modules, but do not test deep models like TCN and Transformer.
*   **Impact:** Code changes could cause gradient issues or output dimension shifts without throwing testing errors.
*   **Resolution Strategy:** Add test scripts with mocked inputs for all model architectures under `aditya_flare/ai_engine/models/`.

### 3.2 Scattered System Logging
*   **Vulnerability:** Log outputs are handled on an ad-hoc basis in script blocks.
*   **Impact:** Lack of standardized logger configuration formats across the application.
*   **Resolution Strategy:** Set up unified rotating logger outputs under the config module.

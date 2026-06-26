# Dependency Audit & Report

## 1. Overview
This document catalogs the dependencies utilized across the Aditya-L1 Monorepo, identifying the Python (Backend) and Node.js (Frontend) ecosystems. It highlights version conflicts, redundancies, recommended updates, and potential security considerations.

## 2. Python Packages (Backend)

The `backend/requirements.txt` defines the scientific and AI computing stack.

### Key Dependencies:
- **Core Math/Data:** `numpy>=1.21`, `pandas>=1.5`, `scipy>=1.7`
- **Machine Learning:** `xgboost`, `lightgbm`, `scikit-learn`, `imbalanced-learn`
- **Visualization:** `matplotlib>=3.5`, `seaborn`, `plotly`
- **Space Science:** `astropy>=5.0`, `netCDF4>=1.6.0`, `cftime>=1.6.0`
- **Legacy UI / Observability:** `streamlit`, `mlflow`

### Analysis & Recommendations:
- **Redundancy (Streamlit):** The `streamlit` package is still listed but the legacy UI has been removed. *Recommendation:* Remove `streamlit` from requirements to reduce the environment size and attack surface.
- **Version Pinning:** Packages like `xgboost` and `scikit-learn` lack strict version pinning (e.g., `==1.3.0`). *Recommendation:* Freeze dependencies using `pip-compile` or `Poetry` to guarantee reproducible production builds.
- **Security:** Ensure `numpy` and `pandas` are updated to patch recent known CVEs in data parsing libraries.

## 3. Node Packages (Frontend)

The `frontend/package.json` defines the React 19 application stack.

### Key Dependencies:
- **Framework:** `react^19.1.0`, `react-dom^19.1.0`, `vite^6.3.5`
- **Routing & State:** `react-router-dom^7.6.2`, `@tanstack/react-virtual^3.14.3`
- **3D / Visualization:** `three^0.185.0`
- **Styling:** `tailwindcss^3.4.17`, `postcss^8.5.6`, `autoprefixer^10.4.21`
- **Tooling:** `typescript~5.8.3`, `eslint^9.29.0`

### Analysis & Recommendations:
- **Modern Stack Validation:** The stack is highly modern (React 19, React Router 7, Vite 6). No major legacy technical debt is present.
- **Redundancy:** There are no obvious duplicate libraries (e.g., both Moment.js and date-fns are absent, meaning native `Intl` or standard JS dates are likely being used).
- **Security:** `npm audit` should be run in CI. `react-error-boundary` is used, which correctly catches render-phase exceptions, improving resilience.

## 4. Cross-Ecosystem Analysis

### 4.1 Version Conflicts
- Since the two ecosystems (Python and JS) execute in completely isolated environments, there are **no direct dependency conflicts**.
- *Note on Plotly:* The backend uses Python `plotly` to generate visual reports. The frontend relies on native React components or D3/Three.js rather than rendering backend-generated HTML blobs. This is the correct separation of concerns.

### 4.2 Recommended Updates (Monorepo Tooling)
To effectively manage this repository in the future, the following tools should be evaluated:
- **Husky & Lint-Staged:** To enforce `eslint` on `frontend/` and `flake8/black` on `backend/` during git pre-commits.
- **Concurrently:** For developers to run both `npm run dev` and `python scripts/run_operations_daemon.py` using a single command from the root.

## 5. Security Summary
- **Backend:** High priority to remove `streamlit` and strictly pin AI package versions to prevent supply-chain poisoning.
- **Frontend:** Continual execution of `npm audit` to catch nested dependencies in `vite` and `three.js`.
- **Secrets Management:** Ensure that neither `backend/.env` nor `frontend/.env` are tracked by git.

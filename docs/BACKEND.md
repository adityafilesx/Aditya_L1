# Backend Architecture

## Stack
- **Language:** Python 3.14+
- **Math/Sci:** NumPy, Pandas, SciPy, Astropy
- **AI/ML:** XGBoost, LightGBM, scikit-learn
- **API (Future):** FastAPI
- **Testing:** Pytest

## Folder Structure
- `aditya_flare/` - Real-time AI inference and digital twin modules.
- `physics_engine/` - Thermodynamic simulations and FFT calculations.
- `scripts/` - Automated pipelines, model training, and data ingestion.
- `tests/` - Comprehensive unit and integration test suite.
- `data/` - Datasets and model checkpoints.

## Execution
To run the backend tests independently:
```bash
cd backend/
source venv/bin/activate
pytest
```

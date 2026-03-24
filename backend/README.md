# Backend scaffold (FastAPI)

This folder is a production-foundation scaffold for a modular monolith backend.

## Notes
- Existing MVP orchestration is preserved under `app/orchestration/math_agent_backend/`.
- API routes are intentionally skeleton implementations.
- Streamlit app remains untouched at repo root (`math_agent_ui/`).

## Run (scaffold)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

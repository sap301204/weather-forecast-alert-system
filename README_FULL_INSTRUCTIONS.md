## Full setup (local)

1. Create venv & install:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Init DB & seed:
   python - <<PY
from src.db_utils import init_db
init_db()
PY
   sqlite3 db/weather.db < db/seed.sql

3. Refresh data (one-off):
   python jobs/refresh.py

4. Start backend:
   uvicorn api.app:app --reload

5. Visit:
   - API UI: http://127.0.0.1:8000/docs
   - Streamlit demo: run `streamlit run web/streamlit_app.py`
   - Frontend (Next.js): run `cd frontend && npm install && npm run dev` or use docker-compose

## Using Docker Compose (production-ish)
Make sure docker is installed. Then:
  docker-compose build
  docker-compose up -d

This will run the API and frontend (Next.js). Seed the DB before starting or mount a pre-initialized db folder to ./db.

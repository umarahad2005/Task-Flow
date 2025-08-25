# TaskFlow

Small task manager (Flask + SQLite) — a compact, deployable code sample to demonstrate backend, API design, and simple frontend.

## Features
- RESTful API for tasks (CRUD)
- Tiny single-file frontend (vanilla JS)
- SQLite with SQLAlchemy
- Tests with pytest

## Run locally
1. Create venv & install:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Initialize DB (first run):
   ```bash
   export FLASK_APP=run.py
   flask shell -c "from app import db; db.create_all()"
   ```

3. Run:
   ```bash
   python run.py
   # open http://127.0.0.1:5000
   ```

4. Run tests:
   ```bash
   pytest -q
   ```
# Task-Flow

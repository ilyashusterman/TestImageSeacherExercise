# Makefile

# Backend initialization and run commands
init_backend:
	python3.12 -m venv .venv
	. .venv/bin/activate && pip install -r backend/requirements.txt

run_backend:
	. .venv/bin/activate && python backend/api.py

# Frontend initialization and run commands
init_frontend:
	cd frontend && npm install

run_frontend:
	cd frontend && npm start

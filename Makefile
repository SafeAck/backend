BACKEND_PORT ?= 8000

test:
	@pytest -s -v

devserver:
	@uvicorn safeack_backend.api --reload

start:
	@gunicorn safeack_backend.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${BACKEND_PORT} --bind [::]:${BACKEND_PORT} --access-logfile - --error-logfile - --capture-output
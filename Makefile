test:
	@pytest -s -v

start:
	@gunicorn -c gunicorn.conf.py safeack_backend.api:app
from os import environ
from multiprocessing import cpu_count
from dotenv import load_dotenv
from gunicorn import __main__

load_dotenv(".env")

# load vars
ENV: str = environ.get("ENV", "PRODUCTION")
DEV_ENV: bool = True if ENV in ["LOCAL", "DEV_ENV"] else False

if DEV_ENV:
    PORT = 8080
    WORKERS = 2
    RELOAD = True
    ACCESS_LOG = "-"
    ERROR_LOG = "-"
else:
    PORT = 8000
    WORKERS = cpu_count() * 2 + 1
    RELOAD = False
    ACCESS_LOG = "/var/log/gunicorn/access.log"
    ERROR_LOG = "/var/log/gunicorn/error.log"


# config: https://docs.gunicorn.org/en/latest/settings.html
bind = [f"localhost:{PORT}"]
wsgi_app = "safeack_backend.api:app"
proc_name = "safeack_backend"

workers = WORKERS
worker_class = "uvicorn.workers.UvicornWorker"
reload = RELOAD
reload_engine = "auto"

accesslog = ACCESS_LOG
errorlog = ERROR_LOG
capture_output = True

max_requests = 1000
preload_app = True

from uvicorn import run
import importlib.resources


def get_installation_dir():
    try:
        # For non-editable installation
        return importlib.resources.files('safeack_backend')
    except ImportError:
        # For editable installation (pip install -e .)
        return importlib.resources.files('.')


def start():
    installation_dir = get_installation_dir()
    run(
        app='safeack_backend.api:app',
        host="0.0.0.0",
        port=8000,
        workers=2,
        reload=True,
        reload_dirs=[installation_dir],
        server_header=False,
        access_log=True,
    )


if __name__ == '__main__':
    start()

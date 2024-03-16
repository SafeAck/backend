from typing import Annotated
from fastapi import FastAPI, Security
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .config import DEV_ENV
from .auth import auth_router, validate_user_perms
from .auth.permissions import MePerm
from .management import mgmt_router
from .offat_scan import scan_router


async def validation_exception_handler(request, exc):
    """Custom exception handler for RequestValidationError"""
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid input data"},
    )


app = FastAPI(
    title="SafeAck API",
    debug=DEV_ENV,
    openapi_url='/api/v1/openapi.json' if DEV_ENV else None,
    servers=[
        {"url": "http://localhost:8080", "description": "Local environment"},
        # {"url": "http://localhost:8000", "description": "Production environment"},
    ],
    docs_url='/docs' if DEV_ENV else None,
    redoc_url='/redoc' if DEV_ENV else None,
)

if not DEV_ENV:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)


# register routers below
app.include_router(auth_router)
app.include_router(scan_router)
app.include_router(mgmt_router)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    # home view
    return {"msg": "SafeAck Backend is Up"}


@app.get("/restricted", tags=["root"])
async def restricted(
    user_id: Annotated[
        int, Security(validate_user_perms, scopes=[MePerm.READ.value], use_cache=False)
    ],
) -> dict:
    return {"msg": "SafeAck Backend is Up", "user_id": user_id}

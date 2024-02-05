# from alembic import command
# from alembic.config import Config
# from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Security
from .config import DEV_ENV
from .auth import auth_router, validate_user_perms
from .auth.permissions import MePerm


# @asynccontextmanager
# async def db_lifespan(app: FastAPI):
#     # start up code below

#     # auto migrate db
#     alembic_cfg = Config("alembic.ini")
#     command.upgrade(alembic_cfg, "head")

#     yield

#     # clean up code below
#     # ...

app = FastAPI(
    title="SafeAck API",
    debug=DEV_ENV,
    openapi_url='/api/v1/openapi.json' if DEV_ENV else None,
    docs_url='/docs' if DEV_ENV else None,
    redoc_url='/redoc' if DEV_ENV else None,
    # lifespan=db_lifespan,
)

# register routers below
app.include_router(auth_router)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    # home view
    return {"msg": "SafeAck Backend is Up"}


@app.get("/restricted", tags=["root"])
async def restricted(
    user_id: int = Security(Depends(validate_user_perms), scopes=[MePerm.READ.name])
) -> dict:
    return {"msg": "SafeAck Backend is Up", "user_id": user_id}

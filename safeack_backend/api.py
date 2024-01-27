from fastapi import FastAPI, Depends
from .auth import JWTBearer, auth_router

app = FastAPI(
    title="SafeAck API"
)

# register routers below
app.include_router(auth_router)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    # home view
    return {"msg": "SafeAck Backend is Up"}


@app.get("/restricted", tags=["root"], dependencies=[Depends(JWTBearer())])
async def restricted() -> dict:
    return {"msg": "SafeAck Backend is Up"}

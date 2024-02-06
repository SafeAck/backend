from decouple import config
from .utils.secrets import generate_secret

ENV: str = config("ENV", default="PRODUCTION", cast=str)
DEV_ENV = True if ENV in ["LOCAL", "DEV_ENV"] else False
JWT_SECRET: str = config("JWT_SECRET", default=generate_secret(), cast=str)
JWT_ALGORITHM: str = config("JWT_ALGORITHM", default="HS256", cast=str)
JWT_EXPIRY: int = config("JWT_EXPIRY", cast=int, default=120)

SQLALCHEMY_DATABASE_URL: str = config("SQLALCHEMY_DATABASE_URL", cast=str)

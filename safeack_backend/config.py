from decouple import config
from .utils.secrets import generate_secret

JWT_SECRET: str = config("JWT_SECRET", default=generate_secret(), cast=str)
JWT_ALGORITHM: str = config("JWT_ALGORITHM", default="HS256", cast=str)
JWT_EXPIRY: int = config("JWT_EXPIRY", cast=int, default=120)

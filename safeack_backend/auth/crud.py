from sqlalchemy.orm import Session
from . import models, schemas, password


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreateSchema, is_active: bool = False):
    hashed_password = password.get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,
        is_active=is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

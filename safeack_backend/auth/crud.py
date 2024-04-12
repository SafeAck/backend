from sqlalchemy.orm import Session
from . import models, schemas, password
from .permissions import Role


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_active_status(db: Session, user_id: int) -> tuple:
    '''
    Returns user activity status and role for provided user id
    '''
    user_data = (
        db.query(models.User.is_active, models.User.role).filter(models.User.id == user_id).first()
    )

    return (
        user_data._tuple()
        if user_data
        else (
            None,
            None,
        )
    )


def is_user_superuser(db: Session, user_id: int) -> tuple:
    """Returns user active and superuser status"""
    user_data = (
        db.query(models.User.is_active, models.User.is_superuser)
        .filter(models.User.id == user_id)
        .first()
    )

    return (
        user_data._tuple()
        if user_data
        else (
            None,
            None,
        )
    )


def get_users(db: Session, skip: int = 1, limit: int = 100) -> list:
    """
    returns list of users
    """
    skip = (skip - 1) * limit
    return (
        db.query(
            models.User.id,
            models.User.email,
            models.User.first_name,
            models.User.last_name,
            models.User.full_name,
            models.User.is_active,
            models.User.is_superuser,
            models.User.role,
        )
        .order_by(models.User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def activate_user(db: Session, user_id: int):
    '''marks user as active based on email id'''
    rows_updated = (
        db.query(models.User).filter(models.User.id == user_id).update({"is_active": True})
    )
    db.commit()
    return rows_updated


def create_user(
    db: Session,
    user: schemas.UserCreateSchema,
    is_active: bool = False,
    is_staff: bool = True,
    is_superuser: bool = False,
):
    hashed_password = password.get_password_hash(user.password)

    role = Role.USER
    if is_superuser:
        role = Role.SUPERUSER
    elif is_staff:
        role = Role.STAFF

    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,
        is_active=is_active,
        is_superuser=is_superuser,
        role=role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from sqlalchemy.orm import Session
from ..models import User
from ..auth.permissions import Role


def set_user_active(db: Session, email: str):
    """
    mark user active based on email
    """
    db.query(User).filter(User.email == email).update({"is_active": True})
    db.commit()


def set_user_superuser(db: Session, email: str):
    """
    set user as superuser. This also makes user active.
    """
    db.query(User).filter(User.email == email).update(
        {"is_superuser": True, "role": Role.SUPERUSER.name, "is_active": True}
    )
    db.commit()


def get_user_id(db: Session, email: str) -> int:
    """
    get user id using email
    """
    user_id = db.query(User.id).filter(User.email == email).first()[0]
    return user_id

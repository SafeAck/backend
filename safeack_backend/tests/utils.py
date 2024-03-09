from sqlalchemy.orm import Session
from ..models import User


def set_user_active(db: Session, email: str):
    """
    mark user active based on email
    """
    db.query(User).filter(User.email == email).update({"is_active": True})
    db.commit()

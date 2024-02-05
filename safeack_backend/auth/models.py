'''User Auth Models'''

from sqlalchemy import Boolean, Column, Integer, String, Enum
from .permissions import Role
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(Role), default=Role.USER)
    hashed_password = Column(String)

    def __str__(self):
        return f'{self.full_name} - {self.id} - {self.is_active}'

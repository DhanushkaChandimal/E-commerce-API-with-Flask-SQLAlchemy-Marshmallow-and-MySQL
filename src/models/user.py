from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(100))

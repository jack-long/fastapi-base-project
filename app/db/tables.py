from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
    name: Mapped[Optional[str]] = mapped_column()
    is_active: Mapped[Optional[bool]] = mapped_column(default=False)

    items: Mapped[List["Item"]] = relationship(back_populates="owner")

    def __repr__(self):
        return f"{self.name=} {self.email=}"


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[Optional[str]] = mapped_column()
    owner_id = mapped_column(ForeignKey("users.id"))

    owner: Mapped[User] = relationship(back_populates="items")

    def __repr__(self):
        return f"{self.id=} {self.title=}"

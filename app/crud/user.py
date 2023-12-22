"""Create, Read, Update, and Delete Operations"""
from sqlalchemy.orm import Session
from sqlalchemy import select

from .. import models
from ..db.tables import User, Item
from ..core.security import get_password_hash
from ..db.database import session_mk


def get_user(user_id: int):
    stmt = select(User).where(User.id == user_id)
    with session_mk() as session:
        return session.scalars(stmt).first()


def get_user_by_email(email: str, db: Session | None = None) -> User:
    stmt = select(User).where(User.email == email)
    if db is None:
        with session_mk() as session:
            return session.scalars(stmt).first()
    else:
        return db.scalars(stmt).first()


def create_user(*, email: str, password: str):
    hashed_password = get_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    with session_mk() as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user


def update_user(user: User):
    with session_mk() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def create_user_item(db: Session, item: models.ItemCreate, user_id: int):
    db_item = Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

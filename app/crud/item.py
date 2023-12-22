from sqlalchemy.orm import Session

import models
from db import tables


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(tables.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: models.ItemCreate, user_id: int):
    db_item = tables.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

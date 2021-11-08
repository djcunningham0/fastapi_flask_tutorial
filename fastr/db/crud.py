from sqlalchemy.orm import Session
from typing import List

from . import models, schemas


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Post]:
    return (
        db.query(models.Post)
        .order_by(models.Post.created.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_post_by_id(db: Session, id: int) -> models.Post:
    return db.query(models.Post).filter(models.Post.id == id).first()


def create_post(db: Session, create_data: schemas.Post, user_id: int):
    post = models.Post(**create_data.dict(), author_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)


def update_post(db: Session, update_data: schemas.PostUpdate):
    post = get_post_by_id(db, update_data.id)
    post.title = update_data.title
    post.body = update_data.body
    db.commit()
    db.refresh(post)


def delete_post(db: Session, post_id: int):
    post = get_post_by_id(db, post_id)
    db.delete(post)
    db.commit()

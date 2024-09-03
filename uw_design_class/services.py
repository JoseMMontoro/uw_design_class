from datetime import datetime

from sqlalchemy.orm import Session

import uw_design_class.database_models as models


def get_posts(db: Session):
    return db.query(models.Post).all()

def create_new_post(db: Session, title: str, content: str, authorid: str, blogid: str):
    authorid = int(authorid) if authorid else 1
    blogid = int(blogid) if blogid else 1
    db_post = models.Post(
        title=title,
        content=content,
        publisheddate=datetime.now(),
        authorid=authorid,
        blogid=blogid
    )
    db.add(db_post)
    db.commit()

def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.postid == post_id).first()

def update_post(db: Session, post_id: int, title: str, content: str, authorid: int, blogid: int):
    db_post = db.query(models.Post).filter(models.Post.postid == post_id).first()
    if db_post:
        db_post.title = title
        db_post.content = content
        db_post.authorid = authorid
        db_post.blogid = blogid
        db_post.publisheddate = datetime.now()
        db.commit()
        db.refresh(db_post)

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.postid == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()

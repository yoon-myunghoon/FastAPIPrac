from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..schemas import TokenData


def like(id: int, db: Session, data: TokenData):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    user = db.query(models.User).filter(models.User.email == data.email).first()
    like = db.query(models.Like).filter(models.Like.user_id == user.id, models.Like.blog_id == blog.id).first()
    if not like:
        like = models.Like(user_id=user.id, blog_id=blog.id)
        db.add(like)
        db.commit()
        db.refresh(like)
        return like
    else:
        db.delete(like)
        db.commit()
        return 'done'


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session, data: TokenData):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    new_blog = models.Blog(title=request.title, body=request.body, user_id=user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    blog.update(dict(request))
    db.commit()
    return 'updated'


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} is not available')
    return blog

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Like(Base):
    __tablename__ = 'likes'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'), primary_key=True)

    like_user = relationship("User", back_populates="liked_blogs")
    liked_blog = relationship("Blog", back_populates="like_users")


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="blogs")
    like_users = relationship("Like", back_populates="liked_blog")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    blogs = relationship("Blog", back_populates="creator")
    liked_blogs = relationship("Like", back_populates="like_user")

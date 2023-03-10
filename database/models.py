from sqlalchemy import Boolean, create_engine, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())

    # Foreign Keys
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    # Relationship with User and Comment models
    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Relationship with Post models
    posts = relationship("Post", back_populates="category")



class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, default=None)
    description = Column(String)
    confirmed = Column(Boolean, default=False)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    # Relationship with User and Post models
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")



class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    image = Column(String)
    password = Column(String)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    # Relationship with Post and Comment models
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
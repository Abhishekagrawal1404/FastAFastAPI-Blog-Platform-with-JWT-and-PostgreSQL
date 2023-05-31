from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
User.posts = relationship("Post", back_populates="author")
User.comments = relationship("Comment", back_populates="author")

Post.comments = relationship("Comment", back_populates="post")

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author = Column(String)
    comments = relationship("Comment", back_populates="blog_post")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    author = Column(String)
    blog_post_id = Column(Integer, ForeignKey("blog_posts.id"))
    blog_post = relationship("BlogPost", back_populates="comments")


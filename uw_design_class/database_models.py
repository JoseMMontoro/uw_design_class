from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
                        Text)
from sqlalchemy.orm import relationship

from uw_design_class.database_setup import Base

# Association tables
blog_tag = Table('blogtag', Base.metadata,
    Column('blogid', Integer, ForeignKey('blog.blogid')),
    Column('tagid', Integer, ForeignKey('tag.tagid'))
)

post_tag = Table('posttag', Base.metadata,
    Column('postid', Integer, ForeignKey('post.postid')),
    Column('tagid', Integer, ForeignKey('tag.tagid'))
)

# Models
class User(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    bio = Column(Text)
    avatar = Column(Text)  # Changed from bytea to Text to match SQLAlchemy

    blogs = relationship("Blog", back_populates="author")
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Blog(Base):
    __tablename__ = "blog"

    blogid = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    createddate = Column(DateTime, default="CURRENT_TIMESTAMP")
    author_id = Column(Integer, ForeignKey('users.userid'))

    author = relationship("User", back_populates="blogs")
    posts = relationship("Post", back_populates="blog")
    tags = relationship("Tag", secondary=blog_tag, back_populates="blogs")

class Post(Base):
    __tablename__ = "post"

    postid = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    publisheddate = Column(DateTime, default="CURRENT_TIMESTAMP")
    authorid = Column(Integer, ForeignKey('users.userid'), name='author')
    blogid = Column(Integer, ForeignKey('blog.blogid'))

    author = relationship("User", back_populates="posts")
    blog = relationship("Blog", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    tags = relationship("Tag", secondary=post_tag, back_populates="posts")

class Comment(Base):
    __tablename__ = "comment"

    commentid = Column(Integer, primary_key=True, index=True)
    postid = Column(Integer, ForeignKey('post.postid'))
    content = Column(Text, nullable=False)
    createddate = Column(DateTime, default="CURRENT_TIMESTAMP")
    authorid = Column(Integer, ForeignKey('users.userid'), name='author')

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

class Tag(Base):
    __tablename__ = "tag"

    tagid = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    blogs = relationship("Blog", secondary=blog_tag, back_populates="tags")
    posts = relationship("Post", secondary=post_tag, back_populates="tags")

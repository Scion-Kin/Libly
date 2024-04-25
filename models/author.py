#!/usr/bin/python3
''' This defines an Author class for SQLAlchemy modeling '''
import models
from models.base_model import BaseModel, Base
from models.favorite_author import FavoriteAuthor
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Author(BaseModel, Base):
    ''' This defines an author SQL model '''
    __tablename__ = 'authors'
    first_name = Column(String(60), nullable=False)
    middle_name = Column(String(60), nullable=True)
    pic = Column(String(128), default="author-avatar.jpeg")
    last_name = Column(String(60), nullable=False)
    book_author = relationship('BookAuthor',
                               backref="author",
                               cascade="all, delete, delete-orphan")
    fav_author = relationship("FavoriteAuthor",
                              backref="author",
                              cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """ initializes an author instance """
        super().__init__(*args, **kwargs)

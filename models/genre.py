#!/usr/bin/python
''' This defines a genre class for SQLAlchemy modeling '''
import models
from models.base_model import BaseModel, Base
from models.favorite_genre import FavoriteGenre
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Genre(BaseModel, Base):
    ''' This defines a genre SQL model '''

    __tablename__ = 'genres'
    name = Column(String(60), nullable=False)
    pic = Column(String(128), default="genre.jpg")
    book_genre = relationship('BookGenre',
                              backref="genre",
                              cascade="all, delete, delete-orphan")
    fav_genre = relationship("FavoriteGenre", backref="genre", cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """ initializes a genre instance """
        super().__init__(*args, **kwargs)

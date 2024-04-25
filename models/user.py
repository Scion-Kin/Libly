#!/usr/bin/python3
''' This defines a user class for SQLAlchemy modeling '''
from models.base_model import BaseModel, Base
from models.favorite_author import FavoriteAuthor
from models.favorite_book import FavoriteBook
from models.favorite_genre  import FavoriteGenre
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    ''' This defines a user SQL model '''

    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    user_type = Column(String(30), default="citizen")
    confirmed = Column(Boolean, default=False)
    first_name = Column(String(128), nullable=True)
    middle_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    pic = Column(String(128), default="user-avatar.jpg")
    reviews = relationship("Review", backref="user", cascade="all, delete, delete-orphan")
    fav_books = relationship("FavoriteBook", backref="user", cascade="all, delete, delete-orphan")
    fav_authors = relationship("FavoriteAuthor", backref="user", cascade="all, delete, delete-orphan")
    fav_genres = relationship("FavoriteGenre", backref="user", cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """ initializes a user instance """
        super().__init__(*args, **kwargs)

        if "username" in kwargs:
            self.id = kwargs["id"]

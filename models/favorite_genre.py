#!/usr/bin/python3
''' This defines an Genre class for SQLAlchemy modeling '''
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class FavoriteGenre(BaseModel, Base):
    ''' This defines a genre favorite relationship '''
    __tablename__ = 'favorite_genres'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    genre_id = Column(String(60), ForeignKey('genres.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        """ initializes instance """
        super().__init__(*args, **kwargs)

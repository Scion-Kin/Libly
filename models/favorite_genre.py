#!/usr/bin/python3
''' This defines a favorites model '''
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class FavoriteGenre(BaseModel, Base):
    ''' This defines a favorite genre SQL model '''

    __tablename__ = "favorite_genres"
    genre_id = Column(String(128), ForeignKey('genres.id'), nullable=False)
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)

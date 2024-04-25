#!/usr/bin/python3
''' This defines a favorites model '''
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class FavoriteAuthor(BaseModel, Base):
    ''' This defines a favorite author SQL model '''

    __tablename__ = "favorite_authors"
    author_id = Column(String(128), ForeignKey('authors.id'), nullable=False)
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)

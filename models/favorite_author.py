#!/usr/bin/python3
''' This defines an SQLAlchemy model '''
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class FavoriteAuthor(BaseModel, Base):
    ''' This defines an author favorite relationship '''
    __tablename__ = 'favorite_authors'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    author_id = Column(String(60), ForeignKey('authors.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """ initializes instance """
        super().__init__(*args, **kwargs)

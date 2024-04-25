#!/usr/bin/python3
''' This defines a favorites model '''
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class FavoriteBook(BaseModel, Base):
    ''' This defines a favorite book SQL model '''

    __tablename__ = "favorite_books"
    book_id = Column(String(128), ForeignKey('books.id'), nullable=False)
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)

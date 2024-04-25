#!/usr/bin/python3
''' This defines an book class for SQLAlchemy modeling '''
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class FavoriteBook(BaseModel, Base):
    ''' This defines a book favorite relationship '''
    __tablename__ = 'favorite_books'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    book_id = Column(String(60), ForeignKey('books.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        """ initializes instance """
        super().__init__(*args, **kwargs)

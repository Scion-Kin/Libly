#!/usr/bin/python3
''' This defines an Genre class for SQLAlchemy modeling '''
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class BookGenre(BaseModel, Base):
    ''' This defines an genre book SQL relationship '''
    __tablename__ = 'book_genres'
    book_id = Column(String(60), ForeignKey('books.id'), nullable=False)
    genre_id = Column(String(60), ForeignKey('genres.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        """ initializes an Genre instance """
        super().__init__(*args, **kwargs)

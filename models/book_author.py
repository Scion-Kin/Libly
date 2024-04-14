#!/usr/bin/python3
''' This defines an Author class for SQLAlchemy modeling '''
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class BookAuthor(BaseModel, Base):
    ''' This defines an author book SQL relationship '''
    __tablename__ = 'book_authors'
    book_id = Column(String(60), ForeignKey('books.id'), nullable=False)
    author_id = Column(String(60), ForeignKey('authors.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        """ initializes an author instance """
        super().__init__(*args, **kwargs)

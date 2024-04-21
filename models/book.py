''' This defines a book class for SQLAlchemy modeling '''
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


class Book(BaseModel, Base):
    ''' This defines a book SQL model '''

    __tablename__ = 'books'
    title = Column(String(60), nullable=False)
    ISBN = Column(String(60), nullable=False)
    pic = Column(String(128), default="vintage-book.png")
    book_genre = relationship('BookGenre',
                              backref="book",
                              cascade="all, delete, delete-orphan")
    book_author = relationship('BookAuthor',
                               backref="book",
                               cascade="all, delete, delete-orphan")
    reviews = relationship("Review", backref="book", cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """ initializes a book instance """
        super().__init__(*args, **kwargs)

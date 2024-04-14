#!/usr/bin/python3
''' This defines a Review class for SQLAlchemy modeling '''
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    ''' This defines a review SQL model '''
    __tablename__ = 'reviews'
    book_id = Column(String(60), ForeignKey('books.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)

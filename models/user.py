#!/usr/bin/python3
''' This defines a user class for SQLAlchemy modeling '''
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    ''' This defines a user SQL model '''

    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    user_type = Column(String(30), default="citizen")
    first_name = Column(String(128), nullable=True)
    middle_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    reviews = relationship("Review", backref="user")

    def __init__(self, *args, **kwargs):
        """ initializes a user instance """
        super().__init__(*args, **kwargs)

        if "username" in kwargs:
            self.id = kwargs["id"]

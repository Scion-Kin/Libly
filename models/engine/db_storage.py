#!/usr/bin/python3
''' Defines a mysql model storage class '''

from models.author import Author
from models.base_model import Base
from models.book_author import BookAuthor
from models.book_genre import BookGenre
from models.book import Book
from models.favorite_author import FavoriteAuthor
from models.favorite_book import FavoriteBook
from models.favorite_genre import FavoriteGenre
from models.genre import Genre
from models.review import Review
from models.user import User
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Author": Author, "Book": Book,
           "Genre": Genre, "Review": Review,
           "User": User, 'BookAuthor': BookAuthor,
           "BookGenre": BookGenre, "FavoriteAuthor": FavoriteAuthor,
           "FavoriteBook": FavoriteBook, "FavoriteGenre": FavoriteGenre}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        LIBLY_MYSQL_USER = getenv('MYSQL_USER', 'libly_user')
        LIBLY_MYSQL_PWD = getenv('MYSQL_PASSWORD', 'libDev')
        LIBLY_MYSQL_HOST = getenv('MYSQL_HOST', 'localhost')
        LIBLY_MYSQL_DB = getenv('MYSQL_DB', 'libly')
        LIBLY_ENV = getenv('LIBLY_ENV', 'production')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(LIBLY_MYSQL_USER,
                                             LIBLY_MYSQL_PWD,
                                             LIBLY_MYSQL_HOST,
                                             LIBLY_MYSQL_DB))
        if LIBLY_ENV == "test":
            Base.metadata.drop_all(self.__engine)

        if self.__session is None:
            self.reload()

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """ Returns the object based on the class and its ID,
        or None if not found """

        cls_list = self.all(cls)

        if type(cls) == str:
            key_id = classes[cls].__name__ + '.' + id
        else:
            key_id = cls.__name__ + '.' + id

        for i in cls_list:
            if i == key_id:
                return cls_list[i]
        return None

    def count(self, cls=None):
        """ Returns the number of objects in storage matching the given class.
        If no class is passed, returns the count of all objects in storage. """

        if cls:
            return len(self.all(cls))

        else:
            return len(self.all())

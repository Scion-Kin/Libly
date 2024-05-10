#!/usr/bin/python3
''' The collection of blueprints '''
from flask import Blueprint

grand_view = Blueprint('grand_view', __name__, url_prefix="/api/v1")

from flask_api.v1.views.author import *
from flask_api.v1.views.book import *
from flask_api.v1.views.fav_author import *
from flask_api.v1.views.fav_book import *
from flask_api.v1.views.fav_genre import *
from flask_api.v1.views.genre import *
from flask_api.v1.views.hot import *
from flask_api.v1.views.index import *
from flask_api.v1.views.pool import *
from flask_api.v1.views.report import *
from flask_api.v1.views.review import *
from flask_api.v1.views.search import *
from flask_api.v1.views.user import *

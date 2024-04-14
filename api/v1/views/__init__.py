#!/usr/bin/python3
''' The collection of blueprints '''
from flask import Blueprint

grand_view = Blueprint('grand_view', __name__, url_prefix="/api/v1")

from api.v1.views.book import *
from api.v1.views.index import *
from api.v1.views.genre import *
from api.v1.views.author import *
from api.v1.views.review import *
from api.v1.views.user import *

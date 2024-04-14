#!/usr/bin/python3
''' The collection of blueprints '''
from flask import Blueprint

grand_view = Blueprint('grand_view', __name__, url_prefix="/api")

from api.v1.views.book import *

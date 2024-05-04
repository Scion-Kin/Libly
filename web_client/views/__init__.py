#!/usr/bin/python3
''' the whole web client view colection '''

from flask import Blueprint

client_view = Blueprint('client_view', __name__)

from web_client.views.about import about
from web_client.views.activation import confirmed_email
from web_client.views.admin import *
from web_client.views.author_genre import *
from web_client.views.goodies import *
from web_client.views.info import *
from web_client.views.login import *
from web_client.views.resource_list import *
from web_client.views.read import *
from web_client.views.report import *
from web_client.views.settings import *
from web_client.views.signup import signup

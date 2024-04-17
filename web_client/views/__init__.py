#!/usr/bin/python3
''' the whole web client view colection '''

from flask import Blueprint

client_view = Blueprint('client_view', __name__)

from web_client.views.activation import confirmed_email
from web_client.views.login import login

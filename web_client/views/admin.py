#!/usr/bin/python3
''' The admin manager '''

from web_client.views import client_view
from flask import render_template, request, session, url_for, redirect
from models import storage
from itsdangerous import URLSafeSerializer
import requests


@client_view.route('/manage/authors', methods=['GET', 'POST'], strict_slashes=False)
def manage_authors():
    ''' manage authors '''

    return render_template('manage_resource.html', title="Authors")


@client_view.route('/manage/books', methods=['GET', 'POST'], strict_slashes=False)
def manage_books():
    ''' manage books '''

    return render_template('manage_resource.html', title="Books")


@client_view.route('/manage/genres', methods=['GET', 'POST'], strict_slashes=False)
def manage_genres():
    ''' manage genres '''

    return render_template('manage_resource.html', title="Genres")


@client_view.route('/manage/reviews', methods=['GET', 'POST'], strict_slashes=False)
def manage_reviews():
    ''' manage reviews '''

    return render_template('manage_resource.html', title="Reviews")


@client_view.route('/manage/users', methods=['GET', 'POST'], strict_slashes=False)
def manage_users():
    ''' manage users '''

    return render_template('manage_resource.html', title="Users")

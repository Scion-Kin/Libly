#!/usr/bin/python3
''' The admin manager '''

from web_client.views import client_view
from flask import render_template, session, abort


@client_view.route('/manage/authors', strict_slashes=False)
def manage_authors():
    ''' manage authors '''
    if session and session['user_type'] == 'king':
        return render_template('manage_resource.html', title="Authors")
    abort(404)


@client_view.route('/manage/books', strict_slashes=False)
def manage_books():
    ''' manage books '''
    if session and session['user_type'] == 'king':
        return render_template('manage_resource.html', title="Books")
    abort(404)


@client_view.route('/manage/genres', strict_slashes=False)
def manage_genres():
    ''' manage genres '''
    if session and session['user_type'] == 'king':
        return render_template('manage_resource.html', title="Genres")
    abort(404)


@client_view.route('/manage/reviews', strict_slashes=False)
def manage_reviews():
    ''' manage reviews '''
    if session and session['user_type'] == 'king':
        return render_template('manage_resource.html', title="Reviews")
    abort(404)


@client_view.route('/manage/users', strict_slashes=False)
def manage_users():
    ''' manage users '''
    if session and session['user_type'] == 'king':
        return render_template('manage_resource.html', title="Users")
    abort(404)

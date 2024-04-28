#!/usr/bin/python3
''' The admin manager '''

from web_client.views import client_view
from flask import render_template, session, abort, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import requests
import os


@client_view.route('/manage/authors', methods=['GET', 'POST'], strict_slashes=False)
def manage_authors():
    ''' manage authors '''
    if session and session['user_type'] == 'librarian':
        
        if request.method == 'POST':
            file = request.files['pic']
            headers = {"Content-Type": "application/json"}
            response = requests.post('https://usernet.tech/api/v1/authors',
                                     headers=headers, json={
                "first_name": request.form.get('first_name'), "middle_name": request.form.get('middle_name'),
                "last_name": request.form.get('last_name'), "pic": secure_filename(file.filename)
            })

            file.save(os.path.join('web_client/static/images', secure_filename(file.filename)))

            return redirect(url_for('client_view.manage_authors'))

        return render_template('manage_resource.html', title="Authors", pic=session["user_pic"])
    abort(404)


@client_view.route('/manage/books', methods=['GET', 'POST'], strict_slashes=False)
def manage_books():
    ''' manage books '''

    if session and session['user_type'] == 'librarian':

        if request.method == 'POST':
            book_file = request.files['file']
            book_cover = request.files['pic']

            headers = {"Content-Type": "application/json"}
            response = requests.post('https://usernet.tech/api/v1/books',
                                     headers=headers, json={
                "title": request.form.get('title'), "ISBN": request.form.get('ISBN'),
                "authors": request.form.get('authors').split(','),
                "genres": request.form.get('genres').split(','), 
                "file_name": secure_filename(book_file.filename),
                "pic": secure_filename(book_cover.filename),
                "description": request.form.get('description')
            })

            if response.status_code < 400:
                book_file.save(os.path.join('web_client/books/', secure_filename(book_file.filename)))
                book_cover.save(os.path.join('web_client/static/images/', secure_filename(book_cover.filename)))

            return redirect(url_for('client_view.manage_books'))

        genres = requests.get('https://usernet.tech/api/v1/genres')
        authors = requests.get('https://usernet.tech/api/v1/authors')

        return render_template('manage_resource.html', title="Books", pic=session["user_pic"],
                               genres=genres.json(), authors=authors.json())
    abort(404)


@client_view.route('/manage/genres', methods=['GET', 'POST'], strict_slashes=False)
def manage_genres():
    ''' manage genres '''
    if session and session['user_type'] == 'librarian':
        if request.method == 'POST':
            headers = {"Content-Type": "application/json"}
            response = requests.post('https://usernet.tech/api/v1/genres',
                                     headers=headers,
                                     json={"name": request.form.get('name')})
            if response.status_code != 201:
                return render_template('manage_resource.html', title="Genres", error=response.json(), pic=session["user_pic"])

        return render_template('manage_resource.html', title="Genres", pic=session["user_pic"])
    abort(404)


@client_view.route('/manage/reviews', strict_slashes=False)
def manage_reviews():
    ''' manage reviews '''
    if session and session['user_type'] == 'librarian':
        return render_template('manage_resource.html', title="Reviews", pic=session["user_pic"])
    abort(404)


@client_view.route('/manage/users', strict_slashes=False)
def manage_users():
    ''' manage users '''
    if session and session['user_type'] == 'librarian':
        return render_template('manage_resource.html', title="Users", pic=session["user_pic"])
    abort(404)

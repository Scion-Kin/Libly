#!/usr/bin/python3
''' This is the web server '''

from web_client.views import client_view
from flask import Flask, Blueprint, render_template, abort, session, request, abort, redirect, url_for
import requests


@client_view.route('/about/book', methods=['GET', 'POST'], strict_slashes=False)
def book_info():
    ''' The home page route '''

    if request.method == 'POST':

        response = requests.get('http://localhost:5000/api/v1/books/{}'.format(request.form.get('id')))

        if response.status_code < 300:

            return render_template('info.html', info=response.json())

    return render_template('info.html')

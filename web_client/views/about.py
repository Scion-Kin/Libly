#!/usr/bin/python3
''' The about route '''

from web_client.views import client_view
from flask import render_template


@client_view.route('/about', strict_slashes=False)
def about():
    ''' sign the user up '''

    return render_template('about.html')

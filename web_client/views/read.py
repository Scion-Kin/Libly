#!/usr/bin/python3
''' The admin manager '''

from web_client.views import client_view
from flask import render_template, session, redirect, url_for
import fitz
import io
from PIL import Image
import requests


@client_view.route('/read/<string:book_id>', strict_slashes=False)
def read_book(book_id):
    ''' manage authors '''

    if session and session['logged'] == True:

        data = requests.get(f'http://localhost:5000/api/v1/books/{book_id}')

        if data.status_code == 200:
            for i in data.json():
                file_name = 'web_client/books/' + data.json()[i]["data"]["file_name"]

                # Open the PDF file using PyMuPDF
                pdf_document = fitz.open(file_name)

                page_images = []

                # Iterate through each page and convert to image
                for page_num in range(len(pdf_document)):
                    # Render the page as a Pixmap
                    page_pixmap = pdf_document[page_num].get_pixmap()

                    # Convert Pixmap to an image
                    image = Image.frombytes(
                        "RGB",
                        [page_pixmap.width, page_pixmap.height],
                        page_pixmap.samples
                    )

                    # Convert image to bytes
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format="PNG")
                    img_bytes.seek(0)

                    # Append image data to the list
                    page_images.append(img_bytes.getvalue())

                # Pass the list of image data to the HTML template

                return render_template('read.html', data=page_images)

    return redirect(url_for('home'))

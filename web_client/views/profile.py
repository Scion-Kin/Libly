#!/usr/bin/python3
''' Defines a method for user profiles '''

from web_client.views import client_view
from flask import session, redirect, url_for, render_template, abort
from uuid import uuid4
import aiohttp
import asyncio


@client_view.route('/profile/<string:user_id>', strict_slashes=False)
def profile(user_id):
    ''' Handels user profiling '''

    if not session or not session['logged']:
        return redirect(url_for('home'))

    async def fetch(session, url):
        ''' fetches data asynchronously '''
        async with session.get(url) as response:
            return await response.json(), response.status

    async def get_user_data(user_id):
        links = [
            'https://usernet.tech/api/v1/users/{}'.format(user_id),
            'https://usernet.tech/api/v1/users/{}/reviews'.format(user_id),
            'https://usernet.tech/api/v1/{}/favs/authors'.format(user_id),
            'https://usernet.tech/api/v1/{}/favs/books'.format(user_id),
            'https://usernet.tech/api/v1/{}/favs/genres'.format(user_id)
        ]

        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url) for url in links]
            responses = await asyncio.gather(*tasks)

            user = responses[0][0] if responses[0][1] == 200 else abort(404)
            user = list(user.values())[0]["data"]
            print(user)

            reviews = responses[1][0] if responses[1][1] == 200 else []

            async def fetch_details(url, obs, id_type):
                ''' Fetches the sub-contents '''
                tasks = [fetch(session, url.format(i[id_type])) for i in obs]
                fav = await asyncio.gather(*tasks)
                fav = [i[0] for i in fav]
                return [list(i.values())[0]["data"] for i in fav]

            fav_authors = responses[2]
            if fav_authors[1] == 200:
                url = 'https://usernet.tech/api/v1/authors/{}'
                fav_authors = await fetch_details(url, fav_authors[0],
                                                  'author_id')
            else:
                fav_authors = []

            fav_books = responses[3]

            if fav_books[1] == 200:
                url = 'https://usernet.tech/api/v1/books/{}'
                fav_books = await fetch_details(url, fav_books[0],
                                                'book_id')
            else:
                fav_books = []

            fav_genres = responses[4]

            if fav_genres[1] == 200:
                url = 'https://usernet.tech/api/v1/genres/{}'
                fav_genres = await fetch_details(url, fav_genres[0],
                                                 'genre_id')
            else:
                fav_books = []

            return {
                "user": user, "reviews": reviews, "fav_authors": fav_authors,
                "fav_books": fav_books, "fav_genres": fav_genres
            }

    user_data = asyncio.run(get_user_data(user_id))

    return render_template(
        'profile.html', pic=session["user_pic"],
        authors=user_data["fav_authors"], books=user_data["fav_books"],
        genres=user_data["fav_genres"], reviews=user_data["reviews"],
        user=user_data["user"], uuid=uuid4()
    )

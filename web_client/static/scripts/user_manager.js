document.addEventListener('DOMContentLoaded', function () {

    const logOut = document.getElementById('log-out');
    const showMenu = document.getElementById('user-menu');
    const user = document.getElementById('avatar');
    const settings = document.getElementById('settings');
    const help = document.getElementById('help');
    const love = document.getElementById('love');

    settings.addEventListener('click', function () {
        window.location.href = '/settings';
    });

    help.addEventListener('click', function () {
        window.location.href = 'https://wa.me/+250787399841';
    });

    let displayed = false;

    user.addEventListener('click', function () {
        if (displayed == false) {
            showMenu.style.display = 'block';
            displayed = true;
        }
        else {
            showMenu.style.display = 'none';
            displayed = false;
        }
    });

    logOut.addEventListener('click', function () {
        window.location.href = '/logout';
    });

    if (love) {
        let user_id = getUserId();
        let typeId = love.getAttribute('type-id');
        let favType = love.getAttribute('fav');
        let favId = love.getAttribute('fav-id');
        let stripped = favType.replace(/s/g, '_id'); // remove the 's' at the end to interact with the response better

        fetch(`https://usernet.tech/api/v1/${user_id}/favs/${favType}`)
            .then(function (response) {
                if (!response.ok) {
                    console.error(response.json()["error"]);
                }
                return response.json();
            })
            .then(function (data) {
                for (i in data) {
                    console.log(`${stripped} is ${data[i][stripped]}`);
                    if (data[i][stripped] == typeId) {
                        love.style.backgroundImage = "url('/static/images/loved-icon.svg')";
                        love.setAttribute('fav-id', i["id"]);
                        favId = love.getAttribute('fav-id');
                        break;
                    }
                }
            })
            .catch(error => {
                alert('Failed to fetch data or parse response');
            });

        love.addEventListener('click', function () {
            if (favId) {
                fetch(`https://usernet.tech/api/v1/favs/${favType}/${favId}`, {
                    method: 'DELETE'
                })
                .then(function(response) {
                    if (response.ok) {
                        love.style.backgroundImage = "url('/static/images/love-icon.svg')";
                        love.removeAttribute('fav-id');
                    } else {
                        alert('Failed to remove favorite');
                    }
                })
                .catch(error => {
                    console.log(error);
                });
            } else {
                let content = {}
                if (stripped === 'author_id') {
                    content = {
                        author_id: typeId,
                        user_id: user_id
                    }
                } else if (stripped === 'genre_id') {
                    content = {
                        genre_id: typeId,
                        user_id: user_id
                    }
                } else {
                    content = {
                        book_id: typeId,
                        user_id: user_id
                    }
                }

                fetch(`https://usernet.tech/api/v1/favs/${favType}/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(content)
                })
                .then(function(response) {
                    if (response.ok) {
                        love.style.backgroundImage = "url('/static/images/loved-icon.svg')";
                        love.setAttribute('fav-id', response.json()['id']);
                    } else {
                        alert('Failed to make favorite');
                    }
                })
                .catch(error => {
                    console.log(error);
                });
            }
        });
    }

    let history = document.getElementById('history');

    if (history) {
	if (localStorage.length <= 1) {
            const section = document.createElement('section');
            const button = document.createElement('button');
            button.textContent = "Nothing read yet";
            section.appendChild(button);
            section.className = "history-book";
            history.appendChild(section);
	}

	else {
	        // Loop through localStorage and store 2 keys in the keys array
            for (let i = 0; i < 2; i++) {
                const key = localStorage.key(i);
                if (key != "darkmode-state") {
                    const section = document.createElement('section');
                    const button = document.createElement('button');
                    button.textContent = key;
                    let id = localStorage.getItem(key).split('_')[0];

                    button.addEventListener('click', function () {
                        window.location.href = `/read/${id}`;
                    });

                    section.appendChild(button);
                    section.className = "history-book";
                    section.style.backgroundImage = `url('/static/images/${localStorage.getItem(key).split('_')[1]}')`;
                    history.appendChild(section);
                }
            }
        }
    }

    function getUserId() {
        let cookieArray = document.cookie.split(';');

        for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i].trim();
            if (cookie.indexOf('user_id') == 0) {
                return cookie.substring(('=user_id').length, cookie.length);
            }
        }
    }
});

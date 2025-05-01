import { host } from "./API_HOST.js";
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import hljs from 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.10.0/build/es/highlight.min.js';

document.addEventListener('DOMContentLoaded', function () {
  const logOut = document.getElementById('log-out');
  const showMenu = document.getElementById('user-menu');
  const user = document.getElementById('avatar');
  const settings = document.getElementById('settings');
  const help = document.getElementById('help');
  const love = document.getElementById('love');
  const profile = document.getElementById('profile');

  Array.from(document.getElementsByClassName('markdown')).forEach(function (element) {
    const text = element.innerHTML;
    const html = marked(text.trim()); // I wonder why it's not processing '\n' in the text.
    element.innerHTML = html;
  });

  hljs.highlightAll();

  profile.addEventListener('click', function () {
    window.location.href = `/profile/${getUserId()}`;
  });

  settings.addEventListener('click', function () {
    window.location.href = '/settings';
  });

  help.addEventListener('click', function () {
    window.location.href = 'https://wa.me/+250787399841';
  });

  let displayed = false;

  user.addEventListener('click', function () {
    if (displayed === false) {
      showMenu.style.display = 'block';
      displayed = true;
    } else {
      showMenu.style.display = 'none';
      displayed = false;
    }
  });

  logOut.addEventListener('click', function () {
    for (let i = 0; i <= localStorage.length; i++) {
      localStorage.removeItem(localStorage.key(i));
    }
    window.location.href = '/logout';
  });

  if (love) {
    const userId = getUserId();
    const typeId = love.getAttribute('type-id');
    const favType = love.getAttribute('fav');
    let favId = love.getAttribute('fav-id');
    const stripped = favType.replace(/s/g, '_id'); // remove the 's' at the end to interact with the response better

    fetch(`https://${host}/api/v1/${userId}/favs/${favType}`)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        for (let i in data) {
          if (data[i][stripped] === typeId) {
            love.style.backgroundImage = "url('/static/images/loved-icon.svg')";
            love.setAttribute('fav-id', data[i].id);
            favId = love.getAttribute('fav-id');
            break;
          }
        }
      });

    love.addEventListener('click', function () {
      if (favId) {
        fetch(`https://${host}/api/v1/favs/${favType}/${favId}`, {
          method: 'DELETE'
        })
          .then(function (response) {
            if (response.ok) {
              love.style.backgroundImage = "url('/static/images/love-icon.svg')";
              love.removeAttribute('fav-id');
              favId = undefined;
            } else {
              alert('Failed to remove favorite');
            }
          })
          .catch(error => {
            console.log(error);
          });
      } else {
        let content = {};
        if (stripped === 'author_id') {
          content = {
            author_id: typeId,
            user_id: userId
          };
        } else if (stripped === 'genre_id') {
          content = {
            genre_id: typeId,
            user_id: userId
          };
        } else {
          content = {
            book_id: typeId,
            user_id: userId
          };
        }

        fetch(`https://${host}/api/v1/favs/${favType}/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(content)
        })
          .then(function (response) {
            if (response.ok) {
              const data = response.json();
              love.style.backgroundImage = "url('/static/images/loved-icon.svg')";
              love.setAttribute('fav-id', data.id);
              favId = data.id;
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

  const history = document.getElementById('history');

  if (localStorage.length <= 1) {
    const section = document.createElement('section');
    const button = document.createElement('button');
    button.textContent = 'Nothing read yet';
    section.appendChild(button);
    section.className = 'history-book';
    history.appendChild(section);
  } else {
    for (let i = 0; i <= 2; i++) {
      const key = localStorage.key(i);
      if (key !== 'darkmode-state') {
        const section = document.createElement('section');
        const button = document.createElement('button');
        button.textContent = key;
        const id = localStorage.getItem(key).split('@') ? localStorage.getItem(key).split('@')[0] : null;

        if (id) {
          button.addEventListener('click', function () {
            window.location.href = `/read/${id}`;
          });

          section.appendChild(button);
          section.className = 'history-book';
          section.style.backgroundImage = `url('/static/images/${localStorage.getItem(key).split('@')[1]}')`;
          history.appendChild(section);
        }
      }
    }
  }

  function getUserId () {
    const cookieArray = document.cookie.split(';');

    for (let i = 0; i < cookieArray.length; i++) {
      const cookie = cookieArray[i].trim();
      if (cookie.indexOf('user_id') === 0) {
        return cookie.substring(('=user_id').length, cookie.length);
      }
    }
  }
});

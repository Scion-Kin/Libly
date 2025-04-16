document.addEventListener('DOMContentLoaded', function () {
  const all = document.getElementById('all');
  const authors = document.getElementById('authors');
  const books = document.getElementById('books');
  const genres = document.getElementById('genres');
  const users = document.getElementById('users');

  const authorsArray = document.getElementsByClassName('author');
  const booksArray = document.getElementsByClassName('book');
  const genresArray = document.getElementsByClassName('genre');
  const usersArray = document.getElementsByClassName('user');
  let hidden = false;

  all.addEventListener('click', function (e) {
    e.preventDefault();
    hidden = true;
    hide([authorsArray, booksArray, genresArray, usersArray]);
  });

  authors.addEventListener('click', function (e) {
    e.preventDefault();
    hide([booksArray, genresArray, usersArray]);
  });

  books.addEventListener('click', function (e) {
    e.preventDefault();
    hide([authorsArray, genresArray, usersArray]);
  });

  genres.addEventListener('click', function (e) {
    e.preventDefault();
    hide([authorsArray, booksArray, usersArray]);
  });

  users.addEventListener('click', function (e) {
    e.preventDefault();
    hide([authorsArray, booksArray, genresArray]);
  });

  function hide (array) {
    if (hidden === false) {
      for (const i of array) {
        Array.from(i).forEach(element => {
          element.style.display = 'none';
        });
      }
      hidden = true;
    } else {
      for (const i of [authorsArray, booksArray, genresArray, usersArray]) {
        Array.from(i).forEach(element => {
          element.style.display = 'block';
        });
      }
      hidden = false;
    }
  }
});

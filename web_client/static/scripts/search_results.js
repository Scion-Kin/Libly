document.addEventListener('DOMContentLoaded', function () {
    console.log('Document is ready.');

    const all = document.getElementById('all');
    const authors = document.getElementById('authors');
    const books = document.getElementById('books');
    const genres = document.getElementById('genres');
    const users = document.getElementById('users');

    let authorsArray = document.getElementsByClassName('author');
    let booksArray = document.getElementsByClassName('book');
    let genresArray = document.getElementsByClassName('genre');
    let usersArray = document.getElementsByClassName('user');
    let hidden = false;
    
    all.addEventListener('click', function(e) {

        e.preventDefault();
        hidden = true;
        hide([booksArray, booksArray,genresArray, usersArray]);
    });

    authors.addEventListener('click', function(e) {

        e.preventDefault();
        hide([booksArray, genresArray, usersArray]);
    });

    books.addEventListener('click', function(e) {
        e.preventDefault();
        hide([authorsArray, genresArray, usersArray]);
    });

    genres.addEventListener('click', function(e) {
        e.preventDefault();
        hide([authorsArray, booksArray, usersArray]);
    });

    users.addEventListener('click', function(e) {
        e.preventDefault();
        hide([authorsArray, booksArray, genresArray]);
    });   

    function hide(array) {
        if (hidden == false) {
            for (let i of array) {
                Array.from(i).forEach(element => {
                    element.style.display = 'none';
                });
            }
            hidden = true;
        }

        else {
            for (let i of array) {
                Array.from(i).forEach(element => {
                    element.style.display = 'block';
                });
            }
            hidden = false;
        }
    }
});

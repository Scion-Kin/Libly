document.addEventListener('DOMContentLoaded', function () {
    console.log('Document is ready.');

    const authors = document.getElementById('authors');
    const books = document.getElementById('books');
    const genres = document.getElementById('genres');
    const users = document.getElementById('users');


    authors.addEventListener('click', function(e) {

        e.preventDefault();
        let results = document.getElementById('results');
        let key = document.getElementById('search');

        let keywords = document.title.replace(/\|/g, '');
        keywords = keywords.replace(/Libly/g, '');
        keywords = keywords.replace(/Search:/g, '');

        console.log(keywords);
    });
});

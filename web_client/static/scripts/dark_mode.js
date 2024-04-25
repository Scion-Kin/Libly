document.addEventListener('DOMContentLoaded', function () {

    const switcher = document.getElementById('dark');
    let main = document.querySelector('main');
    let header = document.querySelector('header');
    let inputs = document.querySelectorAll('input[type="search"]');
    let resultSection = document.getElementById('results');
    let quotes = document.getElementsByClassName('quote');
    let sugBooks = document.getElementsByClassName('suggested-book');
    let results_nav = document.getElementsByClassName('results_nav');
    let history = document.getElementsByClassName('history');
    let options = document.getElementsByClassName('options');
    let resultBoxes = document.getElementsByClassName('result-box');

    if (!(localStorage.getItem('darkmode-state'))) {
        localStorage.setItem('darkmode-state', 'light');
    }
    switchMode(localStorage.getItem('darkmode-state'));

    switcher.addEventListener('click', function () {
        localStorage.getItem('darkmode-state') === 'light' ? switchMode('dark') : switchMode('light');
    });

    function switchMode (mode) {
       if (mode === 'dark') {
            header.style.backgroundColor = '#181a1b';
            main.style.backgroundColor === 'white' ? main.style.backgroundColor = 'black' : main.style.backgroundColor = 'rgb(37, 40, 42)';
            main.style.color = 'white';
            document.body.style.backgroundColor = '#181a1b';
            document.body.style.color = '#e8e6e3';
            if (resultSection) {
                resultSection.style.backgroundColor = 'rgb(37, 40, 42)';
                resultSection.style.color = '#e7e8e9';
            }

            Array.from(quotes).forEach(element => {
                element.style.backgroundColor = 'black';
            });

            Array.from(history).forEach(element => {
                element.style.backgroundColor = 'black';
            });

            Array.from(options).forEach(element => {
                element.style.backgroundColor = 'black';
            });

            Array.from(results_nav).forEach(element => {
                element.style.backgroundColor = 'black';
                element.style.color = '#e7e8e9';
            });

            Array.from(resultBoxes).forEach(element => {
                element.style.backgroundColor = 'black';
                element.style.color = '#e7e8e9';
            });

            Array.from(sugBooks).forEach(element => {
                element.style.backgroundColor = 'black';
            });

            Array.from(inputs).forEach(element => {
                element.style.backgroundColor = 'rgb(37, 40, 42)';
                element.style.color = '#e7e8e9';
            });
            localStorage.setItem('darkmode-state', 'dark');
        }
        else {
            header.style.backgroundColor = '#e0e0e0';
            document.body.style.backgroundColor = '#e8e6e3';
            main.style.backgroundColor === 'black' ? main.style.backgroundColor = 'white' : main.style.backgroundColor = '#e0e0e0';
            main.style.color = '#181a1b';
            document.body.style.color = '#181a1b';
            if (resultSection) {
                resultSection.style.backgroundColor = '#e7e8e9';
                resultSection.style.color = '#181a1b';
            }

            Array.from(quotes).forEach(element => {
                element.style.backgroundColor = 'white';
            });

            Array.from(sugBooks).forEach(element => {
                element.style.backgroundColor = 'white';
            });

            Array.from(history).forEach(element => {
                element.style.backgroundColor = 'white';
            });

            Array.from(resultBoxes).forEach(element => {
                element.style.backgroundColor = 'white';
                element.style.color = '#181a1b';
            });

            Array.from(options).forEach(element => {
                element.style.backgroundColor = 'white';
            });

            Array.from(inputs).forEach(element => {
                element.style.backgroundColor = '#F0F2F5';
                element.style.color = '#181a1b';
            });
            localStorage.setItem('darkmode-state', 'light');
        }
    }
});

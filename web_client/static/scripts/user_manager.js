document.addEventListener('DOMContentLoaded', function () {

    const logOut = document.getElementById('log-out');

    logOut.addEventListener('click', function () {
        window.location.href = '/logout';
    });

});

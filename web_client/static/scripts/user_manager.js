document.addEventListener('DOMContentLoaded', function () {

    const logOut = document.getElementById('log-out');
    const showMenu = document.getElementById('user-menu');
    const user = document.getElementById('user');

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

});

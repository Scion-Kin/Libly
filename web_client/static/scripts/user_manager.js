document.addEventListener('DOMContentLoaded', function () {

    const logOut = document.getElementById('log-out');
    const showMenu = document.getElementById('user-menu');
    const user = document.getElementById('user');
    const settings = document.getElementById('settings');
    const help = document.getElementById('help');

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

});

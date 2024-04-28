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
});

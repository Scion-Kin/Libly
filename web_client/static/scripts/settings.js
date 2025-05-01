import { host } from "./API_HOST.js";

const form = document.createElement('section');
const trash = document.getElementById('trash');
let passInput = document.createElement('input');
let errorInfo = document.createElement('p');
$(passInput).attr('placeholder', 'Input your admin password');
$(errorInfo).text('An error code was returned. Make sure your password is right and try again.');
$(errorInfo).css({'color': 'red', 'font-weight': 'bolder', 'display': 'none', 'margin': 'auto'});
$(errorInfo).attr('id', 'error-info');
$(passInput).attr('type', 'password');
$(form).attr({'class': 'confirm'});
$(document.querySelector('main')).append(form);

$(trash).click(function () {
    let is = confirm('Are you sure you want to delete this account? This action can not be undone!');
    if (is === true) {
        let button = document.createElement('button');
        const cancel = document.createElement('button');
        $(cancel).attr('class', 'cancel');
        $(cancel).text('X');
        $(cancel).click(function () {
            $(form).css('display', 'none');
        });
        $(button).text('Confirm');

        $(form).css({
            'display': 'flex', 'position': 'relative'
        });

        $(form).html([cancel, passInput, button, errorInfo]);
        $(button).click(function () {
            $.ajax({
                type: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                data: JSON.stringify({"password": $(passInput).val()}),
                url: `https://${host}/api/v1/users/${getUserId()}`,
                success: function (data, textStatus) {
                    alert("Account deleted");
                    window.location.href = '/logout';
                }
            });
            $(document).on('ajaxError', function () {
                $('#error-info').css({ 'display': 'block' });
            });
        });
    }
});

function getUserId() {
    let cookieArray = document.cookie.split(';');

    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i].trim();
        if (cookie.indexOf('user_id') == 0) {
            return cookie.substring(('=user_id').length, cookie.length);
        }
    }
}
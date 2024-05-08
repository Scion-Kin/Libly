$(function () {
    let userId = getUserId;
    let count = 0;
    for (let i of $('#selection').children()) {
        $(i).click(function (){
            $.ajax({
                url: 'https://usenet.tech/api/v1/favs/genres',
                type: 'POST',
                headers: {'Content-Type': 'application/json'},
                data: JSON.stringify({
                  "user_id": userId,
                  "genre_id": i.id
                }),
                success: function (data, textStatus) {
                    count += 1;
                    $(i).css('background-color', '#059e54');
                    $('#done').val(count);
                }
            });
            $(document).on('ajaxError', function () {
                alert('Something went wrong. Please try again.')
            });
        });
    }

    function getUserId() {
        let cookieArray = document.cookie.split(';');

        for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i].trim();
            if (cookie.indexOf('user_id') == 0) {
                return cookie.substring(('=user_id').length, cookie.length);
            }
        }
    }
});

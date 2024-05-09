$(function () {
    let userId = getUserId();
    let count = 0;
    for (let i of $('#selection').children()) {
        $(i).find('button').click(function () {
            if (!$(i).find('button').attr('selected')) {
                $.ajax({
                    url: 'https://usernet.tech/api/v1/favs/genres',
                    type: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    data: JSON.stringify({
                        "user_id": userId,
                        "genre_id": $(i).find('button').attr('id')
                    }),
                    success: function (data, textStatus) {
                        count += 1;
                        $(i).find('button').css('background-color', '#059e54');
                        $(i).find('button').attr('selected', data.id);
                        $('#done').val(count);
                    }
                });
            }

            else {
                $.ajax({
                    url: `https://usernet.tech/api/v1/favs/genres/${$(i).attr('selected')}`,
                    type: 'DELETE',
                    success: function (data, textStatus) {
                        count -= 1;
                        $(i).find('button').css('background-color', '#316FF6');
                        $(i).find('button').removeAttr('selected');
                        $('#done').val(count);
                    }
                });
            }

            $(document).on('ajaxError', function ( event, jqxhr, settings, thrownError ) {
                alert('Something went wrong. Please try again.');
                console.log(thrownError);
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

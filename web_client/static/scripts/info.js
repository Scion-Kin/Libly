$(function () {

    const title = document.title.split(' ')[0];
    if (title === 'Info') {

        const url = `http://localhost:5000/api/v1/books`;

        $.ajax({
            type: 'GET',
            url: url,
            success: function (data, textStatus) {
                for (let i in data) {
                    let resource = document.createElement('section');
                    const resource_title = document.createElement('h4');
                    const resource_data_container = document.createElement('section');
                    const form = document.createElement('form');
                    const section = document.createElement('section');
                    const toInfo = document.createElement('button');
                    const toRead = document.createElement('button');
                    const img = document.createElement('img');
                    let resource_data = data[i].data;

                    $(toRead).click(function () {
                        window.location.href = `/read/${resource_data.id}`;
                    });

                    $(form).attr('method', 'POST');
                    $(img).attr('src', `/static/images/${resource_data.pic}`);
                    $(toInfo).text('Info & reviews');
                    $(toInfo).attr({'name': 'id', 'value': resource_data.id});
                    $(toRead).text('Read');
                    $(form).append(toInfo);
                    $(section).append(toRead);
                    $(resource_data_container).addClass('data');
                    $(resource_title).text(i);
                    $(resource_data_container).append([img,  resource_title]);
                    $(resource).append([resource_data_container, form, section]);
                    $(resource).addClass('resource');
                    $(resource).attr('id', resource_data.id);
                    $("#search_results").append(resource);
                }
            }
        });
        
    }

    else {
        if ($('#reviews')) {
            let reviews = $('#reviews').children();
            for (let i = 0; i < reviews.length; i++) {
                let imgId = $(reviews[i]).find('img').attr('id');
                let user_id = imgId.split('_')[1];
                $.get(`http://localhost:5000/api/v1/users/${user_id}`, function(data, textStatus) {
                    for (let j in data) {
                        $(`#${imgId}`).attr('src', '/static/images/' + data[j].data.pic);
                        break;
                    }
                });
            }
        }
    }

    $('#create').click(function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            headers: { 'Content-Type': 'application/json' },
            url: 'http://localhost:5000/api/v1/reviews',
            data: JSON.stringify({ 
                "user_id": getCookie(),
                "book_id": $('#make-review form').attr('id'),
                "text": $('#message').val()
            }),
            success: function (data, textStatus) {
                location.reload();
            }
        });
        $(document).on('ajaxError', function () {
            alert('Something went wrong, please try again later. If the problem persists, please let us know as soon as possible.');
        });
    });

    function getCookie() {
        let cookieArray = document.cookie.split(';');

        for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i].trim();
            if (cookie.indexOf('user_id') == 0) {
                return cookie.substring(('=user_id').length, cookie.length);
            }
        }
    }
});
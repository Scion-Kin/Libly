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
                $.get(`http://localhost:5000/api/v1/users/${imgId}`, function(data, textStatus) {
                    for (let j in data) {
                        $(`#${imgId}`).attr('src', '/static/images/' + data[j].data.pic);
                        break;
                    }
                });
            }
        }
    }
});

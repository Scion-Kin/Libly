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
                    const toInfo = document.createElement('button');
                    const toRead = document.createElement('button');
                    const img = document.createElement('img');
                    let resource_data = data[i].data;

                    $(img).attr('src', `/static/images/${resource_data.pic}`);

                    $(resource_data_container).addClass('data');
                    $(resource_title).text(i);
                    $(resource_data_container).append([img,  resource_title]);
                    $(resource).append(resource_data_container);
                    $(resource).addClass('resource');
                    $(resource).attr('id', resource_data.id);
                    $("#search_results").append(resource);
                }
            }
        });
    }
});

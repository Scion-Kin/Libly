$(function () {
    const title = document.title.split(' ')[1];

    const url = `http://localhost:5000/api/v1/${title.toLowerCase()}`

    $.ajax({
        type: 'GET',
        url: url,
        success: function (data, textStatus) {
            console.log(data);
            for (let i in data) {
                let resource = document.createElement('section');
                const resource_title = document.createElement('h4');
                $(resource_title).text(i);
                $(resource).append(resource_title);
                $(resource).addClass('resource');
                $("section.results").append(resource);
            }
        }
    });
});

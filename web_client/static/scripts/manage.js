$(function () {
    const title = document.title.split(' ')[1];
    
    const url = `http://localhost:5000/api/v1/${title.toLowerCase()}`

    $.ajax({
        type: 'GET',
        url: url,
        success: function (data, textStatus) {
            console.log(data);
        }
    });
});

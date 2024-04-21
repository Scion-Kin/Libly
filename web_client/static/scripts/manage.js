$(function () {
    const title = document.title.split(' ')[1];

    const url = `http://localhost:5000/api/v1/${title.toLowerCase()}`

    let displayed = false;
    $.ajax({
        type: 'GET',
        url: url,
        success: function (data, textStatus) {
            for (let i in data) {
                let resource = document.createElement('section');
                const resource_title = document.createElement('h4');
                const resource_data_container = document.createElement('section');
                const button_container = document.createElement('section');
                const edit = document.createElement('button');
                const trash = document.createElement('button');
                const img = document.createElement('img');
                let resource_data = data[i].data;

                if (title === 'Authors' || title === "Genres" || title === "Users") {
                    $(img).attr('src', `/static/images/${resource_data.pic}`);
                }
                else if (title === "Reviews") {
                    let imgUrl = `http://localhost:5000/api/v1/users/${resource_data.user_id}`;
                    $.get(imgUrl, function(data, textStatus) {
                        for (let k in data) {
                           $(img).attr('src', `/static/images/${data[k].data.pic}`);
                        }
                    });
                }

                $(edit).addClass('edit');
                $(trash).addClass('trash');
                $(resource_data_container).append(img, button_container);

                if (title === "Authors" || title === "Genres") {
                    if (data[i].book_list.length > 0) {
                        let book_list = document.createElement('ul');
                        $(book_list).addClass('book_list');
                        for (let j of data[i].book_list) {
                            let book = document.createElement('button');
                            $(book).text(j.title);
                            $(book_list).append(book);
                        }

                        const book_displayer = document.createElement('button');
                        $(book_displayer).click(function () {
                            if (displayed == false) {
                                $('.book_list').css('display', 'block');
                                $(book_displayer).text('Hide book list');
                                displayed = true
                            }
                            else {
                                $('.book_list').css('display', 'none');
                                $(book_displayer).text('See book list');
                                displayed = false;
                            }
                        });
                        $(book_displayer).text('See book list');
                        $(resource_data_container).append(book_list);
                        $(button_container).append(book_displayer);
                    }
                }

                else if (title === 'Users') {
                    let review_list = document.createElement('ul');
                    $(review_list).addClass('book_list');

                    $.get(`${url}/${resource_data.id}/reviews`, function(data, textStatus) {

                        if (textStatus == 'success') {
                            for (let j of data) {
                                let review = document.createElement('p');
                                $(review).text(j.text);
                                $(review_list).append(review);
                            }
    
                            let review_displayer = document.createElement('button');
                            $(review_displayer).click(function () {
                                if (displayed == false) {
                                    $('.book_list').css('display', 'block');
                                    $(review_displayer).text('Hide review list');
                                    displayed = true
                                }
                                else {
                                    $('.book_list').css('display', 'none');
                                    $(review_displayer).text('See review list');
                                    displayed = false;
                                }
                            });
                            $(review_displayer).text('See review list');
                            $(resource_data_container).append(review_list);
                            $(button_container).prepend(review_displayer);
                        }
                    });
                }
                
                $(edit).click(function () {
                    window.location.href = `${url}/${$(edit).parents()[2].id}`;
                });

                $(trash).click(function () {
                    window.location.href = `${url}/${$(trash).parents()[2].id}`;
                });

                $(button_container).append([edit, trash]);
                $(button_container).addClass('button_container');
                $(resource_data_container).addClass('data');
                $(resource_title).text(i);
                $(resource).append([resource_title, resource_data_container]);
                $(resource).addClass('resource');
                $(resource).attr('id', resource_data.id);
                $("section.results").append(resource);
            }
        }
    });
});

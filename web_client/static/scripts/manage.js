$(function () {
    const title = document.title.split(' ')[1];

    const url = `http://localhost:5000/api/v1/${title.toLowerCase()}`

    let displayed = false;

    function editDatabase(json, editUrl, method) {
        $.ajax({
            type: method,
            headers: { 'Content-Type': 'application/json'},
            data: JSON.stringify(json),
            url: editUrl,
            success: function (data, textStatus) {
                alert('Data updated');
                location.reload();
            }
        });
    }

    $(document).on('ajaxError', function () {
        $(errorInfo).css({'display': 'block'});
    });

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

                const form = document.createElement('section');
                let passInput = document.createElement('input');
                let errorInfo = document.createElement('p');
                $(passInput).attr('placeholder', 'Input your admin password');
                $(errorInfo).text('Wrong password. Try again.');
                $(errorInfo).css({'color': 'red', 'font-weight': 'bolder', 'display': 'none', 'margin': 'auto'});
                $(passInput).attr('type', 'password');
                $(form).attr({'class': 'confirm'});
                $(document.querySelector('main')).append(form);
                
                $(edit).click(function () {
                    let requestData = {};
                    const cancel = document.createElement('button');
                    let submit = document.createElement('input');
                    $(submit).attr('type', 'submit');
                    $(submit).text('Confirm');
                    $(cancel).attr('id', 'cancel');
                    $(cancel).text('X');
                    $(cancel).click(function () {
                        $(form).css('display', 'none');
                    });
                    $.get(`${url}/${$(edit).parents()[2].id}`, function (data, textStatus) {
                        if (textStatus === 'success') {
                            let realForm = document.createElement('form');
                            for (let i in data) {
                                for (let j in data[i].data) {
                                    let ignore = ['__class__', 'confirmed', 'id', 'created_at', 'updated_at'];
                                    if (!ignore.includes(j)) {
                                        let inputData = document.createElement('input');
                                        inputData.required = true;
                                        inputData.type = 'text';
                                        inputData.placeholder = j;
                                        inputData.id = j;
                                        inputData.value = data[i].data[j];
                                        $(realForm).append(inputData);
                                        requestData[j] = '';
                                    }
                                }
                            }
                            $(form).css({
                                'top': '80px', 'display': 'flex'
                            });
                            $(realForm).append(submit);
                            $(form).html([cancel, realForm]);
                        }
                    });
                    $(submit).click(function(e) {
                        e.preventDefault();

                        for (let i in requestData) {
                            requestData[i] = $(`#${i}`).val();
                        }
                        editDatabase(requestData, `${url}/${$(trash).parents()[2].id}`, 'PUT');
                    });
                });

                $(trash).click(function () {
                    let is = confirm('Are you sure you want to delete this resource? This is not reversible');
                    if (is === true) {
                        let button = document.createElement('button');
                        const cancel = document.createElement('button');
                        $(cancel).attr('id', 'cancel');
                        $(cancel).text('X');
                        $(cancel).click(function () {
                            $(form).css('display', 'none');
                        });
                        $(button).text('Confirm');
                        $(form).css({
                            'top': '80px', 'display': 'flex'
                        });
                        $(form).html([cancel, passInput, button, errorInfo]);
                        $(button).click(function() {
                            editDatabase({ password: passInput.value }, `${url}/${$(trash).parents()[2].id}`, 'DELETE');
                        });
                    }
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

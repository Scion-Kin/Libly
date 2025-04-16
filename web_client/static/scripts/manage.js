import { host } from "./API_HOST";

$(function () {
  const title = document.title.split(' ')[1];

  const url = `https://${host}/api/v1/${title.toLowerCase()}`;

  let displayed = false;

  $('#add-resource').click(function () {
    $('#new_resource').css('display', 'block');
    $('main').css('min-height', '1300px');
  });

  const genres = [];
  const authors = [];

  $('#new_resource input[type=checkbox].genre-id').on('change', function () {
    pushPop($(this).is(':checked'), genres, $(this).attr('id'), '#genres');
  });

  $('#new_resource input[type=checkbox].author-id').on('change', function () {
    pushPop($(this).is(':checked'), authors, $(this).attr('id'), '#authors');
  });

  function pushPop (isChecked, arr, id, where) {
    if (isChecked && !arr.includes(id)) {
      arr.push(id);
      $(where).val(arr);
    } else if (!isChecked && arr.includes(id)) {
      arr.splice(arr.indexOf(id), 1);
      $(where).val(arr);
    }
  }

  $('button.cancel').click(function () {
    $('#new_resource').css('display', 'none');
    $('main').css('min-height', '480px');
  });

  $.ajax({
    type: 'GET',
    url,
    success: function (data, textStatus) {
      for (const i in data) {
        const resource = document.createElement('section');
        const resourceTitle = document.createElement('h4');
        const resourceDataContainer = document.createElement('section');
        const buttonContainer = document.createElement('section');
        const edit = document.createElement('button');
        const trash = document.createElement('button');
        const img = document.createElement('img');
        const resourceData = data[i].data;

        if (title === 'Authors' || title === 'Genres' || title === 'Users' || title === 'Books') {
          $(img).attr('src', `/static/images/${resourceData.pic}`);
        } else if (title === 'Reviews') {
          const imgUrl = `https://${host}/api/v1/users/${resourceData.user_id}`;
          $.get(imgUrl, function (data, textStatus) {
            for (const k in data) {
              $(img).attr('src', `/static/images/${data[k].data.pic}`);
            }
          });
        }

        $(edit).addClass('edit');
        $(trash).addClass('trash');
        $(resourceDataContainer).append(img, buttonContainer);

        if (title === 'Authors' || title === 'Genres') {
          if (data[i].book_list.length > 0) {
            const bookList = document.createElement('ul');
            $(bookList).addClass('book_list');
            for (const j of data[i].book_list) {
              const book = document.createElement('button');
              $(book).text(j.title);
              $(bookList).append(book);
            }

            const bookDisplayer = document.createElement('button');
            $(bookDisplayer).click(function () {
              if (displayed === false) {
                $('.book_list').css('display', 'block');
                $(bookDisplayer).text('Hide book list');
                displayed = true;
              } else {
                $('.book_list').css('display', 'none');
                $(bookDisplayer).text('See book list');
                displayed = false;
              }
            });
            $(bookDisplayer).text('See book list');
            $(resourceDataContainer).append(bookList);
            $(buttonContainer).append(bookDisplayer);
          }
        } else if (title === 'Users') {
          const reviewList = document.createElement('ul');
          $(reviewList).addClass('book_list');

          $.get(`${url}/${resourceData.id}/reviews`, function (data, textStatus) {
            if (textStatus === 'success') {
              for (const j of data) {
                const review = document.createElement('p');
                $(review).text(j.text);
                $(reviewList).append(review);
              }

              const reviewDisplayer = document.createElement('button');
              $(reviewDisplayer).click(function () {
                if (displayed === false) {
                  $('.book_list').css('display', 'block');
                  $(reviewDisplayer).text('Hide review list');
                  displayed = true;
                } else {
                  $('.book_list').css('display', 'none');
                  $(reviewDisplayer).text('See review list');
                  displayed = false;
                }
              });
              $(reviewDisplayer).text('See review list');
              $(resourceDataContainer).append(reviewList);
              $(buttonContainer).prepend(reviewDisplayer);
            }
          });
        }

        const form = document.createElement('section');
        const passInput = document.createElement('input');
        const errorInfo = document.createElement('p');
        $(passInput).attr('placeholder', 'Input your admin password');
        $(errorInfo).text('An error code was returned. Make sure your password is right and try again.');
        $(errorInfo).css({ color: 'red', 'font-weight': 'bolder', display: 'none', margin: 'auto' });
        $(errorInfo).attr('id', 'error-info');
        $(passInput).attr('type', 'password');
        $(form).attr({ class: 'confirm' });
        $(document.querySelector('main')).append(form);

        $(edit).click(function () {
          const requestData = {};
          const cancel = document.createElement('button');
          const submit = document.createElement('input');
          const passInput = document.createElement('input');
          $(submit).attr('type', 'submit');
          $(submit).text('Confirm');
          $(cancel).attr('class', 'cancel');
          $(cancel).text('X');
          $(cancel).click(function () {
            $(form).css('display', 'none');
          });
          $.get(`${url}/${$(edit).parents()[2].id}`, function (data, textStatus) {
            if (textStatus === 'success') {
              const realForm = document.createElement('form');
              for (const i in data) {
                for (const j in data[i].data) {
                  const ignore = ['__class__', 'confirmed', 'id', 'created_at', 'updated_at'];
                  if (!ignore.includes(j)) {
                    const inputData = document.createElement('input');
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

              $(passInput).attr({ type: 'password', placeholder: 'input your admin password' });
              $(form).css({
                top: '80px', display: 'flex'
              });

              $(realForm).append([passInput, submit]);
              $(form).html([cancel, realForm]);
            }
          });
          $(submit).click(function (e) {
            e.preventDefault();

            for (const i in requestData) {
              requestData[i] = $(`#${i}`).val();
            }
            if (title === 'Users') {
              requestData.adminPassword = $(passInput).val();
            } else {
              requestData.password = $(passInput).val();
            }
            editDatabase(requestData, `${url}/${$(trash).parents()[2].id}`, 'PUT');
          });
        });

        $(trash).click(function () {
          const is = confirm('Are you sure you want to delete this resource? This is not reversible');
          if (is === true) {
            const button = document.createElement('button');
            const cancel = document.createElement('button');
            $(cancel).attr('class', 'cancel');
            $(cancel).text('X');
            $(cancel).click(function () {
              $(form).css('display', 'none');
            });
            $(button).text('Confirm');
            $(form).css({
              top: '80px', display: 'flex'
            });
            $(form).html([cancel, passInput, button, errorInfo]);
            $(button).click(function () {
              editDatabase({ password: passInput.value }, `${url}/${$(trash).parents()[2].id}`, 'DELETE');
            });
          }
        });

        $(buttonContainer).append([edit, trash]);
        $(buttonContainer).addClass('button_container');
        $(resourceDataContainer).addClass('data');
        $(resourceTitle).text(i);
        $(resource).append([resourceTitle, resourceDataContainer]);
        $(resource).addClass('resource');
        $(resource).attr('id', resourceData.id);
        $('section.results').append(resource);
      }
    }
  });

  function editDatabase (json, editUrl, method) {
    $.ajax({
      type: method,
      headers: { 'Content-Type': 'application/json' },
      data: JSON.stringify(json),
      url: editUrl,
      success: function (data, textStatus) {
        alert('Data updated');
        window.location.href = `/manage/${title.toLowerCase()}`;
      }
    });
    $(document).on('ajaxError', function () {
      $('#error-info').css({ display: 'block' });
    });
  }
});

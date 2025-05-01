import { host } from "./API_HOST.js";

$(function () {
  const userId = getUserId();
  let count = 0;
  for (const i of $('#selection').children()) {
    $(i).find('button').click(function () {
      if (!$(i).find('button').attr('selected')) {
        $.ajax({
          url: `https://${host}/api/v1/favs/genres`,
          type: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: JSON.stringify({
            user_id: userId,
            genre_id: $(i).find('button').attr('id')
          }),
          success: function (data, textStatus) {
            count += 1;
            $(i).find('button').css('background-color', '#059e54');
            $(i).find('button').attr('selected', data.id);
            $(i).find('button').attr('fav_id', data.id);
            $('#done').val(count);
          },
          error: function (jqxhr, textStatus, error) {
            console.log('Error:', error);
            alert('Something went wrong. Please try again.');
          }
        });
      } else {
        $.ajax({
          url: `https://${host}/api/v1/favs/genres/${$(i).find('button').attr('fav_id')}`,
          type: 'DELETE',
          success: function (data, textStatus) {
            count -= 1;
            $(i).find('button').css('background-color', '#316FF6');
            $(i).find('button').removeAttr('selected');
            $('#done').val(count);
          },
          error: function (jqxhr, textStatus, error) {
            console.log('Error:', error);
            alert('Something went wrong. Please try again.');
          }
        });
      }
    });
  }

  function getUserId () {
    const cookieArray = document.cookie.split(';');

    for (let i = 0; i < cookieArray.length; i++) {
      const cookie = cookieArray[i].trim();
      if (cookie.indexOf('user_id') === 0) {
        return cookie.substring(('=user_id').length, cookie.length);
      }
    }
  }
});

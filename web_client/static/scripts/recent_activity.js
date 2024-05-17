const reviews = document.getElementById('reviews');
const books = document.getElementById('books-activity');
const reviewsTitle = document.createElement('h4');
const booksTitle = document.createElement('h4');
const today = new Date();

books.appendChild(booksTitle);
reviews.append(reviewsTitle);

fetch('https://usernet.tech/api/v1/reviews')
  .then(function (response) { return response.json(); })
  .then(function (data) {
    if (!data.error) {
      reviewsTitle.textContent = 'Recent reviews:';

      for (const i in data) {
        const date = (data[i].data.updated_at).split('T')[0].split('-');

        // get data from the last 2 days
        if (Number(date[1]) === today.getMonth() + 1 && (today.getDate() - 2) <= Number(date[2])) {
          const review = document.createElement('section');
          const reviewText = document.createElement('p');
          const owner = document.createElement('section');
          const avatar = document.createElement('img');
          const name = document.createElement('p');
          const link = document.createElement('a');
          const form = document.createElement('form');
          const submit = document.createElement('button');
          const identifier = document.createElement('p');

          fetch(`https://usernet.tech/api/v1/books/${data[i].data.book_id}`)
            .then(function (response) { return response.json(); })
            .then(function (bookData) {
              if (!bookData.error) {
                for (const k in bookData) {
                  form.action = '/about/book';
                  form.method = 'POST';
                  submit.name = 'id';
                  submit.value = `${bookData[k].data.id}`;
                  submit.className = 'go';
                  identifier.innerHTML = `Reviewing on: <b>${bookData[k].data.title}</b>`;
                  identifier.style.fontStyle = 'italic';
                  identifier.style.textDecoration = 'underline';
                  identifier.style.fontSize = 'smaller';
                  identifier.style.opacity = '80%';
                  form.appendChild(identifier);
                  form.appendChild(submit);
                  form.style.display = 'flex';
                  form.style.gap = '5px';
                }
              }
            });

          fetch(`https://usernet.tech/api/v1/users/${data[i].data.user_id}`)
            .then(function (response) { return response.json(); })
            .then(function (userData) {
              if (!userData.error) {
                for (const j in userData) {
                  avatar.src = `/static/images/${userData[j].data.pic}`;
                  avatar.alt = `${userData[j].data.first_name}'s profile picture`;
                  name.textContent = `${userData[j].data.first_name} ${userData[j].data.middle_name} ${userData[j].data.last_name}`;
                  name.className = 'name';
                  link.href = `/profile/${userData[j].data.id}`;
                  link.appendChild(avatar);
                }
              }
            });

          owner.className = 'owner';
          owner.appendChild(link);
          reviewText.appendChild(name);
          reviewText.appendChild(form);
          reviewText.append(data[i].data.text);
          reviewText.className = 'text';
          review.className = 'review';
          review.appendChild(owner);
          review.appendChild(reviewText);
          reviews.appendChild(review);
        }
      }
      if (reviews.children.length < 2) {
        reviewsTitle.textContent = 'No recent reviews';
      }
    } else {
      reviewsTitle.textContent = 'No recent reviews';
    }
  });

fetch('https://usernet.tech/api/v1/books')
  .then(function (response) { return response.json(); })
  .then(function (data) {
    if (!data.error) {
      booksTitle.textContent = 'Recently added books';
      for (const i in data) {
        const date = (data[i].data.updated_at).split('T')[0].split('-');

        // get data from the last 2 days
        if (Number(date[1]) === today.getMonth() + 1 && (today.getDate() - 2) <= Number(date[2])) {
          const book = document.createElement('section');
          const button = document.createElement('button');

          button.textContent = data[i].data.title;
          button.addEventListener('click', function () {
            window.location.href = `/read/${data[i].data.id}`;
            localStorage.setItem(`${data[i].data.title}`, `${data[i].data.id}@${data[i].data.pic}`);
          });

          book.className = 'history-book';
          book.style.backgroundImage = `url('/static/images/${data[i].data.pic}')`;
          button.style.margin = '30px 20px';
          button.style.maxWidth = '240px';
          book.appendChild(button);
          books.append(book);
        }
      }
      if (books.children.length < 2) {
        booksTitle.textContent = 'No new books';
        booksTitle.style.margin = 'auto';
      }
    } else {
      booksTitle.textContent = 'No new books';
      booksTitle.style.margin = 'auto';
    }
  });

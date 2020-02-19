 document.addEventListener('DOMContentLoaded', () => {

      function post() {

        const request = new XMLHttpRequest();
        request.open('POST', '/get_market');

        request.onload = () => {
            const data = JSON.parse(request.responseText);
            const money = `${data.money}`
            const wood = `${data.wood}`
            const rock = `${data.rock}`
            document.querySelector('#money').innerHTML = money;
            document.querySelector('#wood').innerHTML = wood;
            document.querySelector('#rock').innerHTML = rock;
      }

        const data = new FormData();
        data.append('NULL', "NULL");
        request.send(data);
        return false;
      };
      post();
      window.setInterval(post, 5000);

 });


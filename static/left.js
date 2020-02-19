 document.addEventListener('DOMContentLoaded', () => {

      function get_gametime() {

        const request = new XMLHttpRequest();
        request.open('POST', '/get_gametime');

        request.onload = () => {
            const data = JSON.parse(request.responseText);
            document.querySelector('#gametime').innerHTML = `${data.gametime}`;
      }

        const data = new FormData();
        data.append('NULL', "NULL");
        request.send(data);
        return false;
      };
      get_gametime();
      window.setInterval(get_gametime, 5000);

 });


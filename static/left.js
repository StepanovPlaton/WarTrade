 document.addEventListener('DOMContentLoaded', () => {

      function getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
      }

      function get_gametime() {

        const request = new XMLHttpRequest();
        request.open('POST', '/get_gametime');

        request.onload = () => {
            const data = JSON.parse(request.responseText);
            document.querySelector('#gametime').innerHTML = `${data.gametime}`;
      }

        const data = new FormData();
        const login = getCookie("login");
        const password = getCookie("password");
        console.log(login + ":"+ password);
        data.append('login', login);
        data.append('password', password);
        request.send(data);
        return false;
      };
      get_gametime();
      window.setInterval(get_gametime, 5000);

 });


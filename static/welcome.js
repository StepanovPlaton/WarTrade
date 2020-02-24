
$(document).ready(function() {
  console.log(document.cookie);
    $('#send_login').on('click', function() {
      const request = new XMLHttpRequest();
      request.open('POST', '/login');
      request.onload = () => {
          const data = JSON.parse(request.responseText);
          if(`${data.answer}`.search("LOGINOK") == -1) { document.querySelector('#ERROR').innerHTML = `${data.answer}`; }
          else { document.location.href = "http://192.168.32.10:5001/start.html?login=123&password=12345"; }
      }
      const data = new FormData();
      
      const login = document.querySelector('#login').value;
      const password = document.querySelector('#password').value;
      data.append('login', login);
      data.append('password', password);
      document.cookie = `login=${login};`;
      document.cookie = `password=${password};`;
      
      request.send(data);
      return false;
    });
});


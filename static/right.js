 document.addEventListener('DOMContentLoaded', () => {

      function get_graph() {

        const request = new XMLHttpRequest();
        request.open('POST', '/get_graph');

        request.onload = () => {
            const data = JSON.parse(request.responseText);
            document.querySelector('#graph').innerHTML = `<img src="static/graphs/${data.graph}.png" >`;
      }

        const data = new FormData();
        data.append('NULL', "NULL");
        request.send(data);
        return false;
      };
      get_graph();
      window.setInterval(get_graph, 5000);

 });


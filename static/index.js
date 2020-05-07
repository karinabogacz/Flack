document.addEventListener('DOMContentLoaded', () => {

  // Make sure button is diabled if no text provided
  document.querySelector('.button-modal').onclick = () => {
    document.querySelector('.button-form').disabled = true;
    document.querySelector('.form-control').onkeyup = () =>{
      if (document.querySelector('.form-control').value.length > 0)
        document.querySelector('.button-form').disabled = false;
      else
        document.querySelector('.button-form').disabled = true;
    };
  };

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // Send provided by user channel name to the server by emiting a new event
  socket.on('connect', () => {

    document.querySelector('.button-form').onclick = () => { 
      const channel = document.querySelector('.form-control').value;
      socket.emit('create channel', {'channel': channel});
      document.querySelector('.form-control').value = '';
      };
    });
  
  // Create a new channel announcing to everyone
  socket.on('announce channel', data => {
      const li = document.createElement('li');
      li.innerHTML = `# ${data.channel}`;
      li.className = 'list-group-item';
      document.querySelector('.channels').append(li);
      return false;
  });
});

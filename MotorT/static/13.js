socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    socket.emit('client_connected', {data: 'New client!'});
});

$(document).ready(function(){
    $('#heldButtonEast').mousedown(function(){
      let rasp = document.getElementById('heldButtonEast') 
      console.log(rasp.name + ' on')
      console.log("mouse down is called")
      socket.emit('relay_on_east');
    });
  });


 $(document).ready(function(){
    $('#heldButtonEast').mouseup(function(){
       console.log("mouse up is called")
       let rasp = document.getElementById('heldButtonEast')
       console.log(rasp.name)
       socket.emit('relay_off_east');
    });
  });


 $(document).ready(function(){
    $('#heldButtonWest').mousedown(function(){
      console.log("mouse down is called")
      let rasp = document.getElementById('heldButtonWest')
      socket.emit('relay_on_west')
    });
  });


 $(document).ready(function(){
    $('#heldButtonWest').mouseup(function(){
      console.log("mouse up is called")
      let rasp = document.getElementById('heldButtonWest')
      console.log(rasp.name)
      socket.emit('relay_off_west')
    });
  });

function east_for_duration() {
    console.log("east_for_duration")
    socket.emit('east_for_duration')
}

function west_for_duration() {
    console.log("west_for_duration")
    socket.emit('west_for_duration')
}

function start_solar_predicting() {
    console.log("slave pi called")
    console.log("solar predicting")
    socket.emit('track')
}

function go_to_vertical() {
    console.log("go to vertical")
    socket.emit('go_to_vertical')
}

function go_to_horizontal() {
    console.log("go to horizontal")
    socket.emit('go_to_horizontal')
}

function halt_movement() {
    console.log("halting solar panel")
    socket.emit('halt')

}

function start_solar_loop() {
    console.log("slave pi called")
    console.log("solar loop")
    socket.emit('loop')
}

function halt_solar_loop() {
    console.log("slave pi called")
    console.log("solar predicting")
    socket.emit('halt_solar_loop')
}


socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    socket.emit('client_connected', {data: 'New client!'});
});

function disablebuttons(buttonToNotDisable)
{
    
    let parent = document.getElementById('buttons')
    if(parent === null) return
    let  children = parent.childNodes
    for( let i = 0; i < children.length; i++)
    {
        if(children[i].id !== 'halt' && children[i].id !== buttonToNotDisable)
        {
            console.log(children[i])
            children[i].disabled = true
        }
    }
    console.log("HELLO DISABLE")
}

//disable buttons on startup

function enablebuttons()
{
    console.log("enable buttons")
    let parent = document.getElementById('buttons')
    if(parent === null)
        return
    console.log( parent)
    let children = parent.childNodes
    for( let i = 0; i < children.length; i++)
    {
        children[i].disabled = false
    }
}


    $(document).ready(function(){
      $('#heldButtonEast').mousedown(function(){
      let rasp = document.getElementById('heldButtonEast')
      disablebuttons('heldButtonEast') 
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
       halt_movement()
    });
  });


 $(document).ready(function(){
    $('#heldButtonWest').mousedown(function(){
      console.log("mouse down is called")
      let rasp = document.getElementById('heldButtonWest')
      disablebuttons('heldButtonWest') 
      socket.emit('relay_on_west')
    });
  });


 $(document).ready(function(){
    $('#heldButtonWest').mouseup(function(){
      console.log("mouse up is called")
      let rasp = document.getElementById('heldButtonWest')
      console.log(rasp.name)
      halt_movement()
    });
  });

function start_solar_predicting() {
    console.log("slave pi called")
    console.log("solar predicting")
   // disablebuttons()
    socket.emit('track')
}

function go_to_evening_position() {
    console.log("go to vertical")
   // disablebuttons() 
    socket.emit('go_to_evening_position')
}

function go_to_morning_position() {
    console.log("go to morning position")
   // disablebuttons() 
    socket.emit('go_to_morning_position')
}

socket.on('update_alert', function update_alert(message)
{
    console.log("update_alert")
    let alert = document.getElementById('lastPressed')
      alert.innerHTML = message
    console.log("hey hey")

})


function halt_movement() {
    console.log("halting solar panel")
    socket.emit('halt')
    socket.emit('is_client_connected')

}

socket.on("disableButtons", function disable_buttons(nButton)
{
    console.log("disable buttons")
    disablebuttons(nButton)
    console.log("after disable buttons")
})

socket.on("enableButtons", function enable_buttons()
{
    console.log("halt recieved")
    enablebuttons() 
    console.log("after enable buttons")
})


socket.on('rotate_panel_animation_js', function set_animation(amountToChange)
{
     amountToRotate = amountToChange
     console.log(amountToRotate)
    $("#container").css({ transform: 'rotate(' + amountToRotate + 'deg)'})
    digits = document.getElementById("angle")
    roundedValue = amountToRotate.toFixed(2)
   angle.innerHTML = roundedValue + " degrees"

   console.log("hey")
})

function calibrate(){
    console.log("calibrate")
   // disablebuttons()
    socket.emit("calibrate")

}

function move_to_22_degrees(){
    console.log("move_to_22_degrees")
  //  disablebuttons()
    socket.emit("move_to_22_degrees")
}

function onload_set_animation(currentAngleOfPanel) {
    console.log(currentAngleOfPanel)
    $("#container").css({ transform: 'rotate(' + currentAngleOfPanel+ 'deg)'})
 

   console.log("hey")
}

function shut_off()
{
    console.log("shut off called")
    socket.emit("shut_off")
}

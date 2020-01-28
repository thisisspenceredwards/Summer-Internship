function openMyMenu(raspberrybase10) {
      console.log("This is raspberry")
      console.log(raspberrybase10)
      raspberry = ""
      raspberry+=(raspberrybase10.toString(16))
      let buttons = []


      buttons.push(document.getElementById("heldButtonWest"))
      buttons.push(document.getElementById("heldButtonEast"))
      buttons.push(document.getElementById("solarPredict"))
      buttons.push(document.getElementById("vertical"))
      buttons.push(document.getElementById("horizontal"))
      buttons.push(document.getElementById("halt"))




      console.log("this is buttons length")
      console.log(buttons.length)
      console.log(buttons[1])
      for (let  i=0; i < buttons.length;i++)
      {
         buttons[i].name = raspberry
          console.log(buttons[i])

      }
      menu = document.getElementById("myMenu")
      //alrt = document.getElementById("messageStatus")
      menu.style.height = "35%"
      //alrt.style.height = "100%"
      menu.style.zIndex="10";
      //alrt.style.zIndex="15"
      //alrt.style.opacity = "1"
      document.getElementById("myMenu-Content").style.height = "35%";
//      span = document.getElementById("navSpan")
//      fadeOut(span, 0.2)
}

   function closeMyMenu() {
      nav = document.getElementById("myNav")
      //alrt = document.getElementById("messageStatus")
      if(nav.style.width === "100%")
         { return }
      menu = document.getElementById("myMenu")
      menu.style.height = "0%";
      //alrt.style.opacity = "0";
      //alrt.style.height = "0%";
 //     span = document.getElementById("navSpan")
 //     fadeIn(span, 0.2)

}
//DROP DOWN MENU CLOSING LOGIC

let state = "open"

 $(document).on('click', function(e){
          if(e.target.type != "button" && e.target.id !== "toast" &&  e.target.id !== "myMenu" && e.target.id !== "buttonGroup" && state === "close")
          {
              console.log("close drop down menu")
              closeMyMenu()
              state = "open"
          }
          else 
          {
            menu = document.getElementById("myMenu")
            console.log(menu.style.height)
            if(menu.style.height > '34%')
            {
               console.log("i === 0")
               state = "close"
               console.log(state)
          }
      }
  })

//PUSH NOTIFICATIONS
let timeout;
let x=10000;
socket.on('pushNotification',function(data) {
            console.log("pushNotification")
           clearTimeout(timeout)
           console.log(data)
           alrt = document.getElementById("toast")
           alrt.innerHTML = data
           alrt.style.height = "35%"
           alrt.style.opacity = "1"
           alrt.style.zIndex = "15"
           timeout = setTimeout(function(){
           	alrt.style.height = "0%"
           	alrt.style.opacity = "0"
           	alrt.style.zIndex = "0" 
          }, x)
     })

/* Jquery Routes */

socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    socket.emit('client_connected', {data: 'New client!'});
});


$(document).ready(function(){
    $('#solarPredict').click(function(){
      let rasp = document.getElementById('solarPredict')
      console.log(rasp.name)
      console.log('solarPredict is called')
      let message = JSON.stringify({
                       "topic" : rasp.name,
                       "message": 'start_solar_predicting predicting',
                       "qos": 2
                     })
      console.log(message)
      socket.emit('sendMessage', message);
    })
   })

$(document).ready(function(){
    $('#vertical').click(function(){
      let rasp = document.getElementById('vertical')
      console.log(rasp.name)
      console.log('vertical is called')
      let message = JSON.stringify({
                       "topic" : rasp.name,
                       "message": 'go_to_max_angle vertical',
                       "qos": 2
                     })
      console.log(message)
      socket.emit('sendMessage', message);
    })
   })

$(document).ready(function(){
    $('#horizontal').click(function(){
      let rasp = document.getElementById('horizontal')
      console.log(rasp.name)
      console.log('horizontal is called')
      let message = JSON.stringify({
                       "topic" : rasp.name,
                       "message": 'go_to_max_angle horizontal',
                       "qos": 2
                     })
      console.log(message)
      socket.emit('sendMessage', message);
    })
   })


$(document).ready(function(){
    $('#halt').click(function(){
      let rasp = document.getElementById('halt')
      console.log(rasp.name)
      console.log('halt is called')
      let message = JSON.stringify({
                       "topic" : rasp.name,
                       "message": 'halt_solar_panel halt',
                       "qos": 2
                     })
      console.log(message)
      socket.emit('sendMessage', message);
    })
   })

$(document).ready(function(){
    $('#heldButtonEast').mousedown(function(){
      let rasp = document.getElementById('heldButtonEast') 
      console.log(rasp.name + ' on')
      console.log("mouse down is called")
      let message = JSON.stringify({
                      "topic" : rasp.name,
                      "message": 'relay_on east',
                      "qos": 2
                     })
      console.log(message)
      socket.emit('sendMessage', message)
    })
  })


 $(document).ready(function(){
    $('#heldButtonEast').mouseup(function(){
       console.log("mouse up is called")
       let rasp = document.getElementById('heldButtonEast')
       console.log(rasp.name)
       let message = JSON.stringify({
                      "topic" : rasp.name,
                      "message": 'relay_off east',
                      "qos": 2
                     })
       socket.emit('sendMessage', message)
    })
  })

$(document).ready(function(){
    $('#heldButtonWest').mousedown(function(){
      console.log("mouse down is called")
      let rasp = document.getElementById('heldButtonWest')
      console.log(rasp.name)
      let message = JSON.stringify({
                      "topic" : rasp.name,
                      "message": 'relay_on west',
                      "qos": 2
                     })
      socket.emit('sendMessage', message)
    });
  });

 $(document).ready(function(){
    $('#heldButtonWest').mouseup(function(){
      console.log("mouse up is called")
      let rasp = document.getElementById('heldButtonWest')
      console.log(rasp.name)
      let message = JSON.stringify({
                      "topic" : rasp.name,
                      "message": 'relay_off west',
                      "qos": 2
                     })
      socket.emit('sendMessage', message)
    });
  });


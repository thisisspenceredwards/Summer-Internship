     $("#container").velocity({
                         properties: { rotateZ: "360deg"},
                         options: {loop: false,duration: 1000, easing: "linear"}
                       })

let amountToRotate = 0;
function test() {
     amountToRotate+=45
     console.log(amountToRotate)
    $("#container").css({ transform: 'rotate(' + amountToRotate + 'deg)'})
                       

   console.log("hey")
}


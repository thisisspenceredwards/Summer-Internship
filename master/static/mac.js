/*let bootStrapButton= undefined
let CB = undefined
{% for mac in macList %}
   document.getElementById("{{mac}}").addEventListener("mouseup", function(){
   if(bootStrapButton === "{{mac}}")
   {
      bootStrapButton = undefined
      document.getElementById("{{mac}}").className = "btn btn-primary btn-lg mb-3"

   }
   else
   {
      if(bootStrapButton === undefined)
      {
         bootStrapButton = "{{mac}}"
         document.getElementById("{{mac}}").className = "btn btn-warning btn-lg mb-3"
      }
   }
   console.log("{{mac}}")
   })
{% endfor %}

*/
class ButtonSvgContainer
{
  constructor()
  {
      this.selectedSvg = undefined
      this.selectedButton = undefined
      this.svgHolder = []
      this.buttonHolder = []
      let svgBox = document.createElementNS("http://www.w3.org/2000/svg", "svg")
      svgBox.setAttribute("viewBox", "0 0 800 600")
      svgBox.setAttribute("width", "100%")
      svgBox.setAttribute("height", "100%")
      svgBox.setAttribute("id", "svgBox")
      let div = document.getElementById("boundary")
      div.appendChild(svgBox)
  }
  updateSvg(rect)
  {
    console.log("hey")
    if(this.selectedSvg === undefined && this.selectedButton !== undefined)
      {
         this.selectedSvg = rect
         rect.changeColor("green")
      }
      else if(this.selectedSvg !== undefined && this.selectedSvg !== rect)
      {
         console.log(this.selectedSvg)
         this.selectedSvg.changeColor("blue")
         this.selectedSvg = rect
         rect.changeColor("red")
      }
      else if(this.selectedSvg === rect)
      {
         this.selectedSvg = undefined
         rect.changeColor("blue")
      }
      else
      {
        this.selectedSvg = rect
        rect.changeColor("red")
      }

  }
  addSvg(svg)
  {
     this.svgHolder.push(svg)
     svgBox.appendChild(svg.getRectangle())
  }
  addButton(button)
  {
     console.log(button)
     this.buttonHolder.push(button)
  }
removeButton(button)
  {
    for( let i = 0; i < this.buttonHolder.length; i++)
     {
        if( this.buttonHolder[i] === rect)
        {
           this.buttonHolder.splice(i, 1);
        }
     }
  }
  removeSvg(rect)
  {
     for( let i = 0; i < this.svgHolder.length; i++)
     {
        if( this.svgHolder[i] === rect)
        {
           this.svgHolder.splice(i, 1);
        }
     }

  }
}



class Rectangle{
       rectangle = this

   constructor(width, height, x, y)
   {
         console.log(this.rectangle)
       this.observerHolder = []
       this.connectedTo = undefined
       this.rect = document.createElementNS("http://www.w3.org/2000/svg", "rect")
       this.rect.setAttribute("x", x)
       this.rect.setAttribute("y", y)
       this.rect.setAttribute("width", width)
       this.rect.setAttribute("height", height)
       this.rect.setAttribute("stroke", "white")
       this.rect.setAttribute("fill", "blue")
       this.rect.setAttribute("type", "button")
       this.addEventListener()
   }
   registerObserver(observer)
   {
     this.observerHolder.push(observer)
   }

unregisterObserver(observer)
   {
      for(let i = 0; i< observerHolder.length; i++)
      {
         if(observerHolder[i] === observer)
           {
             observerHolder.splice(i, 1)
             return true
           }
      }
      return false
   }
   addEventListener()
   {
      let rectangleClass= this
      this.rect.addEventListener("mouseup", function(){
      console.log(rectangleClass)
      console.log(this)
      rectangleClass.notifyObservers(rectangleClass)
      })

   }
   notifyObservers(rect)
   {
      console.log(rect)
      for(let i=0; i < this.observerHolder.length; i++)
      {
          this.observerHolder[i].updateSvg(rect)
      }
   }
   getRectangle()
   {
     return this.rect
   }
   setConnection(raspberry)
   {
   }
 removeConnection()
   {
   }
   changeColor(color)
   {
     this.rect.setAttribute("fill", color)
   }
}


let container = new ButtonSvgContainer()
let rect1 = new Rectangle("25vh", "50vh", "20vh", "20vh")
let rect2 = new Rectangle("25vh", "50vh","50vh", "20vh")
rect1.registerObserver(container)
rect2.registerObserver(container)
container.addSvg(rect1)
container.addSvg(rect2)
//let myRects = Array.from(svgBox.querySelectorAll("rect"))
//console.log(myRects)




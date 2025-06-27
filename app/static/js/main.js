console.log("🚀 main.js run ...")
console.log("------------------")

function onAnimationCompleted(){
  console.log('animation completed')
}


function init(){

  const main = document.getElementsByTagName('main')[0]
  //below meaning : if main on the DOM has a class named 'landing__main' then ...
  if(main.classList.contains('landing__main')){
    console.log('[on landing__main]')
    gsap.from('.landing__h1', {
        y: -50,
        duration: 2,
        onComplete:onAnimationCompleted
    })

  } else {
    console.log('[not on landing__main]')

  }



}


//function definition
function onDomContentLoaded(event) {
    gsap.registerPlugin(ScrollTrigger)

    init()
     
    
}


// below, the onDomContentLoaded function is used as a callback function
document.addEventListener("DOMContentLoaded", onDomContentLoaded);

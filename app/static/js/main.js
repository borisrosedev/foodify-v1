console.log("🚀 main.js run ...")
console.log("------------------")

function onAnimationCompleted(){
  console.log('animation completed')
}

function liveToastInit(contextualToastTrigger, contextualLiveToast){
  console.log('🚀 LiveToast Initialized , contextualLiveToast: ', contextualLiveToast)
  const toastTrigger = document.getElementById(contextualToastTrigger)
  if(!toastTrigger)  return;
  const liveToast = document.getElementById(contextualLiveToast)

  if (toastTrigger) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(liveToast)
    toastTrigger.addEventListener('click', () => {
      toastBootstrap.show()
    })
  }
}


function init() {
  const main = document.getElementsByTagName('main')[0];
  console.log('main', main);
  console.log(main.classList);

  if (main.classList.contains('landing__main')) {
    console.log('[on landing__main]');
    gsap.from('.landing__h1', {
      y: -50,
      duration: 2,
      onComplete: onAnimationCompleted
    });
  } else if (main.classList.contains('home__main')) {
    liveToastInit('home-live-toast-trigger','home-live-toast');
  } else if (main.classList.contains('dashboard__main')) {

    gsap.from('.dashboard__message-button', {
      y: 20,
      repeat: 3,
      repeatDelay: 2,
      ease: 'bounce.in'
    })


    console.log('dashboard');
    liveToastInit('dashboard-live-toast-trigger','dashboard-live-toast');


  } else if (main.classList.contains('login__main')) {
    console.log('login');
    liveToastInit('login-live-toast-trigger','login-live-toast');
  } else if (main.classList.contains('signup__main')) {
    console.log('signup');
    liveToastInit('signup-live-toast-trigger', 'signup-live-toast');
  } else {
    liveToastInit('default-live-toast-trigger', 'default-live-toast');
  }
}


//function definition
function onDomContentLoaded(event) {
    gsap.registerPlugin(ScrollTrigger)

    init()
     
    
}


// below, the onDomContentLoaded function is used as a callback function
document.addEventListener("DOMContentLoaded", onDomContentLoaded);

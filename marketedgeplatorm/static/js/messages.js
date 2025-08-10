function fadeOut(element, duration) {
    let opacity = 1;
    const intervalTime = 200; // Milliseconds per step
    const steps = duration / intervalTime;
    const opacityDecrement = opacity / steps;
  
    const fadeInterval = setInterval(() => {
      if (opacity > 0) {
        opacity -= opacityDecrement;
        element.style.opacity = opacity;
      } else {
        clearInterval(fadeInterval);
        element.style.display = 'none'; // Hide the element completely
      }
    }, intervalTime);
  }

document.addEventListener('DOMContentLoaded', function() {
    var message_ele = document.getElementById("message_container");
    if (message_ele) { // Check if the element exists
        fadeOut(message_ele, 3000);
    }
});
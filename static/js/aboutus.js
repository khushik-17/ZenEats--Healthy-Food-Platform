document.addEventListener("DOMContentLoaded", function () {
    let currentIndex = 0;
    const slides = document.querySelectorAll(".fade");
  
    if (slides.length === 0) {
      console.error("No elements with class 'fade' found.");
      return;
    }
  
    function showSlides() {
      slides.forEach((slide, index) => {
        slide.classList.remove("active");
        if (index === currentIndex) {
          slide.classList.add("active");
        }
      });
  
      currentIndex = (currentIndex + 1) % slides.length;
    }
  
    setInterval(showSlides, 3000);
    showSlides();
  });
  
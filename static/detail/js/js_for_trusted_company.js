  document.addEventListener("DOMContentLoaded", function () {
    var mySwiper = new Swiper('.custom-swiper-container .custom-swiper-wrapper', {
      direction: 'horizontal',
      loop: true,
      slidesPerView: 6,
      spaceBetween: 1,
      speed: 5000,
      autoplay: {
        delay: 2500,
        disableOnInteraction: false,
      }
    });
  });
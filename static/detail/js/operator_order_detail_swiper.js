  var swiper = new Swiper('.swiper', {
      direction: 'horizontal',
      loop: true,
      slidesPerView: 3,  // Устанавливаем количество видимых слайдов
      spaceBetween: 20,  // Устанавливаем пространство между слайдами в пикселях
      speed: 5000,  // Устанавливаем скорость анимации в 5000 миллисекунд
      autoplay: {
          delay: 2500,
          disableOnInteraction: false,
      },
  });
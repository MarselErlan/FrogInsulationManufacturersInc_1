            var topProductsSwiper = new Swiper('.top-products-swiper', {
    direction: 'horizontal',
      loop: true,
      slidesPerView: 4,  // Устанавливаем количество видимых слайдов
      spaceBetween: 2,  // Устанавливаем пространство между слайдами в пикселях
      speed: 5000,  // Устанавливаем скорость анимации в 5000 миллисекунд
      autoplay: {
          delay: 2500,
          disableOnInteraction: false,
      },      // Бесконечный цикл
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

});
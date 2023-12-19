var recommendedProductsSwiper = new Swiper('.recommended-products-swiper', {
    // параметры слайдера
    navigation: {
        nextEl: '.custom-swiper-next-recommended',
        prevEl: '.custom-swiper-prev-recommended',
    },
    direction: 'horizontal',
  loop: true,
  slidesPerView: 4,  // Устанавливаем количество видимых слайдов
  spaceBetween: 20,  // Устанавливаем пространство между слайдами в пикселях
  speed: 5000,  // Устанавливаем скорость анимации в 5000 миллисекунд
  autoplay: {
      delay: 2500,
      disableOnInteraction: false,
  },
    // другие параметры
});
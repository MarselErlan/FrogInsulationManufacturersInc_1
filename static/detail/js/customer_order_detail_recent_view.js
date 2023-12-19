    var recentViewsSwiper = new Swiper('.recent-views-swiper', {
        direction: 'horizontal',
      loop: true,
      slidesPerView: 2,  // Устанавливаем количество видимых слайдов
      spaceBetween: 5,  // Устанавливаем пространство между слайдами в пикселях
      speed: 5000,  // Устанавливаем скорость анимации в 5000 миллисекунд
      autoplay: {
          delay: 2500,
          disableOnInteraction: false,
      },
      navigation: {
          nextEl: '.custom-swiper-next',
          prevEl: '.custom-swiper-prev',
        },
    });



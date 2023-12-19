// Инициализация нового Swiper слайдера с уникальными классами
var mySwiper = new Swiper('.mySwiper', {
  // Основные настройки
  direction: 'horizontal', // горизонтальное направление прокрутки
  loop: true,              // бесконечный цикл прокрутки
  slidesPerView: 1,        // количество слайдов для отображения
  spaceBetween: 30,        // пространство между слайдами

  // Автовоспроизведение
  autoplay: {
    delay: 2500,            // задержка между прокруткой слайдов
    disableOnInteraction: false, // продолжать после взаимодействия
  },

  // Эффект переключения слайдов
  effect: 'fade',          // эффект "затухания"
  fadeEffect: {
    crossFade: true        // плавное перекрёстное исчезновение
  },

  // Навигация
  navigation: {
    nextEl: '.mySwiper-button-next', // кнопка "следующий слайд"
    prevEl: '.mySwiper-button-prev', // кнопка "предыдущий слайд"
  },

  // Пагинация
  pagination: {
    el: '.mySwiper-pagination',      // элемент пагинации
    type: 'fraction',                // тип пагинации (числа)
    clickable: true,                 // возможность выбора страницы
  },
});
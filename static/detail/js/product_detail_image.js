$(document).ready(function() {

    // Инициализация Swiper для миниатюр
var swiper = new Swiper('.thumbnails', {
    direction: 'vertical',
      loop: true,
      slidesPerView: 'auto',  // Устанавливаем количество видимых слайдов
      spaceBetween: 1,  // Устанавливаем пространство между слайдами в пикселях
      speed: 5000,  // Устанавливаем скорость анимации в 5000 миллисекунд
      autoplay: {
          delay: 2500,
          disableOnInteraction: false,
      },
  });




    // Получение URL-адресов миниатюр из Swiper слайдов
    var thumbnails = $('.swiper-slide .thumbnail-item').map(function() {
        return $(this).attr('src');
    }).get();

    // Начальное состояние счетчика изображений
    var currentImageIndex = 0;

    // Обработчик клика для миниатюр
    $('.swiper-slide .thumbnail-item').click(function() {
        var clickedImageSrc = $(this).attr('src'); // Получаем URL изображения
        $('#main-image').attr('src', clickedImageSrc); // Обновляем главное изображение
    });


    // Обработчик клика для кнопки "Следующее изображение"
    $('#next-image-btn').click(function() {
        currentImageIndex = (currentImageIndex + 1) % thumbnails.length;
        $('#main-image').attr('src', thumbnails[currentImageIndex]);
        swiper.slideToLoop(currentImageIndex); // Синхронизация с Swiper
    });

    // Обработчик клика для кнопки "Предыдущее изображение"
    $('#prev-image-btn').click(function() {
        currentImageIndex = (currentImageIndex - 1 + thumbnails.length) % thumbnails.length;
        $('#main-image').attr('src', thumbnails[currentImageIndex]);
        swiper.slideToLoop(currentImageIndex); // Синхронизация с Swiper
    });

    // Запуск автопрокрутки миниатюр с задержкой после выбора миниатюры
    setTimeout(function () {
        if (isAutoplayEnabled) {
            swiper.autoplay.start();
        }
    }, autoplayDelay);
});


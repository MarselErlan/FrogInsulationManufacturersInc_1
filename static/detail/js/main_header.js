window.addEventListener('scroll', function() {
    var heroContent = document.querySelector('.hero-content');
    var userArea = document.querySelector('.user-area');
    var heroImg = document.querySelector('.hero-img');
    var scrollPosition = window.scrollY;
    var triggerPosition = window.innerHeight / 3; // Измените на другое значение, если нужно изменить точку начала анимации

    if (heroContent && userArea && heroImg) {
      if (scrollPosition >= triggerPosition) {
        heroContent.classList.add('animated');
        userArea.classList.add('animated');
      } else {
        heroContent.classList.remove('animated');
        userArea.classList.remove('animated');
      }

      if (scrollPosition >= triggerPosition / 2) {
        heroImg.classList.add('animated');
        // Активируем анимацию для абзаца и списка пользователей
        document.querySelectorAll('.animated-p, .animated-ul').forEach(function(element) {
          element.classList.add('show');
        });
      } else {
        heroImg.classList.remove('animated');
        // Деактивируем анимацию для абзаца и списка пользователей
        document.querySelectorAll('.animated-p, .animated-ul').forEach(function(element) {
          element.classList.remove('show');
        });
      }
    }
  });
  // Функция для анимации числовых значений
  function animateValue(id, start, end, duration) {
    let obj = document.getElementById(id);
    let startTime = null;

    // Функция анимации
    function animation(currentTime) {
      if (startTime === null) startTime = currentTime;
      let timeElapsed = currentTime - startTime;
      let next = Math.round(easeInOutQuad(timeElapsed, start, end - start, duration));
      obj.innerHTML = next;
      if (timeElapsed < duration) {
        requestAnimationFrame(animation);
      } else {
        obj.innerHTML = end; // Убедимся, что останавливаемся на конечном значении
      }
    }

    requestAnimationFrame(animation);
  }

  // Функция "easeInOutQuad" для плавного начала и завершения анимации
  function easeInOutQuad(t, b, c, d) {
    t /= d/2;
    if (t < 1) return c/2*t*t + b;
    t--;
    return -c/2 * (t*(t-2) - 1) + b;
  }

// Используем IntersectionObserver для отслеживания появления элемента в области видимости
  let observer = new IntersectionObserver(function(entries, observer) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        // Запуск анимации счетчиков
        animateValue('liveJobs', 0, 20223, 3000);
        animateValue('companies', 0, 500, 3000);
        animateValue('candidates', 0, 803, 3000);
        animateValue('new_jobs', 0, 120, 3000);

        // Отключаем наблюдатель после начала анимации
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: [0.5] }); // threshold - процент видимости элемента для активации callback

  // Наблюдаем за элементом .counter-area, когда он попадает в область видимости
  observer.observe(document.querySelector('.counter-area'));
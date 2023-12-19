					document.addEventListener('DOMContentLoaded', function() {
    // Применение обработчика событий ко всем формам внутри #filter-form
    var filterForms = document.querySelectorAll('#filter-form form');
    filterForms.forEach(function(form) {
        form.addEventListener('submit', function() {
            // Добавление якоря к действию формы
            form.action = form.action.split('#')[0] + '#filter-form';
        });
    });

    // Прокрутка к якорю после перезагрузки страницы
    if(window.location.hash) {
        var anchor = window.location.hash; // Получение якоря из URL
        var anchorElement = document.querySelector(anchor);
        if(anchorElement) {
            anchorElement.scrollIntoView(); // Прокрутка к элементу
        }
    }
});
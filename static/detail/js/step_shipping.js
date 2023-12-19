            // Сохранение позиции прокрутки
document.querySelectorAll('.stepwizard-step a').forEach(link => {
    link.addEventListener('click', () => {
        localStorage.setItem('scrollPosition', window.scrollY || document.documentElement.scrollTop);
    });
});

// Восстановление позиции прокрутки
document.addEventListener('DOMContentLoaded', (event) => {
    const savedScrollPosition = localStorage.getItem('scrollPosition');
    if (savedScrollPosition) {
        window.scrollTo(0, parseInt(savedScrollPosition));
        localStorage.removeItem('scrollPosition'); // Очистить после использования
    }
});



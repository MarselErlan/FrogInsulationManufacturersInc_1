document.addEventListener('DOMContentLoaded', function() {
    updatePaginationLinks();

    function updatePaginationLinks() {
        document.querySelectorAll('.pagination a').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const url = this.href;

                fetch(url)
                    .then(response => response.text())
                    .then(html => {
                        const newContent = new DOMParser().parseFromString(html, 'text/html');
                        const updatedContent = newContent.querySelector('#pills-tabContent');
                        document.querySelector('#pills-tabContent').innerHTML = updatedContent.innerHTML;

                        const updatedPagination = newContent.querySelector('.pagination');
                        document.querySelector('.pagination').innerHTML = updatedPagination.innerHTML;

                        window.history.pushState({}, '', url);

                        updatePaginationLinks(); // Повторная привязка событий к новым ссылкам пагинации
                    })
                    .catch(error => console.error('Error:', error));
            });
        });
    }
});
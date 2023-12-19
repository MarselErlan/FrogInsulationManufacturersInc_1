
document.addEventListener('DOMContentLoaded', function() {
    const categoryFilter = $('#categoryFilter').select2(); // Инициализация Select2

    updatePaginationLinks();

    categoryFilter.on('change', function() {
    const selectedCategories = $(this).val() || [];
    let url = '?page=1';
    if (selectedCategories.length > 0) {
        const categoriesQueryParam = selectedCategories.join('&b_category=');
        url += `&b_category=${categoriesQueryParam}`;
    }
    fetchAndUpdateContent(url);
});

    function fetchAndUpdateContent(url) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const newContent = new DOMParser().parseFromString(html, 'text/html');
                const updatedContent = newContent.querySelector('#blog_content');
                document.querySelector('#blog_content').innerHTML = updatedContent.innerHTML;

                const updatedPagination = newContent.querySelector('.pagination');
                document.querySelector('.pagination').innerHTML = updatedPagination.innerHTML;

                window.history.pushState({}, '', url);

                updatePaginationLinks(); // Повторная привязка событий к новым ссылкам пагинации
            })
            .catch(error => console.error('Error:', error));
    }

    function updatePaginationLinks() {
        document.querySelectorAll('.pagination a').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const url = this.href;

                fetchAndUpdateContent(url);
            });
        });
    }
});

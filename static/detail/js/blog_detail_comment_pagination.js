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
                        const updatedComments = newContent.querySelector('.post-comment-area');
                        document.querySelector('.post-comment-area').innerHTML = updatedComments.innerHTML;

                        updatePaginationLinks(); // Rebind events to new pagination links
                    })
                    .catch(error => console.error('Error:', error));
            });
        });
    }
});
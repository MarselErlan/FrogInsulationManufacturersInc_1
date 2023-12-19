
function markAsRead(notificationId) {
    fetch(`/notifications/read/${notificationId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest', // Для Django проверки AJAX запроса
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const notificationElement = document.getElementById(`notification-${notificationId}`);
            if (notificationElement) {
                notificationElement.style.display = 'none';
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

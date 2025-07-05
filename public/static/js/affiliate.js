function showAffiliatePopup() {
    const popup = document.getElementById('affiliatePopup');
    popup.classList.add('active');
    
    // Автоматически скроллим к верху страницы
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function hideAffiliatePopup() {
    const popup = document.getElementById('affiliatePopup');
    popup.classList.remove('active');
}

function copyAffiliateLink() {
    const link = document.getElementById('affiliateLink').textContent;
    navigator.clipboard.writeText(link)
        .then(() => {
            // Создаем временный элемент для показа уведомления
            const notification = document.createElement('div');
            notification.className = 'affiliate-notification';
            notification.textContent = 'Ссылка скопирована!';
            
            document.body.appendChild(notification);
            
            // Удаляем уведомление через 2 секунды
            setTimeout(() => {
                notification.remove();
            }, 2000);
        })
        .catch(err => {
            console.error('Ошибка при копировании:', err);
        });
}

// Добавляем обработчик клика по фону попапа
const popup = document.getElementById('affiliatePopup');
if (popup) {
    popup.addEventListener('click', (e) => {
        if (e.target === popup) {
            hideAffiliatePopup();
        }
    });
}

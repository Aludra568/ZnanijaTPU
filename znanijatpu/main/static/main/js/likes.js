// Функция инициализации лайков (принимает настройки из HTML)
function initLikes(csrfToken, loginUrl) {
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation(); // Не даём сработать stretched-link
            
            const url = this.dataset.url;
            const icon = this.querySelector('i');
            const countSpan = this.querySelector('.likes-count');

            console.log('🔍 Like click:', url);

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                }
            })
            .then(res => {
                console.log('📡 Server response status:', res.status);
                return res.json();
            })
            .then(data => {
                console.log('📦 Server data:', data);
                if (data.success) {
                    icon.className = data.liked 
                        ? 'fa-solid fa-thumbs-up me-1' 
                        : 'fa-regular fa-thumbs-up me-1';
                    countSpan.textContent = data.likes_count;
                    this.dataset.liked = data.liked;
                } else {
                    console.warn('⚠️ Like failed, redirecting to login...');
                    if (loginUrl) window.location.href = loginUrl;
                }
            })
            .catch(err => console.error('❌ Fetch error:', err));
        });
    });
}

// Автозапуск, если данные уже есть в DOM
document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const csrfToken = body.dataset.csrfToken;
    const loginUrl = body.dataset.loginUrl;
    
    if (csrfToken) {
        initLikes(csrfToken, loginUrl);
    }
});
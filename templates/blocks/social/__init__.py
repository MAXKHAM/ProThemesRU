# Социальные блоки для конструктора сайтов

social_blocks = {
    "social_links": {
        "name": "Социальные сети",
        "category": "social",
        "html": "<div class='social-links'><a href='#' class='social-link'><i class='fab fa-facebook'></i></a><a href='#' class='social-link'><i class='fab fa-twitter'></i></a><a href='#' class='social-link'><i class='fab fa-instagram'></i></a><a href='#' class='social-link'><i class='fab fa-linkedin'></i></a></div>",
        "css": ".social-links { display: flex; gap: 15px; justify-content: center; margin: 20px 0; } .social-link { display: inline-block; width: 40px; height: 40px; background: #007bff; color: white; text-align: center; line-height: 40px; border-radius: 50%; text-decoration: none; transition: background 0.3s; } .social-link:hover { background: #0056b3; }",
        "properties": ["platforms", "colors", "size", "alignment", "show-text"]
    },
    "share_buttons": {
        "name": "Кнопки поделиться",
        "category": "social",
        "html": "<div class='share-buttons'><button class='share-btn facebook'>Поделиться в Facebook</button><button class='share-btn twitter'>Поделиться в Twitter</button><button class='share-btn vk'>Поделиться в VK</button></div>",
        "css": ".share-buttons { display: flex; gap: 10px; margin: 20px 0; } .share-btn { padding: 10px 20px; border: none; border-radius: 5px; color: white; cursor: pointer; } .share-btn.facebook { background: #1877f2; } .share-btn.twitter { background: #1da1f2; } .share-btn.vk { background: #4c75a3; }",
        "properties": ["platforms", "button-text", "colors", "size", "show-icons"]
    },
    "social_feed": {
        "name": "Лента социальных сетей",
        "category": "social",
        "html": "<div class='social-feed'><h3>Мы в социальных сетях</h3><div class='feed-container'><div class='feed-item'><div class='feed-header'><img src='https://via.placeholder.com/40x40' alt='Avatar' class='feed-avatar'><span class='feed-author'>@username</span></div><p class='feed-text'>Отличный сервис! Рекомендую всем!</p><div class='feed-meta'><span class='feed-date'>2 часа назад</span><span class='feed-likes'>❤️ 15</span></div></div></div></div>",
        "css": ".social-feed { max-width: 400px; margin: 0 auto; } .feed-container { border: 1px solid #ddd; border-radius: 10px; padding: 20px; } .feed-item { margin-bottom: 20px; } .feed-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; } .feed-avatar { width: 40px; height: 40px; border-radius: 50%; } .feed-author { font-weight: bold; } .feed-text { margin: 10px 0; } .feed-meta { display: flex; justify-content: space-between; color: #666; font-size: 0.9em; }",
        "properties": ["platform", "posts-count", "show-avatars", "show-likes", "auto-refresh"]
    },
    "comment_system": {
        "name": "Система комментариев",
        "category": "social",
        "html": "<div class='comments-section'><h3>Комментарии (3)</h3><div class='comment-form'><textarea placeholder='Написать комментарий...' rows='3'></textarea><button class='comment-submit'>Отправить</button></div><div class='comments-list'><div class='comment'><div class='comment-header'><img src='https://via.placeholder.com/32x32' alt='User' class='comment-avatar'><span class='comment-author'>Пользователь</span><span class='comment-date'>2 часа назад</span></div><p class='comment-text'>Отличная статья!</p></div></div></div>",
        "css": ".comments-section { margin: 40px 0; } .comment-form { margin-bottom: 20px; } .comment-form textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; resize: vertical; } .comment-submit { padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; } .comment { border-bottom: 1px solid #eee; padding: 15px 0; } .comment-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; } .comment-avatar { width: 32px; height: 32px; border-radius: 50%; } .comment-date { color: #666; font-size: 0.9em; }",
        "properties": ["moderation", "show-avatars", "allow-replies", "sort-by", "page-size"]
    },
    "social_proof": {
        "name": "Социальные доказательства",
        "category": "social",
        "html": "<div class='social-proof'><div class='proof-item'><div class='proof-number'>10,000+</div><div class='proof-label'>Довольных клиентов</div></div><div class='proof-item'><div class='proof-number'>4.9</div><div class='proof-label'>Рейтинг на Trustpilot</div></div><div class='proof-item'><div class='proof-number'>99%</div><div class='proof-label'>Время безотказной работы</div></div></div>",
        "css": ".social-proof { display: flex; justify-content: space-around; padding: 40px 0; background: #f8f9fa; border-radius: 10px; } .proof-item { text-align: center; } .proof-number { font-size: 2.5em; font-weight: bold; color: #007bff; } .proof-label { color: #666; margin-top: 5px; }",
        "properties": ["metrics", "background", "text-color", "animation", "show-icons"]
    }
} 
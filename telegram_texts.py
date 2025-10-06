#!/usr/bin/env python3
"""
Тексты для Telegram-бота ГАРАНТ СДЕЛОК 3.0
Все сообщения, уведомления и виральный контент
"""

# Основные тексты бота
BOT_TEXTS = {
    'ru': {
        # Приветствие
        'welcome': """👋 Привет! Я — ГАРАНТ СДЕЛОК, ваш AI-гарант в мире крипто и цифровых активов.

🛡️ За 3 минуты я помогу вам:
• Создать **неподдельную** схему сделки  
• Получить **NFT-сертификат доверия**  
• Заработать на рефералах — **пожизненно**

🎁 Бонус: первые 3 сделки — **БЕСПЛАТНО**!

💰 Ваша реферальная ссылка:
`{ref_link}`
Поделитесь — и получите 20% от всех комиссий ваших друзей. Всегда.

📊 Статистика:
• Сделок завершено: {deals_count}
• Заработано на рефералах: ${referral_earnings:.2f}
• NFT-сертификатов: {nft_count}

Выберите, с чего начать:""",

        # Начало сделки
        'start_deal': """🚀 Отлично! Давайте создадим безопасную сделку.

Выберите актив для сделки:""",

        # Выбор актива
        'asset_selected': """✅ Выбран актив: {asset_name}

💰 Теперь укажите сумму сделки в долларах США:""",

        # Обработка суммы
        'amount_processing': """✅ Сумма: ${amount:,.2f}
📊 Анализ риска: {risk_level}
💸 Комиссия: ${commission:.2f} {'(БЕСПЛАТНО - первая сделка!)' if is_first_deal else ''}

👤 Теперь укажите Telegram ID продавца (например: @username или 123456789):""",

        # Ошибка суммы
        'amount_error': """❌ Неверный формат суммы. Введите число (например: 1000):""",

        # Ошибка ID продавца
        'seller_id_error': """❌ Неверный формат ID. Укажите @username или числовой ID:""",

        # Подтверждение сделки
        'deal_confirmation': """📋 Подтвердите детали сделки:

👤 Покупатель: @{buyer_username}
👤 Продавец: {seller_id}
💰 Актив: {asset}
💵 Сумма: ${amount:,.2f}
💸 Комиссия: ${commission:.2f} {'(БЕСПЛАТНО!)' if is_first_deal else ''}
🛡️ Защита: AI + Блокчейн
⏱️ Время: 2-5 минут

✅ Все верно?""",

        # Сделка запущена
        'deal_started': """🚀 Сделка #{deal_id} запущена!

📱 Отправьте эту ссылку продавцу:
`https://t.me/GARANT_S_bot?deal={deal_id}`

⏱️ Ожидаем подтверждения от продавца...
🛡️ Ваши средства под защитой AI""",

        # Статус сделки
        'deal_status': """📊 Статус сделки #{deal_id}

{status_emoji} Статус: {status}
💰 Сумма: ${amount:,.2f}
💸 Комиссия: ${commission:.2f}
🕐 Создана: {created_at}

{'🎨 NFT-сертификат готов!' if nft_hash else '⏳ Ожидаем завершения...'}

{f'🔗 Хеш сертификата: `{nft_hash}`' if nft_hash else ''}""",

        # Сделка завершена
        'deal_completed': """✅ Сделка #{deal_id} завершена!

🎨 Ваш NFT-сертификат готов:
`{nft_hash}`

💰 Сумма: ${amount:,.2f}
🛡️ Защита сработала идеально!

Поделитесь сертификатом в соцсетях и получите +10% к реферальным вознаграждениям!""",

        # NFT статус
        'nft_status_empty': """🎨 У вас пока нет NFT-сертификатов

Завершите первую сделку, чтобы получить свой первый Soulbound NFT-сертификат доверия!

NFT-сертификаты:
• Не продаются — только ваши
• Доказывают вашу надежность
• Дают +10% к реферальным вознаграждениям
• Можно делиться в соцсетях""",

        'nft_status_with_certs': """🎨 Ваши NFT-сертификаты ({count})

{certificates_text}""",

        # Реферальная программа
        'referral_program': """💰 Реферальная программа

🔗 Ваша ссылка:
`{ref_link}`

📊 Статистика:
• Приглашено друзей: {referrals_count}
• Заработано: ${earnings:.2f}
• Комиссия с каждого друга: 20% пожизненно

🎁 Бонусы:
• +10% к реферальным вознаграждениям за NFT-сертификаты
• Эксклюзивные предложения для активных реферов
• Приоритетная поддержка

📱 Поделитесь ссылкой и начните зарабатывать!""",

        # Статистика пользователя
        'user_stats': """📊 Ваша статистика

👤 Пользователь: @{username}
📅 Регистрация: {join_date}

💼 Сделки:
• Завершено: {deals_count}
• Осталось бесплатных: {free_deals_left}

💰 Заработок:
• Реферальные: ${referral_earnings:.2f}
• Общий: ${total_earnings:.2f}

🎨 NFT-сертификаты: {nft_count}

🏆 Уровень доверия: {trust_level}""",

        # Как это работает
        'how_it_works': """❓ Как работает ГАРАНТ СДЕЛОК 3.0

🛡️ Принцип работы:
1. Покупатель создает сделку
2. Продавец подтверждает участие
3. AI-система блокирует средства
4. Сделка выполняется автоматически
5. Вы получаете NFT-сертификат

🤖 AI-защита:
• Анализ рисков в реальном времени
• Автоматическое обнаружение мошенничества
• Умные контракты на блокчейне
• Возврат средств за 1 час при проблемах

🎨 NFT-сертификаты:
• Soulbound (не продаются)
• Доказывают вашу надежность
• Увеличивают реферальные бонусы
• Можно делиться в соцсетях

💰 Реферальная программа:
• 20% от комиссий друзей пожизненно
• +10% за NFT-сертификаты
• Пассивный доход от каждого реферала

🔒 Безопасность:
• Децентрализованное хранение
• Мультиподпись для крупных сделок
• Страхование от мошенничества
• 24/7 мониторинг AI""",

        # Реферальное уведомление
        'referral_notification': """🎉 Ваш друг @{friend_username} присоединился по вашей ссылке!

Вы будете получать 20% от всех его комиссий пожизненно!""",

        # Реферальный заработок
        'referral_earnings': """🎉 Ваш друг завершил сделку на ${amount:,.2f}!

💰 Вы получили ${earnings:.2f} реферального вознаграждения!""",

        # Ошибки
        'deal_not_found': """❌ Сделка не найдена или устарела""",
        'deal_completed': """❌ Сделка уже завершена или отменена""",
        'invalid_amount': """❌ Сумма должна быть больше 0. Попробуйте еще раз:""",
        'copy_success': """✅ Ссылка скопирована!""",
        'copy_error': """❌ Ошибка копирования. Попробуйте еще раз.""",

        # Кнопки
        'buttons': {
            'start_deal': '🚀 Начать сделку',
            'nft_status': '🎁 Получить NFT-статус',
            'referral_program': '💰 Реферальная программа',
            'how_it_works': '❓ Как это работает',
            'my_stats': '📊 Моя статистика',
            'back_to_main': '🔙 Назад',
            'confirm_deal': '✅ Подтвердить',
            'cancel_deal': '❌ Отменить',
            'deal_status': '📊 Статус сделки',
            'copy_ref_link': '📋 Скопировать ссылку',
            'dismiss_promo': '❌ Не показывать'
        }
    },

    'en': {
        # Приветствие
        'welcome': """👋 Hello! I'm DEAL GUARANTEE, your AI guarantor in the world of crypto and digital assets.

🛡️ In 3 minutes I'll help you:
• Create an **unforgeable** deal scheme  
• Get an **NFT trust certificate**  
• Earn from referrals — **lifetime**

🎁 Bonus: first 3 deals — **FREE**!

💰 Your referral link:
`{ref_link}`
Share — and get 20% from all your friends' commissions. Always.

📊 Statistics:
• Deals completed: {deals_count}
• Earned from referrals: ${referral_earnings:.2f}
• NFT certificates: {nft_count}

Choose where to start:""",

        # Остальные тексты на английском...
        # (Для краткости показаны только основные)
    }
}

# Виральные тексты для соцсетей
VIRAL_TEXTS = {
    'twitter': {
        'first_deal': "🚀 Just completed my first secure deal with @GARANT_S_bot! Got my NFT certificate and earned ${earnings:.2f} in referral bonuses. Zero risk, maximum trust! #SafeDeals #Crypto #NFT",
        'high_value': "💎 Just completed a high-value deal of ${amount:,.2f} with @GARANT_S_bot! My trust level increased. AI + Blockchain = Perfect security! #HighValue #Crypto #AI",
        'referral_milestone': "🏆 Reached milestone: {count} referrals! I'm earning ${earnings:.2f} monthly from my network. Join me! #Referral #Crypto #PassiveIncome",
        'nft_collection': "🎨 Now I have {count} NFT trust certificates! I'm a trust collector. Each certificate proves my reliability. #NFT #Trust #Crypto"
    },
    
    'telegram': {
        'first_deal': "🎉 Завершил первую безопасную сделку через @GARANT_S_bot! Получил NFT-сертификат и заработал ${earnings:.2f} на рефералах. 0% риска, 100% доверия!",
        'high_value': "💎 Выполнил крупную сделку на ${amount:,.2f} через @GARANT_S_bot! Мой уровень доверия повышен. AI + Блокчейн = Идеальная безопасность!",
        'referral_milestone': "🏆 Достигнута веха: {count} рефералов! Зарабатываю ${earnings:.2f} в месяц от своей сети. Присоединяйтесь!",
        'nft_collection': "🎨 У меня уже {count} NFT-сертификатов доверия! Я коллекционер доверия. Каждый сертификат доказывает мою надежность."
    },
    
    'linkedin': {
        'first_deal': "Just used an AI-powered escrow service for a crypto transaction. The future of secure digital asset trading is here! #FinTech #Crypto #AI",
        'high_value': "Completed a high-value crypto transaction using AI-powered escrow. The technology is incredible - zero risk, maximum security! #Blockchain #FinTech",
        'referral_milestone': "Built a passive income stream through crypto referrals. Technology is changing how we think about trust and money! #PassiveIncome #Crypto",
        'nft_collection': "My digital trust portfolio is growing! Each NFT certificate represents a successful, secure transaction. #DigitalAssets #Trust"
    }
}

# Промо-тексты
PROMO_TEXTS = {
    'new_user': {
        'title': '🎁 Добро пожаловать!',
        'message': 'Ваши первые 3 сделки бесплатны. Начните прямо сейчас!',
        'cta': 'Начать первую сделку'
    },
    
    'inactive_user': {
        'title': '💎 Мы скучаем!',
        'message': 'Вернитесь и получите бонус 10% к реферальным вознаграждениям!',
        'cta': 'Вернуться к сделкам'
    },
    
    'referral_reminder': {
        'title': '🎉 Сделка завершена!',
        'message': 'Не забудьте поделиться реферальной ссылкой и заработать на друзьях!',
        'cta': 'Поделиться ссылкой'
    },
    
    'milestone_celebration': {
        'title': '🏆 Поздравляем с достижением!',
        'message': 'Вы получили эксклюзивные привилегии!',
        'cta': 'Посмотреть привилегии'
    }
}

# Персонализированные рекомендации
PERSONALIZED_RECOMMENDATIONS = {
    'newbie': [
        "🎁 Первые 3 сделки бесплатны - отличный способ попробовать!",
        "📚 Изучите руководство по безопасным сделкам",
        "🔗 Пригласите друзей и получите 20% от их комиссий"
    ],
    
    'regular': [
        "💡 Попробуйте новые активы - у нас 300+ вариантов",
        "🎨 Создайте NFT-сертификат после следующей сделки",
        "💰 Увеличьте реферальные доходы, поделившись ссылкой"
    ],
    
    'power_user': [
        "🚀 Рассмотрите крупные сделки - у вас есть привилегии",
        "🏆 Получите VIP-статус за активность",
        "💎 Эксклюзивные предложения доступны для вас"
    ],
    
    'vip': [
        "💎 Эксклюзивные сделки только для VIP",
        "🏆 Вы наш топ-пользователь - спасибо за доверие!",
        "🌟 Персональный менеджер доступен 24/7"
    ]
}

# Эмодзи для статусов
STATUS_EMOJIS = {
    'pending': '⏳',
    'confirmed': '✅',
    'completed': '🎉',
    'cancelled': '❌',
    'high_risk': '🔴',
    'medium_risk': '🟡',
    'low_risk': '🟢'
}

# Уровни доверия
TRUST_LEVELS = {
    'newbie': '🥉 Начинающий',
    'regular': '🥈 Средний',
    'power_user': '🥇 Высокий',
    'vip': '💎 VIP'
}

def get_text(key: str, lang: str = 'ru', **kwargs) -> str:
    """Получение локализованного текста"""
    text = BOT_TEXTS.get(lang, BOT_TEXTS['ru']).get(key, '')
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError as e:
            print(f"Missing parameter: {e}")
            return text
    
    return text

def get_viral_text(platform: str, trigger_type: str, **kwargs) -> str:
    """Получение вирального текста для соцсети"""
    text = VIRAL_TEXTS.get(platform, {}).get(trigger_type, '')
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError as e:
            print(f"Missing parameter: {e}")
            return text
    
    return text

def get_promo_text(promo_type: str) -> dict:
    """Получение промо-текста"""
    return PROMO_TEXTS.get(promo_type, {})

def get_recommendations(user_segment: str) -> list:
    """Получение персонализированных рекомендаций"""
    return PERSONALIZED_RECOMMENDATIONS.get(user_segment, [])

def get_status_emoji(status: str) -> str:
    """Получение эмодзи для статуса"""
    return STATUS_EMOJIS.get(status, '❓')

def get_trust_level(segment: str) -> str:
    """Получение уровня доверия"""
    return TRUST_LEVELS.get(segment, '🥉 Начинающий')

# Пример использования
if __name__ == '__main__':
    # Тест получения текста
    welcome_text = get_text('welcome', 
                          ref_link='https://t.me/GARANT_S_bot?start=ref_123',
                          deals_count=5,
                          referral_earnings=25.50,
                          nft_count=3)
    print(welcome_text)
    
    # Тест вирального текста
    viral_tweet = get_viral_text('twitter', 'first_deal', earnings=15.75)
    print(viral_tweet)
    
    # Тест рекомендаций
    recommendations = get_recommendations('newbie')
    print(recommendations)
#!/usr/bin/env python3
"""
Виральные механики и автопродвижение для ГАРАНТ СДЕЛОК 3.0
Система самораспространения и вирусного роста
"""

import asyncio
import json
import logging
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ViralGrowthEngine:
    """Движок вирусного роста"""
    
    def __init__(self):
        self.growth_metrics = {
            'daily_active_users': 0,
            'referral_conversion_rate': 0.15,  # 15% конверсия рефералов
            'viral_coefficient': 1.0,
            'retention_rate': 0.85
        }
        
        self.viral_triggers = {
            'first_deal_completed': {
                'weight': 0.3,
                'message': "🎉 Первая сделка завершена! Поделитесь своим NFT-сертификатом и получите +10% к реферальным бонусам!",
                'social_share_bonus': 0.1
            },
            'high_value_deal': {
                'weight': 0.4,
                'threshold': 10000,
                'message': "💎 Выполнена крупная сделка на ${amount}! Ваш статус доверия повышен. Поделитесь достижением!",
                'social_share_bonus': 0.15
            },
            'referral_milestone': {
                'weight': 0.2,
                'milestones': [5, 10, 25, 50],
                'message': "🏆 Достигнута веха: {count} рефералов! Вы получаете эксклюзивные привилегии!",
                'social_share_bonus': 0.2
            },
            'nft_collection': {
                'weight': 0.1,
                'threshold': 10,
                'message': "🎨 У вас {count} NFT-сертификатов! Вы стали коллекционером доверия!",
                'social_share_bonus': 0.25
            }
        }

    def calculate_viral_potential(self, user_data: Dict) -> float:
        """Расчет вирального потенциала пользователя"""
        score = 0
        
        # Базовые метрики
        deals_count = user_data.get('deals_count', 0)
        referrals_count = user_data.get('referrals_count', 0)
        nft_count = len(user_data.get('nft_certificates', []))
        total_volume = user_data.get('total_volume', 0)
        
        # Весовые коэффициенты
        score += deals_count * 2
        score += referrals_count * 5
        score += nft_count * 3
        score += min(total_volume / 1000, 50)  # Кап на объем
        
        # Бонусы за активность
        if user_data.get('last_active_days', 0) < 3:
            score *= 1.2
        
        # Бонусы за социальную активность
        if user_data.get('social_shares', 0) > 0:
            score *= 1.1
        
        return min(100, score)

    def generate_viral_content(self, user_data: Dict, trigger_type: str, deal_data: Dict = None) -> Dict:
        """Генерация вирального контента"""
        trigger = self.viral_triggers.get(trigger_type, {})
        
        if not trigger:
            return None
        
        # Персонализация сообщения
        message = trigger['message']
        if deal_data:
            message = message.format(**deal_data)
        else:
            message = message.format(
                count=user_data.get('referrals_count', 0),
                amount=deal_data.get('amount', 0) if deal_data else 0
            )
        
        # Генерация хештегов
        hashtags = self._generate_hashtags(trigger_type, user_data)
        
        # Создание визуального контента
        visual_content = self._create_visual_content(user_data, trigger_type, deal_data)
        
        return {
            'message': message,
            'hashtags': hashtags,
            'visual_content': visual_content,
            'social_share_bonus': trigger.get('social_share_bonus', 0),
            'platforms': ['twitter', 'telegram', 'linkedin']
        }

    def _generate_hashtags(self, trigger_type: str, user_data: Dict) -> List[str]:
        """Генерация релевантных хештегов"""
        base_hashtags = ['#SafeDeals', '#Crypto', '#AI', '#Blockchain', '#Trust']
        
        trigger_hashtags = {
            'first_deal_completed': ['#FirstDeal', '#NFT', '#NewUser'],
            'high_value_deal': ['#HighValue', '#Premium', '#VIP'],
            'referral_milestone': ['#Referral', '#Milestone', '#Achievement'],
            'nft_collection': ['#Collection', '#NFT', '#Certificates']
        }
        
        specific_hashtags = trigger_hashtags.get(trigger_type, [])
        
        # Добавление персонализированных хештегов
        if user_data.get('deals_count', 0) > 10:
            specific_hashtags.append('#Veteran')
        
        if user_data.get('referral_earnings', 0) > 100:
            specific_hashtags.append('#TopEarner')
        
        return base_hashtags + specific_hashtags[:3]  # Ограничиваем количество

    def _create_visual_content(self, user_data: Dict, trigger_type: str, deal_data: Dict = None) -> str:
        """Создание визуального контента (SVG)"""
        # Базовые параметры
        width = 800
        height = 600
        
        # Цвета в зависимости от типа триггера
        color_schemes = {
            'first_deal_completed': ('#00f0b0', '#8a6dff'),
            'high_value_deal': ('#ff4d8d', '#ffa500'),
            'referral_milestone': ('#8a6dff', '#00f0b0'),
            'nft_collection': ('#ffa500', '#ff4d8d')
        }
        
        primary_color, secondary_color = color_schemes.get(trigger_type, ('#8a6dff', '#00f0b0'))
        
        # Создание SVG
        svg = f"""
        <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#0f0c1a;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#1a0f2e;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{primary_color};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{secondary_color};stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="{width}" height="{height}" fill="url(#bgGrad)"/>
            
            <!-- Заголовок -->
            <text x="{width//2}" y="100" text-anchor="middle" fill="url(#accentGrad)" 
                  font-family="Arial" font-size="48" font-weight="bold">ГАРАНТ СДЕЛОК 3.0</text>
            
            <!-- Основной контент -->
            <text x="{width//2}" y="200" text-anchor="middle" fill="#ffffff" 
                  font-family="Arial" font-size="32" font-weight="bold">Безопасная сделка завершена!</text>
            
            <!-- Статистика -->
            <text x="{width//2}" y="280" text-anchor="middle" fill="#b8b8b8" 
                  font-family="Arial" font-size="24">Сделок: {user_data.get('deals_count', 0)}</text>
            
            <text x="{width//2}" y="320" text-anchor="middle" fill="#b8b8b8" 
                  font-family="Arial" font-size="24">Рефералов: {user_data.get('referrals_count', 0)}</text>
            
            <text x="{width//2}" y="360" text-anchor="middle" fill="#b8b8b8" 
                  font-family="Arial" font-size="24">NFT-сертификатов: {len(user_data.get('nft_certificates', []))}</text>
            
            <!-- Призыв к действию -->
            <text x="{width//2}" y="450" text-anchor="middle" fill="url(#accentGrad)" 
                  font-family="Arial" font-size="28" font-weight="bold">Поделитесь и заработайте больше!</text>
            
            <!-- Логотип -->
            <circle cx="{width//2}" cy="520" r="40" fill="url(#accentGrad)"/>
            <text x="{width//2}" y="530" text-anchor="middle" fill="#0f0c1a" 
                  font-family="Arial" font-size="24" font-weight="bold">GS</text>
        </svg>
        """
        
        return f"data:image/svg+xml;base64,{svg.encode('utf-8').hex()}"

class AutoPromotionSystem:
    """Система автопродвижения"""
    
    def __init__(self):
        self.promotion_campaigns = {
            'new_user_onboarding': {
                'trigger': 'user_registered',
                'delay_hours': 1,
                'message_template': "🎁 Добро пожаловать! Ваши первые 3 сделки бесплатны. Начните прямо сейчас!",
                'cta': "Начать первую сделку"
            },
            'inactive_user_reactivation': {
                'trigger': 'user_inactive_7_days',
                'delay_hours': 0,
                'message_template': "💎 Мы скучаем! Вернитесь и получите бонус 10% к реферальным вознаграждениям!",
                'cta': "Вернуться к сделкам"
            },
            'referral_reminder': {
                'trigger': 'deal_completed',
                'delay_hours': 2,
                'message_template': "🎉 Сделка завершена! Не забудьте поделиться реферальной ссылкой и заработать на друзьях!",
                'cta': "Поделиться ссылкой"
            },
            'milestone_celebration': {
                'trigger': 'milestone_reached',
                'delay_hours': 0,
                'message_template': "🏆 Поздравляем с достижением! Вы получили эксклюзивные привилегии!",
                'cta': "Посмотреть привилегии"
            }
        }
        
        self.personalization_engine = PersonalizationEngine()

    async def process_promotion_trigger(self, trigger_type: str, user_data: Dict, additional_data: Dict = None) -> Optional[Dict]:
        """Обработка триггера автопродвижения"""
        campaign = self.promotion_campaigns.get(trigger_type)
        
        if not campaign:
            return None
        
        # Персонализация сообщения
        personalized_message = self.personalization_engine.personalize_message(
            campaign['message_template'],
            user_data,
            additional_data
        )
        
        # Создание клавиатуры
        keyboard = self._create_promotion_keyboard(campaign['cta'], user_data)
        
        # Определение времени отправки
        send_time = datetime.now() + timedelta(hours=campaign['delay_hours'])
        
        return {
            'message': personalized_message,
            'keyboard': keyboard,
            'send_time': send_time,
            'campaign_type': trigger_type,
            'user_id': user_data.get('user_id')
        }

    def _create_promotion_keyboard(self, cta_text: str, user_data: Dict) -> Dict:
        """Создание клавиатуры для промо-сообщения"""
        keyboard = {
            'inline_keyboard': [
                [{'text': cta_text, 'callback_data': 'promo_action'}],
                [{'text': '❌ Не показывать', 'callback_data': 'dismiss_promo'}]
            ]
        }
        
        # Добавление дополнительных кнопок в зависимости от пользователя
        if user_data.get('deals_count', 0) > 0:
            keyboard['inline_keyboard'].insert(0, [
                {'text': '📊 Моя статистика', 'callback_data': 'my_stats'},
                {'text': '💰 Рефералы', 'callback_data': 'referral_program'}
            ])
        
        return keyboard

class PersonalizationEngine:
    """Движок персонализации"""
    
    def __init__(self):
        self.user_segments = {
            'newbie': {'deals_count': (0, 2), 'priority': 'onboarding'},
            'regular': {'deals_count': (3, 10), 'priority': 'retention'},
            'power_user': {'deals_count': (11, 50), 'priority': 'monetization'},
            'vip': {'deals_count': (51, float('inf')), 'priority': 'exclusivity'}
        }
        
        self.personalization_templates = {
            'greeting': {
                'newbie': "👋 Привет, {name}! Добро пожаловать в мир безопасных сделок!",
                'regular': "👋 С возвращением, {name}! Готовы к новой сделке?",
                'power_user': "👋 Привет, {name}! Вы наш надежный партнер!",
                'vip': "👋 Добро пожаловать, {name}! Эксклюзивные предложения ждут вас!"
            },
            'deal_suggestion': {
                'newbie': "🎁 Начните с простой сделки - первые 3 бесплатны!",
                'regular': "💡 Попробуйте новый актив - у нас 300+ вариантов!",
                'power_user': "🚀 Рассмотрите крупную сделку - у вас есть привилегии!",
                'vip': "💎 Эксклюзивная сделка только для VIP-пользователей!"
            }
        }

    def get_user_segment(self, user_data: Dict) -> str:
        """Определение сегмента пользователя"""
        deals_count = user_data.get('deals_count', 0)
        
        for segment, criteria in self.user_segments.items():
            min_deals, max_deals = criteria['deals_count']
            if min_deals <= deals_count <= max_deals:
                return segment
        
        return 'newbie'

    def personalize_message(self, template: str, user_data: Dict, additional_data: Dict = None) -> str:
        """Персонализация сообщения"""
        segment = self.get_user_segment(user_data)
        
        # Базовые данные для подстановки
        context = {
            'name': user_data.get('username', 'Пользователь'),
            'deals_count': user_data.get('deals_count', 0),
            'referrals_count': user_data.get('referrals_count', 0),
            'earnings': user_data.get('referral_earnings', 0),
            'segment': segment
        }
        
        # Добавление дополнительных данных
        if additional_data:
            context.update(additional_data)
        
        # Применение персонализированного шаблона
        personalized_template = self.personalization_templates.get(template, {}).get(segment, template)
        
        # Подстановка переменных
        try:
            return personalized_template.format(**context)
        except KeyError as e:
            logger.warning(f"Missing context variable: {e}")
            return template

    def get_personalized_recommendations(self, user_data: Dict) -> List[str]:
        """Получение персонализированных рекомендаций"""
        segment = self.get_user_segment(user_data)
        recommendations = []
        
        if segment == 'newbie':
            recommendations.extend([
                "🎁 Первые 3 сделки бесплатны - отличный способ попробовать!",
                "📚 Изучите руководство по безопасным сделкам",
                "🔗 Пригласите друзей и получите 20% от их комиссий"
            ])
        elif segment == 'regular':
            recommendations.extend([
                "💡 Попробуйте новые активы - у нас 300+ вариантов",
                "🎨 Создайте NFT-сертификат после следующей сделки",
                "💰 Увеличьте реферальные доходы, поделившись ссылкой"
            ])
        elif segment == 'power_user':
            recommendations.extend([
                "🚀 Рассмотрите крупные сделки - у вас есть привилегии",
                "🏆 Получите VIP-статус за активность",
                "💎 Эксклюзивные предложения доступны для вас"
            ])
        elif segment == 'vip':
            recommendations.extend([
                "💎 Эксклюзивные сделки только для VIP",
                "🏆 Вы наш топ-пользователь - спасибо за доверие!",
                "🌟 Персональный менеджер доступен 24/7"
            ])
        
        return recommendations

class ViralAnalytics:
    """Аналитика вирусного роста"""
    
    def __init__(self):
        self.metrics = {
            'total_users': 0,
            'active_users_24h': 0,
            'active_users_7d': 0,
            'referral_conversion_rate': 0.0,
            'viral_coefficient': 0.0,
            'retention_rate': 0.0,
            'social_shares': 0,
            'nft_certificates_created': 0
        }

    def update_metrics(self, event_type: str, data: Dict):
        """Обновление метрик"""
        if event_type == 'user_registered':
            self.metrics['total_users'] += 1
        elif event_type == 'user_active':
            self.metrics['active_users_24h'] += 1
        elif event_type == 'referral_conversion':
            self.metrics['referral_conversion_rate'] = data.get('conversion_rate', 0.0)
        elif event_type == 'social_share':
            self.metrics['social_shares'] += 1
        elif event_type == 'nft_created':
            self.metrics['nft_certificates_created'] += 1

    def calculate_viral_coefficient(self) -> float:
        """Расчет вирального коэффициента"""
        if self.metrics['total_users'] == 0:
            return 0.0
        
        # Простая формула вирального коэффициента
        referrals_per_user = self.metrics['referral_conversion_rate'] * 2
        retention_factor = self.metrics['retention_rate']
        
        return referrals_per_user * retention_factor

    def get_growth_forecast(self, days: int = 30) -> Dict:
        """Прогноз роста на N дней"""
        current_users = self.metrics['total_users']
        viral_coeff = self.calculate_viral_coefficient()
        
        # Простая модель экспоненциального роста
        forecast = []
        for day in range(1, days + 1):
            new_users = current_users * (viral_coeff ** day)
            forecast.append({
                'day': day,
                'total_users': int(current_users + new_users),
                'new_users': int(new_users)
            })
        
        return {
            'forecast': forecast,
            'viral_coefficient': viral_coeff,
            'current_metrics': self.metrics
        }

# Главный класс виральных механик
class ViralMechanicsManager:
    """Менеджер виральных механик"""
    
    def __init__(self):
        self.growth_engine = ViralGrowthEngine()
        self.auto_promotion = AutoPromotionSystem()
        self.personalization = PersonalizationEngine()
        self.analytics = ViralAnalytics()

    async def process_user_event(self, event_type: str, user_data: Dict, additional_data: Dict = None) -> List[Dict]:
        """Обработка события пользователя"""
        actions = []
        
        # Обновление аналитики
        self.analytics.update_metrics(event_type, additional_data or {})
        
        # Проверка виральных триггеров
        viral_content = self.growth_engine.generate_viral_content(
            user_data, event_type, additional_data
        )
        
        if viral_content:
            actions.append({
                'type': 'viral_content',
                'content': viral_content,
                'priority': 'high'
            })
        
        # Проверка автопродвижения
        promotion = await self.auto_promotion.process_promotion_trigger(
            event_type, user_data, additional_data
        )
        
        if promotion:
            actions.append({
                'type': 'auto_promotion',
                'content': promotion,
                'priority': 'medium'
            })
        
        # Персонализированные рекомендации
        recommendations = self.personalization.get_personalized_recommendations(user_data)
        if recommendations:
            actions.append({
                'type': 'personalized_recommendations',
                'content': recommendations,
                'priority': 'low'
            })
        
        return actions

# Пример использования
async def main():
    """Пример использования виральных механик"""
    manager = ViralMechanicsManager()
    
    # Тестовые данные пользователя
    user_data = {
        'user_id': 12345,
        'username': 'testuser',
        'deals_count': 5,
        'referrals_count': 3,
        'referral_earnings': 50.0,
        'nft_certificates': [{'hash': '0x123...', 'amount': 1000}],
        'last_active_days': 1
    }
    
    # Обработка события завершения сделки
    actions = await manager.process_user_event(
        'first_deal_completed',
        user_data,
        {'amount': 5000, 'asset': 'btc'}
    )
    
    print("Действия для пользователя:")
    for action in actions:
        print(f"- {action['type']}: {action['content']}")

if __name__ == '__main__':
    asyncio.run(main())
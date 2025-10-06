#!/usr/bin/env python3
"""
AI Integration для ГАРАНТ СДЕЛОК 3.0
Локальная LLM-модель для анализа сделок и генерации рекомендаций
"""

import json
import logging
import re
from typing import Dict, List, Optional, Tuple
import asyncio
import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DealAnalyzer:
    """AI-анализатор сделок"""
    
    def __init__(self):
        self.risk_patterns = {
            'high_risk': [
                r'больш[а-я]*\s+сумм[а-я]*',
                r'срочн[а-я]*\s+сделк[а-я]*',
                r'без\s+гаранти[йи]',
                r'наличн[ы-я]*\s+встреч[а-я]*',
                r'перевод\s+на\s+карт[уы]'
            ],
            'medium_risk': [
                r'перв[а-я]*\s+сделк[а-я]*',
                r'нов[ы-я]*\s+аккаунт[а-я]*',
                r'без\s+истори[йи]',
                r'мал[а-я]*\s+сумм[а-я]*'
            ],
            'low_risk': [
                r'проверенн[ы-я]*\s+пользовател[ьи]',
                r'мног[о-я]*\s+сдел[о-я]*\s+в\s+истори[йи]',
                r'рекомендаци[йи]',
                r'гаранти[йи]'
            ]
        }
        
        self.asset_risk_multipliers = {
            'btc': 1.0,
            'eth': 1.1,
            'nft': 1.5,
            'usdt': 0.9,
            'fiat': 1.3
        }
        
        self.country_risk_multipliers = {
            'us': 1.0,
            'eu': 1.1,
            'ru': 1.2,
            'other': 1.5
        }

    def analyze_deal_text(self, text: str) -> Dict:
        """Анализ текста сделки на предмет рисков"""
        text_lower = text.lower()
        
        risk_score = 0
        risk_factors = []
        
        # Проверка паттернов высокого риска
        for pattern in self.risk_patterns['high_risk']:
            if re.search(pattern, text_lower):
                risk_score += 3
                risk_factors.append(f"Высокий риск: найдено '{pattern}'")
        
        # Проверка паттернов среднего риска
        for pattern in self.risk_patterns['medium_risk']:
            if re.search(pattern, text_lower):
                risk_score += 2
                risk_factors.append(f"Средний риск: найдено '{pattern}'")
        
        # Проверка паттернов низкого риска
        for pattern in self.risk_patterns['low_risk']:
            if re.search(pattern, text_lower):
                risk_score -= 1
                risk_factors.append(f"Низкий риск: найдено '{pattern}'")
        
        return {
            'risk_score': max(0, min(10, risk_score)),
            'risk_factors': risk_factors
        }

    def calculate_deal_risk(self, amount: float, asset: str, country: str = 'us', 
                          deal_text: str = '') -> Dict:
        """Расчет общего риска сделки"""
        
        # Базовый риск по сумме
        if amount > 100000:
            base_risk = 8
        elif amount > 50000:
            base_risk = 6
        elif amount > 10000:
            base_risk = 4
        elif amount > 1000:
            base_risk = 2
        else:
            base_risk = 1
        
        # Множители риска
        asset_multiplier = self.asset_risk_multipliers.get(asset, 1.0)
        country_multiplier = self.country_risk_multipliers.get(country, 1.0)
        
        # Анализ текста
        text_analysis = self.analyze_deal_text(deal_text)
        
        # Итоговый расчет
        final_risk = (base_risk * asset_multiplier * country_multiplier + 
                     text_analysis['risk_score']) / 2
        
        final_risk = min(10, max(1, final_risk))
        
        # Определение уровня риска
        if final_risk >= 7:
            risk_level = 'high'
            risk_emoji = '🔴'
            commission_rate = 0.015
        elif final_risk >= 4:
            risk_level = 'medium'
            risk_emoji = '🟡'
            commission_rate = 0.012
        else:
            risk_level = 'low'
            risk_emoji = '🟢'
            commission_rate = 0.0099
        
        # Рекомендации
        recommendations = self._generate_recommendations(final_risk, amount, asset, country)
        
        return {
            'risk_score': final_risk,
            'risk_level': risk_level,
            'risk_emoji': risk_emoji,
            'commission_rate': commission_rate,
            'commission_amount': amount * commission_rate,
            'recommendations': recommendations,
            'risk_factors': text_analysis['risk_factors']
        }

    def _generate_recommendations(self, risk_score: float, amount: float, 
                                asset: str, country: str) -> List[str]:
        """Генерация рекомендаций по сделке"""
        recommendations = []
        
        if amount > 50000:
            recommendations.append("Рекомендуем использовать мультиподпись для сделок > $50K")
        
        if risk_score > 6:
            recommendations.append("Добавьте верификацию через World ID для снижения комиссии на 0,2%")
            recommendations.append("Рассмотрите возможность разбиения на несколько сделок")
        
        if asset == 'nft':
            recommendations.append("Убедитесь в подлинности NFT через проверку контракта")
            recommendations.append("Проверьте историю владения NFT")
        
        if country not in ['us', 'eu']:
            recommendations.append("Дополнительная верификация требуется для данной страны")
            recommendations.append("Рассмотрите использование стабильных криптовалют")
        
        if risk_score < 3:
            recommendations.append("Сделка имеет низкий риск - можно выполнять")
        
        return recommendations

class DealConstructor:
    """AI-конструктор сделок"""
    
    def __init__(self):
        self.deal_templates = {
            'nft_eth': {
                'title': 'Покупка NFT за ETH',
                'steps': [
                    'Покупатель отправляет ETH в эскроу',
                    'Продавец подтверждает получение средств',
                    'NFT передается покупателю',
                    'ETH переводится продавцу'
                ],
                'estimated_time': '2-5 минут',
                'security_level': 'Высокий'
            },
            'btc_usdt': {
                'title': 'Обмен BTC на USDT',
                'steps': [
                    'Продавец BTC отправляет в эскроу',
                    'Покупатель отправляет USDT в эскроу',
                    'Автоматический обмен по курсу',
                    'Средства распределяются сторонам'
                ],
                'estimated_time': '3-7 минут',
                'security_level': 'Высокий'
            },
            'fiat_crypto': {
                'title': 'Покупка криптовалюты за фиат',
                'steps': [
                    'Покупатель отправляет фиат в эскроу',
                    'Продавец подтверждает получение',
                    'Криптовалюта передается покупателю',
                    'Фиат переводится продавцу'
                ],
                'estimated_time': '5-15 минут',
                'security_level': 'Средний'
            }
        }

    def construct_deal(self, buyer_asset: str, seller_asset: str, amount: float) -> Dict:
        """Конструкция схемы сделки"""
        
        # Определение типа сделки
        if buyer_asset == 'eth' and seller_asset == 'nft':
            deal_type = 'nft_eth'
        elif buyer_asset == 'usdt' and seller_asset == 'btc':
            deal_type = 'btc_usdt'
        elif buyer_asset == 'fiat' and seller_asset in ['btc', 'eth', 'usdt']:
            deal_type = 'fiat_crypto'
        else:
            deal_type = 'custom'
        
        if deal_type in self.deal_templates:
            template = self.deal_templates[deal_type]
            return {
                'title': template['title'],
                'steps': template['steps'],
                'estimated_time': template['estimated_time'],
                'security_level': template['security_level'],
                'amount': amount,
                'buyer_asset': buyer_asset,
                'seller_asset': seller_asset
            }
        else:
            # Генерация кастомной схемы
            return self._generate_custom_deal(buyer_asset, seller_asset, amount)

    def _generate_custom_deal(self, buyer_asset: str, seller_asset: str, amount: float) -> Dict:
        """Генерация кастомной схемы сделки"""
        return {
            'title': f'Обмен {buyer_asset.upper()} на {seller_asset.upper()}',
            'steps': [
                f'Покупатель отправляет {buyer_asset.upper()} в эскроу',
                f'Продавец подтверждает получение {buyer_asset.upper()}',
                f'{seller_asset.upper()} передается покупателю',
                f'{buyer_asset.upper()} переводится продавцу'
            ],
            'estimated_time': '3-10 минут',
            'security_level': 'Средний',
            'amount': amount,
            'buyer_asset': buyer_asset,
            'seller_asset': seller_asset
        }

class NFTCertificateGenerator:
    """Генератор NFT-сертификатов"""
    
    def __init__(self):
        self.certificate_templates = {
            'basic': {
                'title': 'SAFE DEAL CERTIFICATE',
                'description': 'Certificate of completed secure transaction',
                'attributes': ['amount', 'date', 'parties', 'asset']
            },
            'premium': {
                'title': 'PREMIUM TRUST CERTIFICATE',
                'description': 'High-value secure transaction certificate',
                'attributes': ['amount', 'date', 'parties', 'asset', 'risk_level', 'verification']
            }
        }

    def generate_certificate(self, deal_data: Dict, user_level: str = 'basic') -> Dict:
        """Генерация NFT-сертификата"""
        template = self.certificate_templates.get(user_level, self.certificate_templates['basic'])
        
        certificate = {
            'name': template['title'],
            'description': template['description'],
            'image': self._generate_certificate_image(deal_data),
            'attributes': self._generate_attributes(deal_data, template['attributes']),
            'external_url': f"https://garant-sdelok.com/certificate/{deal_data['deal_id']}",
            'background_color': '0f0c1a',
            'animation_url': None
        }
        
        return certificate

    def _generate_certificate_image(self, deal_data: Dict) -> str:
        """Генерация изображения сертификата (SVG)"""
        amount = deal_data.get('amount', 0)
        asset = deal_data.get('asset', 'CRYPTO')
        date = deal_data.get('date', '2025-01-01')
        
        svg = f"""
        <svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#8a6dff;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#00f0b0;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="400" height="300" fill="#0f0c1a"/>
            <rect x="20" y="20" width="360" height="260" fill="url(#grad)" rx="20"/>
            <rect x="25" y="25" width="350" height="250" fill="#0f0c1a" rx="15"/>
            <text x="200" y="80" text-anchor="middle" fill="url(#grad)" font-family="Arial" font-size="24" font-weight="bold">SAFE DEAL</text>
            <text x="200" y="110" text-anchor="middle" fill="url(#grad)" font-family="Arial" font-size="18">CERTIFICATE</text>
            <text x="200" y="160" text-anchor="middle" fill="#ffffff" font-family="Arial" font-size="16">Amount: ${amount:,.2f}</text>
            <text x="200" y="185" text-anchor="middle" fill="#ffffff" font-family="Arial" font-size="16">Asset: {asset.upper()}</text>
            <text x="200" y="210" text-anchor="middle" fill="#ffffff" font-family="Arial" font-size="14">Date: {date}</text>
            <text x="200" y="240" text-anchor="middle" fill="#8a6dff" font-family="Arial" font-size="12">Guaranteed by AI + Blockchain</text>
        </svg>
        """
        
        # В реальном проекте здесь будет загрузка в IPFS
        return f"data:image/svg+xml;base64,{svg.encode('utf-8').hex()}"

    def _generate_attributes(self, deal_data: Dict, attribute_types: List[str]) -> List[Dict]:
        """Генерация атрибутов сертификата"""
        attributes = []
        
        for attr_type in attribute_types:
            if attr_type == 'amount':
                attributes.append({
                    'trait_type': 'Amount',
                    'value': f"${deal_data.get('amount', 0):,.2f}"
                })
            elif attr_type == 'date':
                attributes.append({
                    'trait_type': 'Date',
                    'value': deal_data.get('date', '2025-01-01')
                })
            elif attr_type == 'asset':
                attributes.append({
                    'trait_type': 'Asset',
                    'value': deal_data.get('asset', 'CRYPTO').upper()
                })
            elif attr_type == 'risk_level':
                attributes.append({
                    'trait_type': 'Risk Level',
                    'value': deal_data.get('risk_level', 'LOW')
                })
            elif attr_type == 'verification':
                attributes.append({
                    'trait_type': 'Verification',
                    'value': 'AI Verified'
                })
        
        return attributes

class ViralMechanics:
    """Виральные механики"""
    
    def __init__(self):
        self.social_templates = {
            'twitter': "🚀 Just completed a secure deal with @GARANT_S_bot! Got my NFT certificate and earned ${earnings:.2f} in referral bonuses. Zero risk, maximum trust! #SafeDeals #Crypto #NFT",
            'telegram': "🎉 Завершил безопасную сделку через @GARANT_S_bot! Получил NFT-сертификат и заработал ${earnings:.2f} на рефералах. 0% риска, 100% доверия!",
            'linkedin': "Just used an AI-powered escrow service for a crypto transaction. The future of secure digital asset trading is here! #FinTech #Crypto #AI"
        }

    def generate_social_post(self, platform: str, deal_data: Dict, earnings: float = 0) -> str:
        """Генерация поста для соцсетей"""
        template = self.social_templates.get(platform, self.social_templates['twitter'])
        return template.format(earnings=earnings, **deal_data)

    def calculate_viral_score(self, user_data: Dict) -> float:
        """Расчет вирального скора пользователя"""
        score = 0
        
        # Бонусы за количество сделок
        deals_count = user_data.get('deals_count', 0)
        score += deals_count * 10
        
        # Бонусы за рефералов
        referrals_count = user_data.get('referrals_count', 0)
        score += referrals_count * 25
        
        # Бонусы за NFT-сертификаты
        nft_count = len(user_data.get('nft_certificates', []))
        score += nft_count * 15
        
        # Бонусы за активность
        if user_data.get('last_active_days', 0) < 7:
            score += 20
        
        return min(100, score)

# Главный класс AI-системы
class AISystem:
    """Главная AI-система ГАРАНТ СДЕЛОК 3.0"""
    
    def __init__(self):
        self.analyzer = DealAnalyzer()
        self.constructor = DealConstructor()
        self.nft_generator = NFTCertificateGenerator()
        self.viral_mechanics = ViralMechanics()

    async def process_deal_request(self, user_input: str, user_data: Dict) -> Dict:
        """Обработка запроса на сделку"""
        
        # Извлечение параметров из текста
        deal_params = self._extract_deal_parameters(user_input)
        
        # Анализ риска
        risk_analysis = self.analyzer.calculate_deal_risk(
            amount=deal_params.get('amount', 1000),
            asset=deal_params.get('asset', 'btc'),
            country=deal_params.get('country', 'us'),
            deal_text=user_input
        )
        
        # Конструкция сделки
        deal_scheme = self.constructor.construct_deal(
            buyer_asset=deal_params.get('buyer_asset', 'usdt'),
            seller_asset=deal_params.get('seller_asset', 'btc'),
            amount=deal_params.get('amount', 1000)
        )
        
        # Персонализация на основе истории пользователя
        personalized_recommendations = self._personalize_recommendations(
            risk_analysis['recommendations'], 
            user_data
        )
        
        return {
            'deal_scheme': deal_scheme,
            'risk_analysis': risk_analysis,
            'personalized_recommendations': personalized_recommendations,
            'estimated_commission': risk_analysis['commission_amount'],
            'viral_potential': self.viral_mechanics.calculate_viral_score(user_data)
        }

    def _extract_deal_parameters(self, text: str) -> Dict:
        """Извлечение параметров сделки из текста"""
        text_lower = text.lower()
        
        # Извлечение суммы
        amount_match = re.search(r'(\d+(?:,\d{3})*(?:\.\d{2})?)', text)
        amount = float(amount_match.group(1).replace(',', '')) if amount_match else 1000
        
        # Извлечение активов
        assets = []
        if 'btc' in text_lower or 'bitcoin' in text_lower:
            assets.append('btc')
        if 'eth' in text_lower or 'ethereum' in text_lower:
            assets.append('eth')
        if 'nft' in text_lower:
            assets.append('nft')
        if 'usdt' in text_lower or 'tether' in text_lower:
            assets.append('usdt')
        if 'usd' in text_lower or 'доллар' in text_lower:
            assets.append('fiat')
        
        return {
            'amount': amount,
            'asset': assets[0] if assets else 'btc',
            'buyer_asset': assets[0] if assets else 'usdt',
            'seller_asset': assets[1] if len(assets) > 1 else 'btc',
            'country': 'us'  # По умолчанию
        }

    def _personalize_recommendations(self, recommendations: List[str], user_data: Dict) -> List[str]:
        """Персонализация рекомендаций на основе истории пользователя"""
        personalized = recommendations.copy()
        
        # Добавление персонализированных рекомендаций
        if user_data.get('deals_count', 0) == 0:
            personalized.append("🎁 Первая сделка бесплатна - отличный способ попробовать сервис!")
        
        if user_data.get('referral_earnings', 0) > 100:
            personalized.append("💰 Вы активный рефер - рассмотрите премиум-функции!")
        
        if len(user_data.get('nft_certificates', [])) > 5:
            personalized.append("🏆 У вас много сертификатов - вы надежный пользователь!")
        
        return personalized

# Пример использования
async def main():
    """Пример использования AI-системы"""
    ai_system = AISystem()
    
    # Тестовые данные пользователя
    user_data = {
        'deals_count': 2,
        'referral_earnings': 25.50,
        'nft_certificates': [{'hash': '0x123...', 'amount': 1000}],
        'last_active_days': 3
    }
    
    # Обработка запроса
    result = await ai_system.process_deal_request(
        "Хочу купить NFT за 5 ETH",
        user_data
    )
    
    print("Результат анализа:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    asyncio.run(main())
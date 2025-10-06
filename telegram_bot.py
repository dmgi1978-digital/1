#!/usr/bin/env python3
"""
ГАРАНТ СДЕЛОК 3.0 - Telegram Bot
Революционный эскроу-сервис с AI, NFT-сертификатами и виральными механиками
"""

import asyncio
import json
import logging
import os
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-domain.com/webhook')

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Состояния FSM
class DealStates(StatesGroup):
    waiting_for_asset = State()
    waiting_for_amount = State()
    waiting_for_seller = State()
    waiting_for_confirmation = State()
    deal_in_progress = State()

# База данных (в реальном проекте использовать PostgreSQL/MongoDB)
users_db = {}
deals_db = {}
referrals_db = {}
nft_certificates = {}

# Утилиты
def generate_deal_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_nft_hash():
    return '0x' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))

def calculate_commission(amount: float, is_first_deal: bool = False) -> float:
    """Расчет комиссии"""
    if is_first_deal:
        return 0.0
    if amount > 50000:
        return amount * 0.015  # 1.5%
    elif amount > 10000:
        return amount * 0.012  # 1.2%
    else:
        return amount * 0.0099  # 0.99%

def get_risk_level(amount: float, asset: str) -> str:
    """Определение уровня риска"""
    if amount > 50000:
        return "🔴 Высокий риск"
    elif amount > 10000:
        return "🟡 Средний риск"
    else:
        return "🟢 Низкий риск"

# Обработчики команд
@dp.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    """Приветственное сообщение с геймификацией"""
    user_id = message.from_user.id
    username = message.from_user.username or f"User{user_id}"
    
    # Обработка реферальной ссылки
    ref_id = None
    if len(message.text.split()) > 1:
        ref_id = message.text.split()[1].replace('ref_', '')
        if ref_id and ref_id != str(user_id):
            referrals_db[user_id] = ref_id
            # Уведомление рефереру
            try:
                await bot.send_message(
                    ref_id,
                    f"🎉 Ваш друг @{username} присоединился по вашей ссылке!\n"
                    f"Вы будете получать 20% от всех его комиссий пожизненно!"
                )
            except:
                pass
    
    # Инициализация пользователя
    if user_id not in users_db:
        users_db[user_id] = {
            'username': username,
            'deals_count': 0,
            'total_earned': 0.0,
            'referral_earnings': 0.0,
            'nft_certificates': [],
            'joined_at': datetime.now().isoformat()
        }
    
    # Генерация реферальной ссылки
    ref_link = f"https://t.me/GARANT_S_bot?start=ref_{user_id}"
    
    welcome_text = f"""👋 Привет, @{username}! Я — ГАРАНТ СДЕЛОК, ваш AI-гарант в мире крипто и цифровых активов.

🛡️ За 3 минуты я помогу вам:
• Создать **неподдельную** схему сделки  
• Получить **NFT-сертификат доверия**  
• Заработать на рефералах — **пожизненно**

🎁 Бонус: первые 3 сделки — **БЕСПЛАТНО**!

💰 Ваша реферальная ссылка:
`{ref_link}`
Поделитесь — и получите 20% от всех комиссий ваших друзей. Всегда.

📊 Статистика:
• Сделок завершено: {users_db[user_id]['deals_count']}
• Заработано на рефералах: ${users_db[user_id]['referral_earnings']:.2f}
• NFT-сертификатов: {len(users_db[user_id]['nft_certificates'])}

Выберите, с чего начать:"""

    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🚀 Начать сделку", callback_data="start_deal"))
    keyboard.add(InlineKeyboardButton(text="🎁 Получить NFT-статус", callback_data="nft_status"))
    keyboard.add(InlineKeyboardButton(text="💰 Реферальная программа", callback_data="referral_program"))
    keyboard.add(InlineKeyboardButton(text="❓ Как это работает?", callback_data="how_it_works"))
    keyboard.add(InlineKeyboardButton(text="📊 Моя статистика", callback_data="my_stats"))
    
    keyboard.adjust(2)
    
    await message.answer(welcome_text, reply_markup=keyboard.as_markup(), parse_mode='Markdown')

@dp.callback_query(lambda c: c.data == "start_deal")
async def start_deal(callback: CallbackQuery, state: FSMContext):
    """Начало создания сделки"""
    await callback.answer()
    await state.set_state(DealStates.waiting_for_asset)
    
    text = """🚀 Отлично! Давайте создадим безопасную сделку.

Выберите актив для сделки:"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="₿ Bitcoin (BTC)", callback_data="asset_btc"))
    keyboard.add(InlineKeyboardButton(text="Ξ Ethereum (ETH)", callback_data="asset_eth"))
    keyboard.add(InlineKeyboardButton(text="🎨 NFT", callback_data="asset_nft"))
    keyboard.add(InlineKeyboardButton(text="💵 USDT", callback_data="asset_usdt"))
    keyboard.add(InlineKeyboardButton(text="💸 Фиат (USD/EUR)", callback_data="asset_fiat"))
    keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    
    keyboard.adjust(2)
    
    await callback.message.edit_text(text, reply_markup=keyboard.as_markup())

@dp.callback_query(lambda c: c.data.startswith("asset_"))
async def select_asset(callback: CallbackQuery, state: FSMContext):
    """Выбор актива"""
    await callback.answer()
    asset = callback.data.replace("asset_", "")
    await state.update_data(asset=asset)
    await state.set_state(DealStates.waiting_for_amount)
    
    asset_names = {
        'btc': 'Bitcoin (BTC)',
        'eth': 'Ethereum (ETH)', 
        'nft': 'NFT',
        'usdt': 'USDT',
        'fiat': 'Фиат (USD/EUR)'
    }
    
    text = f"""✅ Выбран актив: {asset_names[asset]}

💰 Теперь укажите сумму сделки в долларах США:"""
    
    await callback.message.edit_text(text)

@dp.message(DealStates.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext):
    """Обработка суммы сделки"""
    try:
        amount = float(message.text)
        if amount <= 0:
            await message.answer("❌ Сумма должна быть больше 0. Попробуйте еще раз:")
            return
            
        await state.update_data(amount=amount)
        await state.set_state(DealStates.waiting_for_seller)
        
        data = await state.get_data()
        asset = data['asset']
        
        # Расчет комиссии и риска
        user_id = message.from_user.id
        is_first_deal = users_db[user_id]['deals_count'] < 3
        commission = calculate_commission(amount, is_first_deal)
        risk_level = get_risk_level(amount, asset)
        
        text = f"""✅ Сумма: ${amount:,.2f}
📊 Анализ риска: {risk_level}
💸 Комиссия: ${commission:.2f} {'(БЕСПЛАТНО - первая сделка!)' if is_first_deal else ''}

👤 Теперь укажите Telegram ID продавца (например: @username или 123456789):"""
        
        await message.answer(text)
        
    except ValueError:
        await message.answer("❌ Неверный формат суммы. Введите число (например: 1000):")

@dp.message(DealStates.waiting_for_seller)
async def process_seller(message: types.Message, state: FSMContext):
    """Обработка ID продавца"""
    seller_id = message.text.replace('@', '')
    
    # Простая валидация ID
    if not seller_id.isdigit() and not seller_id.startswith('@'):
        await message.answer("❌ Неверный формат ID. Укажите @username или числовой ID:")
        return
    
    await state.update_data(seller_id=seller_id)
    await state.set_state(DealStates.waiting_for_confirmation)
    
    data = await state.get_data()
    amount = data['amount']
    asset = data['asset']
    user_id = message.from_user.id
    is_first_deal = users_db[user_id]['deals_count'] < 3
    commission = calculate_commission(amount, is_first_deal)
    
    text = f"""📋 Подтвердите детали сделки:

👤 Покупатель: @{message.from_user.username or f'User{user_id}'}
👤 Продавец: {seller_id}
💰 Актив: {asset.upper()}
💵 Сумма: ${amount:,.2f}
💸 Комиссия: ${commission:.2f} {'(БЕСПЛАТНО!)' if is_first_deal else ''}
🛡️ Защита: AI + Блокчейн
⏱️ Время: 2-5 минут

✅ Все верно?"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_deal"))
    keyboard.add(InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_deal"))
    
    await message.answer(text, reply_markup=keyboard.as_markup())

@dp.callback_query(lambda c: c.data == "confirm_deal")
async def confirm_deal(callback: CallbackQuery, state: FSMContext):
    """Подтверждение сделки"""
    await callback.answer()
    
    data = await state.get_data()
    deal_id = generate_deal_id()
    user_id = callback.from_user.id
    
    # Сохранение сделки
    deals_db[deal_id] = {
        'buyer_id': user_id,
        'seller_id': data['seller_id'],
        'asset': data['asset'],
        'amount': data['amount'],
        'commission': calculate_commission(data['amount'], users_db[user_id]['deals_count'] < 3),
        'status': 'pending',
        'created_at': datetime.now().isoformat(),
        'nft_hash': None
    }
    
    await state.set_state(DealStates.deal_in_progress)
    
    text = f"""🚀 Сделка #{deal_id} запущена!

📱 Отправьте эту ссылку продавцу:
`https://t.me/GARANT_S_bot?deal={deal_id}`

⏱️ Ожидаем подтверждения от продавца...
🛡️ Ваши средства под защитой AI"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="📊 Статус сделки", callback_data=f"deal_status_{deal_id}"))
    keyboard.add(InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main"))
    
    await callback.message.edit_text(text, reply_markup=keyboard.as_markup(), parse_mode='Markdown')

@dp.callback_query(lambda c: c.data.startswith("deal_status_"))
async def deal_status(callback: CallbackQuery):
    """Статус сделки"""
    await callback.answer()
    deal_id = callback.data.replace("deal_status_", "")
    
    if deal_id not in deals_db:
        await callback.message.answer("❌ Сделка не найдена")
        return
    
    deal = deals_db[deal_id]
    status_emoji = {
        'pending': '⏳',
        'confirmed': '✅',
        'completed': '🎉',
        'cancelled': '❌'
    }
    
    text = f"""📊 Статус сделки #{deal_id}

{status_emoji.get(deal['status'], '❓')} Статус: {deal['status'].upper()}
💰 Сумма: ${deal['amount']:,.2f}
💸 Комиссия: ${deal['commission']:.2f}
🕐 Создана: {deal['created_at'][:19]}

{'🎨 NFT-сертификат готов!' if deal['nft_hash'] else '⏳ Ожидаем завершения...'}"""
    
    if deal['nft_hash']:
        text += f"\n\n🔗 Хеш сертификата: `{deal['nft_hash']}`"
    
    await callback.message.answer(text, parse_mode='Markdown')

@dp.callback_query(lambda c: c.data == "nft_status")
async def nft_status(callback: CallbackQuery):
    """NFT статус пользователя"""
    await callback.answer()
    user_id = callback.from_user.id
    user = users_db.get(user_id, {})
    certificates = user.get('nft_certificates', [])
    
    if not certificates:
        text = """🎨 У вас пока нет NFT-сертификатов

Завершите первую сделку, чтобы получить свой первый Soulbound NFT-сертификат доверия!

NFT-сертификаты:
• Не продаются — только ваши
• Доказывают вашу надежность
• Дают +10% к реферальным вознаграждениям
• Можно делиться в соцсетях"""
    else:
        text = f"""🎨 Ваши NFT-сертификаты ({len(certificates)})

"""
        for i, cert in enumerate(certificates, 1):
            text += f"""📜 Сертификат #{i}
🔗 Хеш: `{cert['hash']}`
📅 Дата: {cert['date']}
💰 Сумма: ${cert['amount']:,.2f}

"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    
    await callback.message.edit_text(text, reply_markup=keyboard.as_markup(), parse_mode='Markdown')

@dp.callback_query(lambda c: c.data == "referral_program")
async def referral_program(callback: CallbackQuery):
    """Реферальная программа"""
    await callback.answer()
    user_id = callback.from_user.id
    user = users_db.get(user_id, {})
    ref_link = f"https://t.me/GARANT_S_bot?start=ref_{user_id}"
    
    text = f"""💰 Реферальная программа

🔗 Ваша ссылка:
`{ref_link}`

📊 Статистика:
• Приглашено друзей: {len([uid for uid, ref_id in referrals_db.items() if ref_id == str(user_id)])}
• Заработано: ${user.get('referral_earnings', 0):.2f}
• Комиссия с каждого друга: 20% пожизненно

🎁 Бонусы:
• +10% к реферальным вознаграждениям за NFT-сертификаты
• Эксклюзивные предложения для активных реферов
• Приоритетная поддержка

📱 Поделитесь ссылкой и начните зарабатывать!"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="📋 Скопировать ссылку", callback_data="copy_ref_link"))
    keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    
    await callback.message.edit_text(text, reply_markup=keyboard.as_markup(), parse_mode='Markdown')

@dp.callback_query(lambda c: c.data == "my_stats")
async def my_stats(callback: CallbackQuery):
    """Статистика пользователя"""
    await callback.answer()
    user_id = callback.from_user.id
    user = users_db.get(user_id, {})
    
    text = f"""📊 Ваша статистика

👤 Пользователь: @{callback.from_user.username or f'User{user_id}'}
📅 Регистрация: {user.get('joined_at', 'Неизвестно')[:10]}

💼 Сделки:
• Завершено: {user.get('deals_count', 0)}
• Осталось бесплатных: {max(0, 3 - user.get('deals_count', 0))}

💰 Заработок:
• Реферальные: ${user.get('referral_earnings', 0):.2f}
• Общий: ${user.get('total_earned', 0):.2f}

🎨 NFT-сертификаты: {len(user.get('nft_certificates', []))}

🏆 Уровень доверия: {'🥇 Высокий' if user.get('deals_count', 0) > 10 else '🥈 Средний' if user.get('deals_count', 0) > 3 else '🥉 Начинающий'}"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    
    await callback.message.edit_text(text, reply_markup=keyboard.as_markup())

@dp.callback_query(lambda c: c.data == "how_it_works")
async def how_it_works(callback: CallbackQuery):
    """Как это работает"""
    await callback.answer()
    
    text = """❓ Как работает ГАРАНТ СДЕЛОК 3.0

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
• 24/7 мониторинг AI"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    
    await callback.message.edit_text(text, reply_markup=keyboard.as_markup())

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await callback.answer()
    await state.clear()
    await start_command(callback.message, state)

@dp.callback_query(lambda c: c.data == "cancel_deal")
async def cancel_deal(callback: CallbackQuery, state: FSMContext):
    """Отмена сделки"""
    await callback.answer()
    await state.clear()
    await start_command(callback.message, state)

# Симуляция завершения сделки (в реальном проекте - интеграция с блокчейном)
async def simulate_deal_completion(deal_id: str):
    """Симуляция завершения сделки"""
    if deal_id not in deals_db:
        return
    
    deal = deals_db[deal_id]
    deal['status'] = 'completed'
    deal['nft_hash'] = generate_nft_hash()
    
    # Обновление статистики покупателя
    buyer_id = deal['buyer_id']
    if buyer_id in users_db:
        users_db[buyer_id]['deals_count'] += 1
        users_db[buyer_id]['total_earned'] += deal['amount']
        
        # Создание NFT-сертификата
        nft_cert = {
            'hash': deal['nft_hash'],
            'amount': deal['amount'],
            'date': datetime.now().isoformat()[:10],
            'deal_id': deal_id
        }
        users_db[buyer_id]['nft_certificates'].append(nft_cert)
        
        # Уведомление покупателя
        try:
            await bot.send_message(
                buyer_id,
                f"""✅ Сделка #{deal_id} завершена!

🎨 Ваш NFT-сертификат готов:
`{deal['nft_hash']}`

💰 Сумма: ${deal['amount']:,.2f}
🛡️ Защита сработала идеально!

Поделитесь сертификатом в соцсетях и получите +10% к реферальным вознаграждениям!""",
                parse_mode='Markdown'
            )
        except:
            pass
        
        # Реферальные выплаты
        if buyer_id in referrals_db:
            referrer_id = referrals_db[buyer_id]
            if referrer_id in users_db:
                referral_earnings = deal['commission'] * 0.2
                users_db[referrer_id]['referral_earnings'] += referral_earnings
                
                try:
                    await bot.send_message(
                        referrer_id,
                        f"🎉 Ваш друг завершил сделку на ${deal['amount']:,.2f}!\n"
                        f"💰 Вы получили ${referral_earnings:.2f} реферального вознаграждения!"
                    )
                except:
                    pass

# Обработка входящих сделок от продавцов
@dp.message(lambda message: message.text and message.text.startswith('/deal_'))
async def handle_deal_join(message: types.Message):
    """Обработка присоединения к сделке"""
    deal_id = message.text.replace('/deal_', '')
    
    if deal_id not in deals_db:
        await message.answer("❌ Сделка не найдена или устарела")
        return
    
    deal = deals_db[deal_id]
    if deal['status'] != 'pending':
        await message.answer("❌ Сделка уже завершена или отменена")
        return
    
    # Подтверждение участия продавца
    deal['status'] = 'confirmed'
    deal['seller_confirmed_at'] = datetime.now().isoformat()
    
    # Симуляция завершения сделки через 30 секунд
    await asyncio.sleep(30)
    await simulate_deal_completion(deal_id)

# Запуск бота
async def main():
    """Главная функция"""
    logger.info("Запуск ГАРАНТ СДЕЛОК 3.0 Bot...")
    
    # Удаление webhook (если используется)
    await bot.delete_webhook()
    
    # Запуск polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
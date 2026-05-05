#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Telegram Bot для анализа криптовалют
Запуск на Render.com (режим polling)
"""

import os
import logging
import asyncio
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ==================== 🔧 НАСТРОЙКИ ====================
# Токен берём из переменных окружения Render
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]  # Вывод в консоль Render
)
logger = logging.getLogger(__name__)

# ==================== 💬 КОМАНДЫ БОТА ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    logger.info(f"📨 /start от @{user.username} (ID: {user.id})")
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"Я бот для анализа криптовалют 📈\n"
        f"Сервер запущен на Render.com 🚀\n\n"
        f"Доступные команды:\n"
        f"/test — проверить соединение\n"
        f"/help — справка"
    )

async def test_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /test"""
    logger.info("📨 /test команда")
    
    # Проверяем соединение с API Telegram
    try:
        me = await context.bot.get_me()
        await update.message.reply_text(
            f"✅ Бот работает!\n\n"
            f"🤖 Имя: @{me.username}\n"
            f"🆔 ID: {me.id}\n"
            f"⏰ Время сервера: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        logger.info("✅ /test успешен")
    except Exception as e:
        logger.error(f"❌ Ошибка /test: {e}")
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "📚 **Справка по командам**:\n\n"
        "/start — приветствие и меню\n"
        "/test — проверка работы бота\n"
        "/help — эта справка\n\n"
        "💡 Бот анализирует криптовалюты через Binance API."
    )

# ==================== 🧠 АНАЛИЗ (заглушка) ====================

async def analyze_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Заглушка для команды анализа"""
    symbol = context.args[0].upper() if context.args else "BTC/USDT"
    
    status = await update.message.reply_text(f"🔍 Анализирую {symbol}...")
    
    # Имитация анализа (замените на реальную логику)
    await asyncio.sleep(2)
    
    await status.edit_text(
        f"📊 **Результат анализа {symbol}**:\n\n"
        f"🎯 Рекомендация: 🟢 LONG\n"
        f"💰 Прогноз: $67,234.50 (+1.23%)\n"
        f"📈 Уверенность: 78.4%\n"
        f"✅ Точность модели: 82.1%"
    )

# ==================== 🔧 СИСТЕМНЫЕ ФУНКЦИИ ====================

async def post_init(application: Application):
    """Инициализация при старте"""
    logger.info("🔄 Инициализация бота...")
    try:
        # Удаляем вебхук (на случай, если был настроен)
        await application.bot.delete_webhook()
        
        # Проверяем подключение
        me = await application.bot.get_me()
        logger.info(f"✅ Бот подключён: @{me.username} (ID: {me.id})")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации: {e}")
        raise

def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Глобальный обработчик ошибок"""
    logger.error(f"❌ Ошибка при обработке обновления: {context.error}", exc_info=True)

# ==================== 🚀 ЗАПУСК ====================

def main():
    """Точка входа"""
    logger.info("=" * 60)
    logger.info("🚀 ЗАПУСК TELEGRAM БОТА НА RENDER")
    logger.info(f"🔐 Токен: {'✓' if BOT_TOKEN else '✗ НЕ НАЙДЕН'}")
    logger.info("=" * 60)
    
    # Проверка токена
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не найден в переменных окружения!")
        logger.error("💡 Добавьте BOT_TOKEN в Render → Environment Variables")
        return
    
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
        
        # Регистрируем хендлеры команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("test", test_cmd))
        application.add_handler(CommandHandler("help", help_cmd))
        application.add_handler(CommandHandler("analyze", analyze_cmd))
        
        # Глобальный обработчик ошибок
        application.add_error_handler(error_handler)
        
        logger.info("✅ Хендлеры зарегистрированы")
        logger.info("🚀 Запуск polling...")
        
        # 🔥 ЗАПУСК ЧЕРЕZ POLLING (работает на Render Free)
        # drop_pending_updates=True — игнорируем старые сообщения при старте
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
        )
        
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()

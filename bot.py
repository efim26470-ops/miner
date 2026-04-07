import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Настройки ---
# Токен вашего бота, полученный от @BotFather
BOT_TOKEN = os.environ.get('BOT_TOKEN')
# Публичный URL вашей игры на Railway (например, https://sapper.up.railway.app)
GAME_URL = os.environ.get('GAME_URL')
# Короткое имя игры, которое вы задали в BotFather
GAME_SHORT_NAME = os.environ.get('GAME_SHORT_NAME') # Например, 'sapper_game'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Обработчики команд ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение с кнопкой для запуска игры."""
    # Создаем кнопку, которая откроет игру
    keyboard = [[InlineKeyboardButton("💣 Играть в Сапёра", callback_data="play_game")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в игру 'Сапёр'! Нажмите на кнопку ниже, чтобы начать.",
        reply_markup=reply_markup
    )

async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатие на кнопку 'Играть' и открывает игру."""
    query = update.callback_query
    await query.answer() # Обязательно отвечаем на callback, чтобы убрать "часики" на кнопке

    # Отправляем игру пользователю
    await context.bot.send_game(
        chat_id=query.message.chat_id,
        game_short_name=GAME_SHORT_NAME,
        # reply_to_message_id=query.message.message_id, # Можно привязать к сообщению с кнопкой
    )

# --- Обработчик callback'ов (для запуска игры) ---
async def game_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Вызывается, когда пользователь нажимает на кнопку 'Play GameName' в сообщении с игрой."""
    query = update.callback_query
    await query.answer(url=GAME_URL) # Это действие и открывает игру!

# --- Обработчик ошибок ---
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логирует ошибки."""
    logging.error(msg="Exception while handling an update:", exc_info=context.error)

# --- Запуск бота ---
def main() -> None:
    """Запускает бота."""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(play_game, pattern="play_game"))
    application.add_handler(CallbackQueryHandler(game_callback, pattern="game_short_name")) # Важно!

    # Регистрируем обработчик ошибок
    application.add_error_handler(error_handler)

    # Запускаем бота (long polling)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
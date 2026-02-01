import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.core.config import settings
from loguru import logger
from app.models.tender import Tender

# Инициализация бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в Tender Analyzer! 🛠️\n"
        "Я буду уведомлять о новых тендерах.\n"
        "/help - список команд."
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "/start - Запуск\n"
        "/prefs - Настройки (скоро)\n"
    )

async def send_telegram_notification(tender: Tender):
    """
    Отправка уведомления пользователю/в канал.
    """
    # Заглушка: Здесь должна быть отправка по chat_id из базы
    
    msg = (
        f"🚨 **Найден тендер!** 🚨\n\n"
        f"📜 **{tender.title}**\n"
        f"💰 **{tender.max_price}**\n"
        f"🏢 {tender.customer_name}\n\n"
        f"🔗 [Открыть]({tender.link})"
    )
    
    # Кнопка генерации КП
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ Создать КП", callback_data=f"quote_{tender.zakupki_id}")]
    ])
    
    logger.info(f"БОТ ХОТЕЛ ОТПРАВИТЬ:\n{msg}")
    
    # if settings.DEBUG_CHAT_ID:
    #     await bot.send_message(chat_id=settings.DEBUG_CHAT_ID, text=msg, parse_mode="Markdown", reply_markup=kb)

dp.include_router(router)

async def start_bot():
    logger.info("Запуск Telegram бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())

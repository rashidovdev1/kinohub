import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from database.database import db
from handlers import user, admin

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    """Bot ishga tushganda"""
    # Database ga ulanish
    await db.connect()
    
    # Bot ma'lumotlarini olish
    bot_info = await bot.get_me()
    logger.info(f"✅ Bot ishga tushdi: @{bot_info.username}")
    
    # Adminni xabardor qilish
    try:
        await bot.send_message(
            config.ADMIN_ID,
            "🤖 <b>Bot muvaffaqiyatli ishga tushdi!</b>",
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Adminni xabardor qilishda xatolik: {e}")


async def on_shutdown(bot: Bot):
    """Bot to'xtaganda"""
    await db.disconnect()
    logger.info("❌ Bot to'xtadi")


async def main():
    """Asosiy funksiya"""
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher(storage=MemoryStorage())
    
    # Handlerlarni ro'yxatdan o'tkazish
    dp.include_router(admin.router)
    dp.include_router(user.router)

    
    # Startup va shutdown eventlar
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Botni ishga tushirish
    try:
        logger.info("🚀 Bot ishga tushmoqda...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi (Ctrl+C)")

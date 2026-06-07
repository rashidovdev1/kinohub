import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
import config
from database.database import db
from handlers import user, admin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def health_check(request):
    return web.Response(text="OK")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    logger.info("✅ Health check server ishga tushdi: port 8000")

async def on_startup(bot: Bot):
    await db.connect()
    bot_info = await bot.get_me()
    logger.info(f"✅ Bot ishga tushdi: @{bot_info.username}")
    try:
        await bot.send_message(
            config.ADMIN_ID,
            "🤖 <b>Bot muvaffaqiyatli ishga tushdi!</b>",
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Adminni xabardor qilishda xatolik: {e}")

async def on_shutdown(bot: Bot):
    await db.disconnect()
    logger.info("❌ Bot to'xtadi")

async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(admin.router)
    dp.include_router(user.router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await start_web_server()

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
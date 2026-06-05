from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ChatJoinRequest
from aiogram.fsm.context import FSMContext

import config
from database.database import db
from keyboards import user_kb
from handlers.subscription import check_user_subscription, auto_approve_join_request

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    """Start buyrug'i"""
    # Userni bazaga qo'shish
    await db.add_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    # Obunani tekshirish
    subscription_status = await check_user_subscription(bot, message.from_user.id)
    
    if subscription_status['pending_channels']:
        # Zapros kutilmoqda
        await message.answer(
            "⏳ <b>Sizning zaproslaringiz ko'rib chiqilmoqda...</b>\n\n"
            "Iltimos, admin tasdiqini kuting.\n"
            "Tasdiqlanganidan keyin botdan foydalanishingiz mumkin.",
            parse_mode='HTML'
        )
        return
    
    if not subscription_status['subscribed']:
        # Obuna yo'q
        text = config.TEXTS['start']
        for idx, channel in enumerate(subscription_status['not_subscribed_channels'], 1):
            text += f"{idx}. {channel.get('username', 'Private kanal')}\n"
        
        await message.answer(
            text,
            reply_markup=user_kb.subscription_kb(subscription_status['not_subscribed_channels']),
            parse_mode='HTML'
        )
        return
    
    # Obuna bor - asosiy menyuni ko'rsatish
    await message.answer(
        config.TEXTS['start_success'],
        reply_markup=user_kb.main_menu_kb(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery, bot: Bot):
    """Obunani tekshirish tugmasi bosilganda"""
    await callback.answer(config.TEXTS['checking_subscription'])
    
    subscription_status = await check_user_subscription(bot, callback.from_user.id)
    
    if subscription_status['pending_channels']:
        await callback.message.edit_text(
            "⏳ <b>Sizning zaproslaringiz ko'rib chiqilmoqda...</b>\n\n"
            "Iltimos, admin tasdiqini kuting.",
            parse_mode='HTML'
        )
        return
    
    if subscription_status['subscribed']:
        await callback.message.delete()
        await callback.message.answer(
            config.TEXTS['start_success'],
            reply_markup=user_kb.main_menu_kb(),
            parse_mode='HTML'
        )
    else:
        text = config.TEXTS['not_subscribed']
        for idx, channel in enumerate(subscription_status['not_subscribed_channels'], 1):
            text += f"{idx}. {channel.get('username', 'Private kanal')}\n"
        
        await callback.message.edit_text(
            text,
            reply_markup=user_kb.subscription_kb(subscription_status['not_subscribed_channels']),
            parse_mode='HTML'
        )


@router.chat_join_request()
async def handle_join_request(update: ChatJoinRequest, bot: Bot):
    """Private kanalga zapros yuborilganda avtomatik qabul qilish"""
    # Zaprosni qabul qilish
    approved = await auto_approve_join_request(bot, update.chat.id, update.from_user.id)
    
    if approved:
        # Userga xabar yuborish
        await bot.send_message(
            update.from_user.id,
            "✅ <b>Zapros qabul qilindi!</b>\n\n"
            "Endi botdan foydalanishingiz mumkin.\n"
            "/start buyrug'ini bosing.",
            parse_mode='HTML'
        )


@router.message(F.text == "🔍 Qidirish")
async def search_movies(message: Message, bot: Bot):
    """Qidirish bo'limi"""
    # Obunani tekshirish
    subscription_status = await check_user_subscription(bot, message.from_user.id)
    
    if not subscription_status['subscribed']:
        text = config.TEXTS['not_subscribed']
        await message.answer(
            text,
            reply_markup=user_kb.subscription_kb(subscription_status['not_subscribed_channels']),
            parse_mode='HTML'
        )
        return
    
    await message.answer(
        "🔍 <b>Kino qidirish</b>\n\n"
        "Kino nomini yoki kodini yuboring:\n\n"
        "Masalan:\n"
        "• <code>Avatar</code>\n"
        "• <code>123</code>",
        parse_mode='HTML'
    )


@router.message(F.text == "📊 Statistika")
async def show_statistics(message: Message, bot: Bot):
    """Statistikani ko'rsatish"""
    # Obunani tekshirish
    subscription_status = await check_user_subscription(bot, message.from_user.id)
    
    if not subscription_status['subscribed']:
        text = config.TEXTS['not_subscribed']
        await message.answer(
            text,
            reply_markup=user_kb.subscription_kb(subscription_status['not_subscribed_channels']),
            parse_mode='HTML'
        )
        return
    
    # Statistika ma'lumotlarini olish
    users_count = await db.get_users_count()
    movies_count = await db.get_movies_count()
    total_views = await db.get_total_views()
    
    text = f"""
📊 <b>Bot Statistikasi</b>

👥 Foydalanuvchilar: <b>{users_count}</b>
🎬 Kinolar: <b>{movies_count}</b>
👁 Jami ko'rishlar: <b>{total_views}</b>
"""
    
    await message.answer(text, parse_mode='HTML')


@router.message(F.text == "💬 Bog'lanish")
async def contact_admin(message: Message, bot: Bot):
    """Admin bilan bog'lanish"""
    # Obunani tekshirish
    subscription_status = await check_user_subscription(bot, message.from_user.id)
    
    if not subscription_status['subscribed']:
        text = config.TEXTS['not_subscribed']
        await message.answer(
            text,
            reply_markup=user_kb.subscription_kb(subscription_status['not_subscribed_channels']),
            parse_mode='HTML'
        )
        return
    
    await message.answer(
        "💬 <b>Bog'lanish</b>\n\n"
        "Reklama va hamkorlik uchun admin bilan bog'laning:",
        reply_markup=user_kb.contact_kb(),
        parse_mode='HTML'
    )


@router.message(F.text)
async def search_movie_by_text(message: Message, bot: Bot):
    """Matn orqali kino qidirish"""
    # Obunani tekshirish
    subscription_status = await check_user_subscription(bot, message.from_user.id)
    
    if not subscription_status['subscribed']:
        text = config.TEXTS['not_subscribed']
        await message.answer(
            text,
            reply_markup=user_kb.subscription_kb(subscription_status['not_subscribed_channels']),
            parse_mode='HTML'
        )
        return
    
    # Admin buyruqlarini o'tkazib yuborish
    if message.text in ["➕ Kino qo'shish", "🗑 Kino o'chirish", "✏️ Kino tahrirlash",
                        "📢 Xabar yuborish", "⚙️ Kanallar", "🔙 Orqaga", "❌ Bekor qilish",
                        "⏭ O'tkazib yuborish"] or message.text.startswith('/'):
        return
    
    # Kinoni qidirish
    search_msg = await message.answer("🔍 Qidirilmoqda...")
    
    movie = await db.search_movie(message.text)
    
    if not movie:
        await search_msg.edit_text(config.TEXTS['movie_not_found'])
        return
    
    # Kino topildi - yuborish
    await search_msg.delete()
    
    # Ko'rishlar sonini oshirish
    await db.update_movie_views(movie['id'])
    
    # Kino haqida ma'lumot
    caption = f"🎬 <b>{movie['title']}</b>\n\n🔢 Kod: <code>{movie['id']}</code>"
    
    if movie['trailer_link']:
        caption += f"\n🔗 Trailer: {movie['trailer_link']}"
    
    # Video yuborish (protected)
    await message.answer_video(
        video=movie['file_id'],
        caption=caption,
        reply_markup=user_kb.movie_found_kb(movie['id'], config.PUBLIC_CHANNEL_USERNAME),
        protect_content=True,  # Screenshot/forward oldini olish
        parse_mode='HTML'
    )

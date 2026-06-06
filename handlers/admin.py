from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
import asyncio

import config
from database.database import db
from keyboards import admin_kb, user_kb
from utils.states import AddMovie, EditMovie, DeleteMovie, Broadcast, ManageChannels

router = Router()


def is_admin(user_id: int) -> bool:
    """Admin ekanligini tekshirish"""
    return user_id == config.ADMIN_ID


@router.message(Command("admin"))
async def admin_panel(message: Message):
    """Admin panel"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    await message.answer(
        config.TEXTS['admin_panel'],
        reply_markup=admin_kb.admin_main_kb(),
        parse_mode='HTML'
    )


@router.message(F.text == "🔙 Orqaga")
async def back_to_user_menu(message: Message, state: FSMContext):
    """Foydalanuvchi menyusiga qaytish"""
    if not is_admin(message.from_user.id):
        return
    
    await state.clear()
    await message.answer(
        config.TEXTS['start_success'],
        reply_markup=user_kb.main_menu_kb(),
        parse_mode='HTML'
    )


# ==================== KINO QO'SHISH ====================

@router.message(F.text == "➕ Kino qo'shish")
async def add_movie_start(message: Message, state: FSMContext):
    """Kino qo'shish boshlash"""
    if not is_admin(message.from_user.id):
        return
    
    await state.set_state(AddMovie.title)
    await message.answer(
        "📝 <b>Kino qo'shish</b>\n\nKino nomini yuboring:",
        reply_markup=admin_kb.cancel_kb(),
        parse_mode='HTML'
    )


@router.message(AddMovie.title, F.text)
async def add_movie_title(message: Message, state: FSMContext):
    """Kino nomini qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=admin_kb.admin_main_kb())
        return
    
    await state.update_data(title=message.text)
    await state.set_state(AddMovie.file)
    await message.answer(
        "🎬 <b>Video faylni yuboring</b>\n\n"
        "Video formatida kino faylini yuklang:",
        reply_markup=admin_kb.cancel_kb(),
        parse_mode='HTML'
    )


@router.message(AddMovie.file, F.video)
async def add_movie_file(message: Message, state: FSMContext):
    """Video faylni qabul qilish"""
    await state.update_data(
        file_id=message.video.file_id,
        file_unique_id=message.video.file_unique_id
    )
    await state.set_state(AddMovie.trailer)
    await message.answer(
        "🖼 <b>Trailer rasmini yuboring</b>\n\n"
        "Instagram yoki kanal uchun rasm yuklang.\n"
        "O'tkazib yuborish uchun - <b>/</b> yuboring",
        reply_markup=admin_kb.skip_kb(),
        parse_mode='HTML'
    )


@router.message(AddMovie.file)
async def add_movie_file_invalid(message: Message):
    """Noto'g'ri fayl formati"""
    await message.answer("❌ Iltimos, video fayl yuboring!")


@router.message(AddMovie.trailer, F.photo)
async def add_movie_trailer_photo(message: Message, state: FSMContext):
    """Trailer rasmini qabul qilish"""
    await state.update_data(trailer_photo=message.photo[-1].file_id)
    await add_movie_ask_link(message, state)


@router.message(AddMovie.trailer, F.text)
async def add_movie_trailer_skip(message: Message, state: FSMContext):
    """Trailer rasmini o'tkazib yuborish"""
    if message.text in ["⏭ O'tkazib yuborish", "/"]:
        await state.update_data(trailer_photo=None)
        await add_movie_ask_link(message, state)
    elif message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=admin_kb.admin_main_kb())
    else:
        await message.answer("❌ Iltimos, rasm yuboring yoki o'tkazib yuboring!")


async def add_movie_ask_link(message: Message, state: FSMContext):
    """Trailer link so'rash"""
    await state.set_state(AddMovie.confirm)
    await message.answer(
        "🔗 <b>Trailer linkini yuboring</b>\n\n"
        "Instagram yoki YouTube havolasini yuboring.\n"
        "O'tkazib yuborish uchun - <b>/</b> yuboring",
        reply_markup=admin_kb.skip_kb(),
        parse_mode='HTML'
    )


@router.message(AddMovie.confirm, F.text)
async def add_movie_confirm(message: Message, state: FSMContext, bot: Bot):
    """Kinoni tasdiqlash"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=admin_kb.admin_main_kb())
        return
    
    # Linkni saqlash
    trailer_link = None if message.text in ["⏭ O'tkazib yuborish", "/"] else message.text
    await state.update_data(trailer_link=trailer_link)
    
    # Ma'lumotlarni olish
    data = await state.get_data()
    
    # Tasdiqlash uchun ma'lumotlarni ko'rsatish
    text = f"""
📝 <b>Kino ma'lumotlari</b>

🎬 Nomi: <b>{data['title']}</b>
🖼 Trailer rasm: {"✅ Bor" if data.get('trailer_photo') else "❌ Yo'q"}
🔗 Trailer link: {"✅ Bor" if trailer_link else "❌ Yo'q"}

Kinoni qo'shishni tasdiqlaysizmi?
"""
    
    # Video preview
    await message.answer_video(
        video=data['file_id'],
        caption=text,
        reply_markup=admin_kb.confirm_kb(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == "confirm_yes", AddMovie.confirm)
async def add_movie_save(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Kinoni saqlash"""
    await callback.answer("💾 Saqlanmoqda...")
    
    data = await state.get_data()
    
    # Bazaga saqlash
    movie_id = await db.add_movie(
        title=data['title'],
        file_id=data['file_id'],
        file_unique_id=data['file_unique_id'],
        trailer_photo=data.get('trailer_photo'),
        trailer_link=data.get('trailer_link'),
        added_by=callback.from_user.id
    )
    
    # Public kanalga post qilish
    try:
        caption = f"📽 <b>{data['title']}</b>\n\nKinoni olish uchun: @Hyper_cinema_bot\n🔢 Kod: <code>{movie_id}</code>"
        
        if data.get('trailer_photo'):
            await bot.send_photo(
                chat_id=config.PUBLIC_CHANNEL_ID,
                photo=data['trailer_photo'],
                caption=caption,
                parse_mode='HTML'
            )
        else:
            await bot.send_message(
                chat_id=config.PUBLIC_CHANNEL_ID,
                text=caption,
                parse_mode='HTML'
            )
    except Exception as e:
        print(f"Kanalga post qilishda xatolik: {e}")
    
    await state.clear()
    await callback.message.edit_caption(
        caption=f"✅ <b>Kino muvaffaqiyatli qo'shildi!</b>\n\n🔢 Kino kodi: <code>{movie_id}</code>",
        parse_mode='HTML'
    )
    await callback.message.answer(
        "Admin panelga qaytish:",
        reply_markup=admin_kb.admin_main_kb()
    )


@router.callback_query(F.data == "confirm_no")
async def add_movie_cancel(callback: CallbackQuery, state: FSMContext):
    """Kinoni qo'shishni bekor qilish"""
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "❌ Bekor qilindi",
        reply_markup=admin_kb.admin_main_kb()
    )


# ==================== KINO O'CHIRISH ====================

@router.message(F.text == "🗑 Kino o'chirish")
async def delete_movie_start(message: Message, state: FSMContext):
    """Kino o'chirish boshlash"""
    if not is_admin(message.from_user.id):
        return
    
    movies = await db.get_all_movies()
    
    if not movies:
        await message.answer("❌ Bazada kinolar yo'q!")
        return
    
    await state.set_state(DeleteMovie.select)
    await message.answer(
        "🗑 <b>Kino o'chirish</b>\n\nO'chirish uchun kinoni tanlang:",
        reply_markup=admin_kb.movie_list_kb(movies[:20]),  # Faqat 20 ta
        parse_mode='HTML'
    )


@router.callback_query(F.data.startswith("movie_"), DeleteMovie.select)
async def delete_movie_confirm(callback: CallbackQuery, state: FSMContext):
    """Kinoni o'chirishni tasdiqlash"""
    movie_id = int(callback.data.split("_")[1])
    movie = await db.get_movie(movie_id)
    
    if not movie:
        await callback.answer("❌ Kino topilmadi!")
        return
    
    await state.update_data(movie_id=movie_id)
    
    await callback.message.edit_text(
        f"❗️ <b>{movie['title']}</b> kinoni o'chirishni tasdiqlaysizmi?\n\n"
        f"Bu amalni bekor qilib bo'lmaydi!",
        reply_markup=admin_kb.confirm_kb(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == "confirm_yes", DeleteMovie.select)
async def delete_movie_execute(callback: CallbackQuery, state: FSMContext):
    """Kinoni o'chirish"""
    data = await state.get_data()
    movie_id = data['movie_id']
    
    await db.delete_movie(movie_id)
    await state.clear()
    
    await callback.message.edit_text(
        "✅ Kino muvaffaqiyatli o'chirildi!",
        parse_mode='HTML'
    )
    await callback.message.answer(
        "Admin panelga qaytish:",
        reply_markup=admin_kb.admin_main_kb()
    )


# ==================== STATISTIKA ====================

@router.message(F.text == "📊 Statistika")
async def admin_statistics(message: Message):
    """Admin statistikasi"""
    if not is_admin(message.from_user.id):
        return
    
    users_count = await db.get_users_count()
    movies_count = await db.get_movies_count()
    total_views = await db.get_total_views()
    
    # Eng ko'p ko'rilgan kinolar
    movies = await db.get_all_movies()
    top_movies = sorted(movies, key=lambda x: x['views_count'], reverse=True)[:5]
    
    text = f"""
📊 <b>ADMIN STATISTIKASI</b>

👥 Jami foydalanuvchilar: <b>{users_count}</b>
🎬 Jami kinolar: <b>{movies_count}</b>
👁 Jami ko'rishlar: <b>{total_views}</b>

🏆 <b>Top 5 kinolar:</b>
"""
    
    for idx, movie in enumerate(top_movies, 1):
        text += f"{idx}. {movie['title']} - {movie['views_count']} ko'rish\n"
    
    await message.answer(text, parse_mode='HTML')


# ==================== BROADCAST ====================

@router.message(F.text == "📢 Xabar yuborish")
async def broadcast_start(message: Message, state: FSMContext):
    """Broadcast boshlash"""
    if not is_admin(message.from_user.id):
        return
    
    await state.set_state(Broadcast.message)
    await message.answer(
        config.TEXTS['broadcast_start'],
        reply_markup=admin_kb.cancel_kb(),
        parse_mode='HTML'
    )


@router.message(Broadcast.message)
async def broadcast_receive_message(message: Message, state: FSMContext):
    """Broadcast xabarini qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=admin_kb.admin_main_kb())
        return
    
    # Xabarni saqlash
    await state.update_data(message_data=message)
    await state.set_state(Broadcast.confirm)
    
    await message.answer(
        config.TEXTS['broadcast_confirm'],
        reply_markup=admin_kb.confirm_kb(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == "confirm_yes", Broadcast.confirm)
async def broadcast_execute(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Broadcast amalga oshirish"""
    await callback.answer("📤 Yuborilmoqda...")
    
    data = await state.get_data()
    broadcast_msg: Message = data['message_data']
    
    # Barcha userlarni olish
    users = await db.get_all_users()
    total = len(users)
    success = 0
    failed = 0
    
    progress_msg = await callback.message.edit_text(
        config.TEXTS['broadcast_progress'].format(sent=0, total=total)
    )
    
    for idx, user in enumerate(users, 1):
        try:
            # Xabar turini aniqlash va yuborish
            if broadcast_msg.text:
                await bot.send_message(user['telegram_id'], broadcast_msg.text)
            elif broadcast_msg.photo:
                await bot.send_photo(
                    user['telegram_id'],
                    broadcast_msg.photo[-1].file_id,
                    caption=broadcast_msg.caption
                )
            elif broadcast_msg.video:
                await bot.send_video(
                    user['telegram_id'],
                    broadcast_msg.video.file_id,
                    caption=broadcast_msg.caption
                )
            elif broadcast_msg.forward_date:
                await broadcast_msg.forward(user['telegram_id'])
            
            success += 1
        except Exception as e:
            print(f"User {user['telegram_id']} ga yuborishda xatolik: {e}")
            failed += 1
        
        # Har 10 ta userdan keyin progress yangilash
        if idx % 10 == 0:
            try:
                await progress_msg.edit_text(
                    config.TEXTS['broadcast_progress'].format(sent=idx, total=total)
                )
            except TelegramBadRequest:
                pass
        
        # Flood kutish
        await asyncio.sleep(0.05)
    
    await state.clear()
    await progress_msg.edit_text(
        config.TEXTS['broadcast_done'].format(
            total=total,
            success=success,
            failed=failed
        )
    )
    await callback.message.answer(
        "Admin panelga qaytish:",
        reply_markup=admin_kb.admin_main_kb()
    )


# ==================== KANALLAR BOSHQARUVI ====================

@router.message(F.text == "⚙️ Kanallar")
async def manage_channels(message: Message):
    """Kanallar boshqaruvi"""
    if not is_admin(message.from_user.id):
        return
    
    await message.answer(
        "⚙️ <b>Kanallar boshqaruvi</b>\n\nKerakli amalni tanlang:",
        reply_markup=admin_kb.channels_manage_kb(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == "list_channels")
async def list_channels(callback: CallbackQuery):
    """Kanallar ro'yxati"""
    channels = await db.get_active_channels()
    
    if not channels:
        await callback.answer("❌ Hech qanday kanal yo'q!")
        return
    
    await callback.message.edit_text(
        "📋 <b>Aktiv kanallar:</b>",
        reply_markup=admin_kb.channel_list_kb(channels),
        parse_mode='HTML'
    )


@router.callback_query(F.data == "manage_channels")
async def back_to_channels_menu(callback: CallbackQuery):
    """Kanallar menyusiga qaytish"""
    await callback.message.edit_text(
        "⚙️ <b>Kanallar boshqaruvi</b>\n\nKerakli amalni tanlang:",
        reply_markup=admin_kb.channels_manage_kb(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == "back_to_admin")
async def back_to_admin_panel(callback: CallbackQuery):
    """Admin panelga qaytish"""
    await callback.message.delete()
    await callback.message.answer(
        config.TEXTS['admin_panel'],
        reply_markup=admin_kb.admin_main_kb(),
        parse_mode='HTML'
    )

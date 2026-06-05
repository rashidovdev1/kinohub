from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def admin_main_kb():
    """Admin asosiy menyu"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Kino qo'shish"), KeyboardButton(text="🗑 Kino o'chirish")],
            [KeyboardButton(text="✏️ Kino tahrirlash"), KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="📢 Xabar yuborish"), KeyboardButton(text="⚙️ Kanallar")],
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True
    )
    return keyboard


def cancel_kb():
    """Bekor qilish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard


def skip_kb():
    """O'tkazib yuborish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏭ O'tkazib yuborish")],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard


def confirm_kb():
    """Tasdiqlash klaviaturasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="confirm_no")
        ]
    ])
    return keyboard


def movie_list_kb(movies: list):
    """Kinolar ro'yxati"""
    buttons = []
    for movie in movies:
        buttons.append([InlineKeyboardButton(
            text=f"{movie['id']}. {movie['title'][:40]}",
            callback_data=f"movie_{movie['id']}"
        )])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def edit_movie_kb():
    """Kino tahrirlash bo'limlari"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Nomini o'zgartirish", callback_data="edit_title")],
        [InlineKeyboardButton(text="🎬 Faylni o'zgartirish", callback_data="edit_file")],
        [InlineKeyboardButton(text="🖼 Trailer rasmini o'zgartirish", callback_data="edit_photo")],
        [InlineKeyboardButton(text="🔗 Trailer linkini o'zgartirish", callback_data="edit_link")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_admin")]
    ])
    return keyboard


def channels_manage_kb():
    """Kanallar boshqaruvi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel")],
        [InlineKeyboardButton(text="📋 Kanallar ro'yxati", callback_data="list_channels")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_admin")]
    ])
    return keyboard


def channel_list_kb(channels: list):
    """Kanallar ro'yxati"""
    buttons = []
    for channel in channels:
        text = f"🔒 {channel['channel_username'] or 'Private'}" if not channel['channel_username'] else f"📢 {channel['channel_username']}"
        buttons.append([
            InlineKeyboardButton(text=text, callback_data=f"ch_info_{channel['id']}"),
            InlineKeyboardButton(text="🗑", callback_data=f"ch_delete_{channel['id']}")
        ])
    
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="manage_channels")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

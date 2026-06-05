from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb():
    """Asosiy menyu"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Qidirish")],
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="💬 Bog'lanish")]
        ],
        resize_keyboard=True
    )
    return keyboard


def subscription_kb(channels: list):
    """Majburiy obuna klaviaturasi"""
    buttons = []

    for idx, channel in enumerate(channels, 1):
        if channel.get('username'):
            # Public kanal
            buttons.append([InlineKeyboardButton(
                text=f"📢 {idx}-kanal",
                url=f"https://t.me/{channel['username'].replace('@', '')}"
            )])
        elif channel.get('invite_link'):
            # Private kanal - invite link bilan
            buttons.append([InlineKeyboardButton(
                text=f"🔒 {idx}-kanal (Private)",
                url=channel['invite_link']
            )])
        else:
            # Fallback - agar link bo'lmasa
            buttons.append([InlineKeyboardButton(
                text=f"🔒 {idx}-kanal",
                callback_data=f"no_link_{idx}"
            )])

    buttons.append([InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_subscription")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def movie_found_kb(movie_id: int, public_channel: str):
    """Kino topilganda ko'rsatiladigan klaviatura"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Bizning kanal", url=f"https://t.me/{public_channel.replace('@', '')}")]
    ])
    return keyboard


def contact_kb():
    """Bog'lanish klaviaturasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Admin", url="https://t.me/revangeuser")],
        [InlineKeyboardButton(text="📢 Kanalimiz", url="https://t.me/uzpornone")]
    ])
    return keyboard

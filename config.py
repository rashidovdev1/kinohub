import os
from dotenv import load_dotenv

load_dotenv()

# Bot sozlamalari
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

# Database sozlamalari
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'kinohub'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD')
}

# Kanallar
PUBLIC_CHANNEL_ID = int(os.getenv('PUBLIC_CHANNEL_ID'))
PUBLIC_CHANNEL_USERNAME = os.getenv('PUBLIC_CHANNEL_USERNAME')
PRIVATE_CHANNEL_ID = int(os.getenv('PRIVATE_CHANNEL_ID'))
PRIVATE_CHANNEL_INVITE = os.getenv('PRIVATE_CHANNEL_INVITE')

# Majburiy obuna kanallari
REQUIRED_CHANNELS = [
    {'id': PUBLIC_CHANNEL_ID, 'username': PUBLIC_CHANNEL_USERNAME, 'invite_link': None},
    {'id': PRIVATE_CHANNEL_ID, 'username': None, 'invite_link': PRIVATE_CHANNEL_INVITE}
]

# Matnlar
TEXTS = {
    'start': """
🎬 <b>Kino Bot ga xush kelibsiz!</b>

Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:
""",
    'start_success': """
✅ <b>Xush kelibsiz!</b>

🎬 Kino qidirish uchun:
• Kino nomini yozing (masalan: Avatar)
• Yoki kino kodini yozing (masalan: 123)

📊 Statistikani ko'rish uchun tugmani bosing
💬 Reklama uchun bizga murojaat qiling
""",
    'not_subscribed': """
❌ <b>Obuna bo'lmagan ekansiz!</b>

Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:
""",
    'checking_subscription': "⏳ Obuna tekshirilmoqda...",
    'subscription_confirmed': "✅ Obuna tasdiqlandi!",
    'movie_not_found': "❌ Kino topilmadi. Qaytadan urinib ko'ring.",
    'admin_panel': "👨‍💼 <b>Admin Panel</b>\n\nKerakli bo'limni tanlang:",
    'broadcast_start': "📢 Xabarni yuboring (matn, rasm, video yoki forward):",
    'broadcast_confirm': "Xabarni barcha foydalanuvchilarga yuborish tasdiqlansinmi?",
    'broadcast_progress': "📤 Yuborilmoqda: {sent}/{total}",
    'broadcast_done': "✅ Xabar yuborildi!\n\n👥 Jami: {total}\n✅ Muvaffaqiyatli: {success}\n❌ Xatolik: {failed}",
}

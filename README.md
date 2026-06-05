# 🎬 CINEMA BOT 1.0

Telegram kino bot - Aiogram 3 va PostgreSQL asosida

## 📋 Talablar

- Python 3.11+
- PostgreSQL 12+
- Git

## 🚀 O'rnatish

### 1. Loyihani klonlash

Ushbu barcha fayllarni `cinema_bot` papkasiga joylashtiring.

### 2. Virtual environment yaratish

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL sozlash

PostgreSQL ga kiring va database yarating:

```sql
-- psql ga kirish
psql -U postgres

-- Database yaratish
CREATE DATABASE kinohub;

-- Chiqish
\q
```

### 5. .env faylni sozlash

`.env` faylda o'z ma'lumotlaringizni tekshiring:

```env
BOT_TOKEN=8****************************k
ADMIN_ID=7********9

DB_HOST=localhost
DB_PORT=5432
DB_NAME=k******b
DB_USER=postgres
DB_PASSWORD=A*******1

PUBLIC_CHANNEL_ID=-1**********7
PUBLIC_CHANNEL_USERNAME=@u******e
PRIVATE_CHANNEL_ID=-1***********5
```

### 6. Botni ishga tushirish

```bash
python bot.py
```

## 📱 Foydalanish

### Foydalanuvchi komandlari:
- `/start` - Botni boshlash
- `🔍 Qidirish` - Kino qidirish
- `📊 Statistika` - Statistikani ko'rish
- `💬 Bog'lanish` - Admin bilan bog'lanish

### Admin komandlari:
- `/admin` - Admin panelni ochish
- `➕ Kino qo'shish` - Yangi kino qo'shish
- `🗑 Kino o'chirish` - Kinoni o'chirish
- `✏️ Kino tahrirlash` - Kinoni tahrirlash
- `📢 Xabar yuborish` - Barcha userlarga xabar
- `⚙️ Kanallar` - Kanallarni boshqarish
- `📊 Statistika` - To'liq statistika

## 🔧 PyCharm sozlamalari

### 1. Loyihani ochish
- PyCharm → Open → `cinema_bot` papkasini tanlash

### 2. Interpreterni sozlash
- File → Settings → Project → Python Interpreter
- Add Interpreter → Add Local Interpreter
- Virtualenv Environment → Existing
- `cinema_bot/venv` papkasini tanlash

### 3. Run Configuration
- Run → Edit Configurations → Add New → Python
- Name: Cinema Bot
- Script path: `bot.py`
- Working directory: `cinema_bot`

### 4. Ishga tushirish
- Run → Run 'Cinema Bot' yoki Shift+F10

## 📁 Fayl strukturasi

```
cinema_bot/
├── .env                    # Maxfiy sozlamalar
├── bot.py                  # Asosiy bot fayl
├── config.py               # Konfiguratsiya
├── requirements.txt        # Python paketlar
├── database/
│   ├── __init__.py
│   ├── models.py          # Database modellar
│   └── database.py        # Database funksiyalari
├── handlers/
│   ├── __init__.py
│   ├── user.py           # User handlerlari
│   ├── admin.py          # Admin handlerlari
│   └── subscription.py   # Obuna tekshiruvi
├── keyboards/
│   ├── __init__.py
│   ├── user_kb.py       # User klaviaturalar
│   └── admin_kb.py      # Admin klaviaturalar
└── utils/
    ├── __init__.py
    └── states.py        # FSM states
```

## ✨ Xususiyatlar

- ✅ Majburiy obuna (public + private kanallar)
- ✅ Avtomatik zapros qabul qilish (private kanal)
- ✅ Kino qidirish (ID va nom bo'yicha)
- ✅ File protection (screenshot/forward yo'q)
- ✅ Admin panel (CRUD)
- ✅ Broadcast (matn, rasm, video, forward)
- ✅ Statistika
- ✅ Public kanalga avtomatik post

## 🐛 Muammolar hal qilish

### Database ulanish xatosi
```bash
# PostgreSQL ishlab turganligini tekshiring
# Windows
pg_ctl status

# .env fayldagi ma'lumotlar to'g'riligini tekshiring
```

### Bot ishga tushmayapti
```bash
# Token to'g'riligini tekshiring
# Internet ulanishini tekshiring
# Loglarni o'qing
```

### asyncpg o'rnatish xatosi (Windows)
```bash
# Visual C++ Build Tools o'rnating
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

## 📞 Yordam

Muammolar yuzaga kelsa:
- GitHub Issues
- Telegram: @revangeuser

## 📝 License

MIT License

---

**Yaratuvchi:** @revangeuser
**Versiya:** 1.0
**Sana:** 2025

# 🎯 PyCharm da CINEMA BOT ni ishga tushirish

## 📌 QADAMMA-QADAM YO'RIQNOMA

### ✅ BOSHLASH OLDIN TAYYOR BO'LISHI KERAK:
1. ✅ Python 3.11.6 o'rnatilgan
2. ✅ PostgreSQL ishlab turibdi
3. ✅ Bot token va kanallar tayyor
4. ✅ PyCharm o'rnatilgan

---

## 🔴 QADAM 1: LOYIHANI OCHISH

1. **PyCharm ni oching**

2. **Loyihani import qiling:**
   - `File` → `Open`
   - `cinema_bot` papkasini tanlang
   - `OK` ni bosing

---

## 🟠 QADAM 2: VIRTUAL ENVIRONMENT YARATISH

### Windows uchun:

1. **PyCharm terminalini oching** (pastki qism, `Terminal` tab)

2. **Virtual environment yaratish:**
```cmd
python -m venv venv
```

3. **Aktivlashtirish:**
```cmd
venv\Scripts\activate
```

Terminal `(venv)` bilan boshlanishi kerak:
```
(venv) C:\Users\user\cinema_bot>
```

### Agar terminal `(venv)` ko'rsatmasa:

**PowerShell uchun:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**Yoki CMD ishlatilsa:**
```cmd
venv\Scripts\activate.bat
```

---

## 🟡 QADAM 3: PAKETLARNI O'RNATISH

Virtual environment aktiv bo'lganidan keyin:

```cmd
pip install -r requirements.txt
```

**Kutilayotgan natija:**
```
Successfully installed aiogram-3.15.0 asyncpg-0.29.0 python-dotenv-1.0.0
```

### ❗ Agar `asyncpg` xatosi chiqsa (Windows):

```cmd
pip install wheel
pip install asyncpg --no-binary :all:
```

Yoki:
```cmd
pip install asyncpg==0.29.0
```

---

## 🟢 QADAM 4: DATABASE SOZLASH

### 1. PostgreSQL ga kirish:

```cmd
psql -U postgres
```

Password kiritilsa: `Ac0451241` (sizning parolingiz)

### 2. Database yaratish:

```sql
CREATE DATABASE kinohub;
```

### 3. Chiqish:

```sql
\q
```

### 4. Database ni tekshirish:

```cmd
python test_db.py
```

**Muvaffaqiyatli natija:**
```
✅ Database ga ulanish muvaffaqiyatli!

📊 Mavjud jadvallar (4 ta):
  - users
  - movies
  - channels
  - statistics

👥 Users: 0 ta
🎬 Movies: 0 ta

✅ Test muvaffaqiyatli yakunlandi!
```

---

## 🔵 QADAM 5: .env FAYLNI TEKSHIRISH

`.env` faylni oching va ma'lumotlarni tekshiring:

```env
BOT_TOKEN=8470618802:AAGK1g0j4j4PI3KO3DVjR9nk6LEIbK6eZ5k
ADMIN_ID=7975671119

DB_HOST=localhost
DB_PORT=5432
DB_NAME=kinohub
DB_USER=postgres
DB_PASSWORD=Ac0451241

PUBLIC_CHANNEL_ID=-1003770277367
PUBLIC_CHANNEL_USERNAME=@uzpornone
PRIVATE_CHANNEL_ID=-1003879758485
```

**MUHIM:** Barcha qiymatlar to'g'ri ekanligiga ishonch hosil qiling!

---

## 🟣 QADAM 6: PYTHON INTERPRETERNI SOZLASH

### Avtomatik (tavsiya etiladi):

PyCharm avtomatik `venv` ni aniqlashi kerak. Agar pastki o'ng burchakda `Python 3.11 (cinema_bot)` ko'rsatilsa, hammasi tayyor.

### Qo'lda sozlash:

1. `File` → `Settings` (yoki `Ctrl+Alt+S`)

2. `Project: cinema_bot` → `Python Interpreter`

3. **Settings icon** (⚙️) → `Add...`

4. `Virtualenv Environment` tanlang

5. `Existing environment` ni belgilang

6. **Interpreter:** `cinema_bot\venv\Scripts\python.exe` tanlang

7. `OK` → `OK`

---

## 🔴 QADAM 7: RUN CONFIGURATION YARATISH

### 1. Konfiguratsiyani qo'shish:

- `Run` → `Edit Configurations...`
- `+` (Add) → `Python`

### 2. Sozlamalar:

```
Name: Cinema Bot
Script path: C:\Users\user\cinema_bot\bot.py  (to'liq yo'l)
Python interpreter: Python 3.11 (cinema_bot)
Working directory: C:\Users\user\cinema_bot
```

### 3. Saqlash:

- `Apply` → `OK`

---

## ⚡ QADAM 8: BOTNI ISHGA TUSHIRISH

### Usul 1: Run tugmasi

1. Yuqori o'ng burchakda `Cinema Bot` tanlanganligini tekshiring
2. ▶️ **Run** tugmasini bosing (yoki `Shift+F10`)

### Usul 2: Terminal

```cmd
python bot.py
```

### ✅ Muvaffaqiyatli ishga tushish:

```
2025-02-13 15:30:45,123 - __main__ - INFO - 🚀 Bot ishga tushmoqda...
2025-02-13 15:30:45,456 - __main__ - INFO - ✅ Database ga ulanish muvaffaqiyatli!
2025-02-13 15:30:46,789 - __main__ - INFO - ✅ Bot ishga tushdi: @echouz_robot
```

Telegramda admin (siz)ga xabar keladi:
```
🤖 Bot muvaffaqiyatli ishga tushdi!
```

---

## 🧪 QADAM 9: TESTLASH

### 1. Telegram da botni toping:

- `@echouz_robot` ni qidiring
- `/start` ni bosing

### 2. Majburiy obuna:

Bot sizdan kanallarga obuna bo'lishni so'raydi.

### 3. Admin panel:

- `/admin` buyrug'ini yuboring
- Admin menyu ochilishi kerak

### 4. Kino qo'shish:

- `➕ Kino qo'shish` tugmasini bosing
- Ketma-ketlikni bajaring

---

## ❌ MUAMMOLARNI HAL QILISH

### ❗ "ModuleNotFoundError: No module named 'aiogram'"

**Yechim:**
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

### ❗ "Database connection error"

**Yechim:**
1. PostgreSQL ishlab turganini tekshiring:
```cmd
pg_ctl status
```

2. `.env` fayldagi ma'lumotlar to'g'riligini tekshiring

3. Database mavjudligini tekshiring:
```cmd
psql -U postgres -c "\l"
```

### ❗ "Unauthorized" (Bot xatosi)

**Yechim:**
- `.env` fayldagi `BOT_TOKEN` to'g'riligini tekshiring
- BotFather dan yangi token oling

### ❗ PyCharm "venv" ni tanimaydi

**Yechim:**
1. `File` → `Invalidate Caches` → `Invalidate and Restart`
2. Interpreterni qo'lda sozlang (Qadam 6)

### ❗ "Access denied" (PostgreSQL)

**Yechim:**
```cmd
# Windows Services da PostgreSQL ni restart qiling
# Yoki
pg_ctl restart
```

---

## 🎯 KEYINGI QADAMLAR

### Botni test qilish:

1. ✅ Foydalanuvchi sifatida `/start`
2. ✅ Kino qidirish
3. ✅ Admin panel `/admin`
4. ✅ Kino qo'shish
5. ✅ Public kanalda post paydo bo'lishini tekshirish

### Qo'shimcha sozlamalar:

- **Kanallarni boshqarish:** `/admin` → `⚙️ Kanallar`
- **Statistika:** `📊 Statistika`
- **Broadcast test:** Bitta userga xabar yuboring

---

## 📞 YORDAM

Agar muammolar hal bo'lmasa:

1. **Loglarni o'qing** (PyCharm konsolda)
2. **Terminal da xatoni ko'ring**
3. **test_db.py** ni ishga tushiring

**Qo'shimcha yordam kerak bo'lsa:**
- GitHub Issues
- Telegram: @revangeuser

---

## ✨ TAYYOR!

Endi botingiz ishlashi kerak! 🎉

**Esda tuting:**
- Botni to'xtatish: `Ctrl+C` (Terminal) yoki 🛑 (PyCharm)
- Qayta ishga tushirish: ▶️ `Run` tugmasi
- Loglarni kuzatish: PyCharm konsolda

**Omad tilaymiz!** 🚀

"""
Database test script
Database ulanishini va jadvallarni tekshirish uchun
"""
import asyncio
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

async def test_database():
    """Database ulanishini tekshirish"""
    try:
        # Database ga ulanish
        conn = await asyncpg.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        print("✅ Database ga ulanish muvaffaqiyatli!")
        
        # Jadvallar ro'yxatini olish
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        print(f"\n📊 Mavjud jadvallar ({len(tables)} ta):")
        for table in tables:
            print(f"  - {table['table_name']}")
        
        # Users soni
        users_count = await conn.fetchval("SELECT COUNT(*) FROM users")
        print(f"\n👥 Users: {users_count} ta")
        
        # Movies soni
        movies_count = await conn.fetchval("SELECT COUNT(*) FROM movies")
        print(f"🎬 Movies: {movies_count} ta")
        
        await conn.close()
        print("\n✅ Test muvaffaqiyatli yakunlandi!")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")

if __name__ == '__main__':
    asyncio.run(test_database())

import asyncpg
from typing import Optional, List, Dict
import config
from database.models import ALL_TABLES


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Database ga ulanish"""
        self.pool = await asyncpg.create_pool(**config.DB_CONFIG)
        await self.create_tables()
        print("✅ Database ga ulanish muvaffaqiyatli!")

    async def disconnect(self):
        """Database dan uzilish"""
        if self.pool:
            await self.pool.close()

    async def create_tables(self):
        """Jadvallarni yaratish"""
        async with self.pool.acquire() as conn:
            for table_query in ALL_TABLES:
                await conn.execute(table_query)

    # ==================== USERS ====================
    
    async def add_user(self, telegram_id: int, username: str = None, 
                      first_name: str = None, last_name: str = None):
        """Yangi user qo'shish"""
        query = """
        INSERT INTO users (telegram_id, username, first_name, last_name)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (telegram_id) DO UPDATE
        SET username = $2, first_name = $3, last_name = $4
        RETURNING id;
        """
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, telegram_id, username, first_name, last_name)

    async def get_user(self, telegram_id: int):
        """User ma'lumotlarini olish"""
        query = "SELECT * FROM users WHERE telegram_id = $1;"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, telegram_id)

    async def get_all_users(self, active_only: bool = True) -> List:
        """Barcha userlarni olish"""
        query = "SELECT * FROM users WHERE is_active = TRUE;" if active_only else "SELECT * FROM users;"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query)

    async def get_users_count(self) -> int:
        """Userlar sonini olish"""
        query = "SELECT COUNT(*) FROM users WHERE is_active = TRUE;"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query)

    async def block_user(self, telegram_id: int):
        """Userni bloklash"""
        query = "UPDATE users SET is_blocked = TRUE WHERE telegram_id = $1;"
        async with self.pool.acquire() as conn:
            await conn.execute(query, telegram_id)

    # ==================== MOVIES ====================
    
    async def add_movie(self, title: str, file_id: str, file_unique_id: str,
                       trailer_photo: str = None, trailer_link: str = None, 
                       added_by: int = None) -> int:
        """Yangi kino qo'shish"""
        query = """
        INSERT INTO movies (title, file_id, file_unique_id, trailer_photo, trailer_link, added_by)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id;
        """
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, title, file_id, file_unique_id, 
                                      trailer_photo, trailer_link, added_by)

    async def get_movie(self, movie_id: int):
        """Kinoni ID bo'yicha olish"""
        query = "SELECT * FROM movies WHERE id = $1;"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, movie_id)

    async def search_movie(self, query_text: str):
        """Kinoni qidirish (ID yoki nom bo'yicha)"""
        # Agar raqam bo'lsa, ID bo'yicha qidirish
        if query_text.isdigit():
            return await self.get_movie(int(query_text))
        
        # Aks holda nom bo'yicha qidirish
        query = """
        SELECT * FROM movies 
        WHERE LOWER(title) LIKE LOWER($1)
        LIMIT 10;
        """
        async with self.pool.acquire() as conn:
            results = await conn.fetch(query, f"%{query_text}%")
            return results[0] if results else None

    async def get_all_movies(self) -> List:
        """Barcha kinolarni olish"""
        query = "SELECT * FROM movies ORDER BY id DESC;"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query)

    async def update_movie_views(self, movie_id: int):
        """Kino ko'rilishini +1 qilish"""
        query = "UPDATE movies SET views_count = views_count + 1 WHERE id = $1;"
        async with self.pool.acquire() as conn:
            await conn.execute(query, movie_id)

    async def delete_movie(self, movie_id: int):
        """Kinoni o'chirish"""
        query = "DELETE FROM movies WHERE id = $1;"
        async with self.pool.acquire() as conn:
            await conn.execute(query, movie_id)

    async def update_movie(self, movie_id: int, field: str, value: str):
        """Kinoni tahrirlash"""
        query = f"UPDATE movies SET {field} = $1 WHERE id = $2;"
        async with self.pool.acquire() as conn:
            await conn.execute(query, value, movie_id)

    async def get_movies_count(self) -> int:
        """Kinolar sonini olish"""
        query = "SELECT COUNT(*) FROM movies;"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query)

    async def get_total_views(self) -> int:
        """Jami ko'rishlar soni"""
        query = "SELECT SUM(views_count) FROM movies;"
        async with self.pool.acquire() as conn:
            result = await conn.fetchval(query)
            return result if result else 0

    # ==================== CHANNELS ====================
    
    async def add_channel(self, channel_id: int, username: str = None, 
                         channel_type: str = 'required'):
        """Kanal qo'shish"""
        query = """
        INSERT INTO channels (channel_id, channel_username, channel_type)
        VALUES ($1, $2, $3)
        ON CONFLICT (channel_id) DO UPDATE
        SET channel_username = $2, is_active = TRUE;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, channel_id, username, channel_type)

    async def get_active_channels(self) -> List:
        """Aktiv kanallarni olish"""
        query = "SELECT * FROM channels WHERE is_active = TRUE;"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query)

    async def remove_channel(self, channel_id: int):
        """Kanalni o'chirish"""
        query = "UPDATE channels SET is_active = FALSE WHERE channel_id = $1;"
        async with self.pool.acquire() as conn:
            await conn.execute(query, channel_id)

    # ==================== STATISTICS ====================
    
    async def update_statistics(self):
        """Statistikani yangilash"""
        query = """
        INSERT INTO statistics (date, total_users, new_users)
        VALUES (CURRENT_DATE, 
                (SELECT COUNT(*) FROM users WHERE is_active = TRUE),
                (SELECT COUNT(*) FROM users WHERE DATE(joined_date) = CURRENT_DATE))
        ON CONFLICT (date) DO UPDATE
        SET total_users = EXCLUDED.total_users,
            new_users = EXCLUDED.new_users;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query)


# Global database instance
db = Database()

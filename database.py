import aiosqlite
import hashlib
import os

DB_NAME = "movies.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            login TEXT NOT NULL,
            password TEXT NOT NULL
            )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            price INTEGER,
            end_date TEXT NOT NULL,
            reminded_5_days INTEGER DEFAULT 0,
            reminded_1_day INTEGER DEFAULT 0,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

# ------------------------------------------------------------------------------------

async def add_user(telegram_id, login, password):
    password_hash = _hash_password(password)
    async with aiosqlite.connect(DB_NAME) as db:
        try:
            await db.execute("""
                INSERT INTO users (telegram_id, login, password)
                VALUES (?, ?, ?)
            """, (telegram_id, login, password_hash))
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def get_user_by_telegram_id(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
                    SELECT * FROM users WHERE telegram_id = ?
                """, (telegram_id,))
        result = await cursor.fetchone()
        return result


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    iterations = 100_000
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}"


# ------------------------------------------------------------------------------------

async def add_movie(user_id, title, type_, comment):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO movies (user_id, title, type, comment)
            VALUES (?, ?, ?, ?)
        """, (user_id, title, type_, comment))
        await db.commit()


async def get_movies(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""SELECT * FROM movies WHERE user_id = ?""", (user_id,))
        result = await cursor.fetchall()
        return result


async def delete_movie(user_id, movie_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""DELETE FROM movies WHERE id = ? AND user_id = ?""", (movie_id, user_id))
        await db.commit()

# ------------------------------------------------------------------------------------

async def add_note(user_id, title, due_date=None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO notes (user_id, title, due_date)
            VALUES (?, ?, ?)
        """, (user_id, title, due_date))
        await db.commit()


async def get_notes(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT * FROM notes WHERE user_id = ?
        """, (user_id,))
        return await cursor.fetchall()


async def delete_note(user_id, note_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            DELETE FROM notes WHERE id = ? AND user_id = ?
        """, (note_id, user_id))
        await db.commit()

# ------------------------------------------------------------------------------------

async def add_subscription(user_id, title, price, end_date, comment):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO subscriptions (user_id, title, price, end_date, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, title, price, end_date, comment))
        await db.commit()

async def get_subscriptions(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT * FROM subscriptions WHERE user_id = ? ORDER BY end_date ASC
            """, (user_id,))
        return await cursor.fetchall()


async def delete_subscription(user_id, subscription_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        DELETE FROM subscriptions WHERE id = ? AND user_id = ?
            """, (subscription_id, user_id))
        await db.commit()

#-------------------------------------------------------------------------------------

async def get_all_subscriptions():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT * FROM subscriptions
            """)
        return await cursor.fetchall()

async def mark_reminded_5(subscription_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        UPDATE subscriptions SET reminded_5_days = 1 WHERE id = ?
            """, (subscription_id,))
        await db.commit()

async def mark_reminded_1(subscription_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        UPDATE subscriptions SET reminded_1_day = 1 WHERE id = ?
            """, (subscription_id,))
        await db.commit()
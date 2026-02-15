import aiosqlite

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
        await db.commit()

# ------------------------------------------------------------------------------------

async def add_user(telegram_id, login, password):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, login, password)
            VALUES (?, ?, ?)
        """, (telegram_id, login, password))
        await db.commit()


async def get_user_by_telegram_id(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
                    SELECT * FROM users WHERE telegram_id = ?
                """, (telegram_id,))
        result = await cursor.fetchone()
        return result


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
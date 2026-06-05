"""
Database models va SQL queries
"""

# Users table
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_blocked BOOLEAN DEFAULT FALSE
);
"""

# Movies table
CREATE_MOVIES_TABLE = """
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    file_id VARCHAR(500) NOT NULL,
    file_unique_id VARCHAR(500),
    trailer_photo VARCHAR(500),
    trailer_link TEXT,
    views_count INTEGER DEFAULT 0,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    added_by BIGINT REFERENCES users(telegram_id)
);
"""

# Channels table
CREATE_CHANNELS_TABLE = """
CREATE TABLE IF NOT EXISTS channels (
    id SERIAL PRIMARY KEY,
    channel_id BIGINT UNIQUE NOT NULL,
    channel_username VARCHAR(255),
    channel_type VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Statistics table
CREATE_STATISTICS_TABLE = """
CREATE TABLE IF NOT EXISTS statistics (
    id SERIAL PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE,
    new_users INTEGER DEFAULT 0,
    total_users INTEGER DEFAULT 0,
    movies_watched INTEGER DEFAULT 0,
    UNIQUE(date)
);
"""

ALL_TABLES = [
    CREATE_USERS_TABLE,
    CREATE_MOVIES_TABLE,
    CREATE_CHANNELS_TABLE,
    CREATE_STATISTICS_TABLE
]

-- 0001_init.sql

CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    created_at  INTEGER NOT NULL DEFAULT (unixepoch())
);

CREATE TABLE IF NOT EXISTS gifs(
    id        INTEGER PRIMARY KEY,
    url       TEXT NOT NULL,
    tier      TEXT NOT NULL,
    added_by  INTEGER,
    series    TEXT,
    active    INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_gifs_tier ON gifs(tier);

CREATE TABLE IF NOT EXISTS user_gacha(
    user_id          INTEGER PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    roll_count       INTEGER NOT NULL DEFAULT 10,
    roll_streak      INTEGER NOT NULL DEFAULT 0,
    last_daily_date  TEXT,
    a_pity           INTEGER NOT NULL DEFAULT 0,
    s_pity           INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_gifs(
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    gif_id       INTEGER NOT NULL REFERENCES gifs(id),
    obtained_at  INTEGER NOT NULL DEFAULT (unixepoch())
);

CREATE INDEX IF NOT EXISTS idx_user_gifs_user ON user_gifs(user_id, gif_id);


CREATE TABLE IF NOT EXISTS user_favorites(
    user_id       INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    gif_id        INTEGER NOT NULL REFERENCES gifs(id) ON DELETE CASCADE,
    favorited_at  INTEGER NOT NULL DEFAULT (unixepoch()),
    PRIMARY KEY (user_id, gif_id)
);

CREATE TABLE IF NOT EXISTS daily_gifs(
    date         TEXT PRIMARY KEY, -- Eastern date, one row per day
    gif_id       INTEGER NOT NULL REFERENCES gifs(id),
    triggered_by  INTEGER NOT NULL REFERENCES users(user_id),
    created_at   INTEGER NOT NULL DEFAULT (unixepoch())
);

CREATE TABLE IF NOT EXISTS pulls(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(user_id),
    gif_id     INTEGER NOT NULL REFERENCES gifs(id),
    pulled_at  INTEGER NOT NULL DEFAULT (unixepoch()),
    a_pity     INTEGER,
    s_pity     INTEGER
);

CREATE TABLE IF NOT EXISTS birthdays(
    user_id    INTEGER PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    month      INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    day        INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    year       INTEGER
);

CREATE TRIGGER IF NOT EXISTS trg_users_create_gacha
AFTER INSERT ON users
BEGIN
    INSERT INTO user_gacha (user_id, roll_count) VALUES (NEW.user_id, 10);
END;


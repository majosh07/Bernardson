-- 0003_add_bot_state.sql

CREATE TABLE IF NOT EXISTS bot_state(
    key     TEXT PRIMARY KEY,
    value   TEXT NOT NULL
);


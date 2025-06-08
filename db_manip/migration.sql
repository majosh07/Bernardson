BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

INSERT INTO alembic_version (version_num) VALUES ('317c58e5e9a0') RETURNING alembic_version.version_num;

-- Running upgrade 317c58e5e9a0 -> e3ba9114f4b3

UPDATE alembic_version SET version_num='e3ba9114f4b3' WHERE alembic_version.version_num = '317c58e5e9a0';

-- Running upgrade e3ba9114f4b3 -> 1ca75b4abcd3

CREATE TABLE user_favorites (
    user_id BIGINT NOT NULL, 
    gif_id INTEGER NOT NULL, 
    id SERIAL NOT NULL, 
    favorited_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
    CONSTRAINT user_favorites_pkey PRIMARY KEY (id), 
    CONSTRAINT fk_gif FOREIGN KEY(gif_id) REFERENCES gifs (id) ON DELETE CASCADE, 
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE, 
    CONSTRAINT unique_user_gif_fav UNIQUE (user_id, gif_id)
);

UPDATE alembic_version SET version_num='1ca75b4abcd3' WHERE alembic_version.version_num = 'e3ba9114f4b3';

COMMIT;


CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    vk_id BIGINT NOT NULL UNIQUE,
    age INTEGER,
    gender INTEGER,
    city VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    favorite_vk_id BIGINT NOT NULL,
    UNIQUE (user_id, favorite_vk_id)
);

CREATE TABLE IF NOT EXISTS viewed (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    candidate_vk_id BIGINT NOT NULL,
    UNIQUE (user_id, candidate_vk_id)
);
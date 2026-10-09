import psycopg2


DB_CONFIG = {
    "dbname": "vkinder",
    "user": "postgres",
    "password": "Z041109a!",
    "host": "localhost",
    "port": "5432"
}


def get_connection():
    """Подключение к базе данных."""
    return psycopg2.connect(**DB_CONFIG)


def add_user(vk_id, age, gender, city):
    """Добавляет пользователя или обновляет его данные."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (vk_id, age, gender, city)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (vk_id)
        DO UPDATE SET
            age = EXCLUDED.age,
            gender = EXCLUDED.gender,
            city = EXCLUDED.city
        RETURNING id;
    """, (vk_id, age, gender, city))

    user_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return user_id


def get_user(vk_id):
    """Получает пользователя по VK ID."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, vk_id, age, gender, city
        FROM users
        WHERE vk_id = %s;
    """, (vk_id,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user


def add_favorite(user_vk_id, favorite_vk_id):
    """Добавляет пользователя в избранное."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM users
        WHERE vk_id = %s;
    """, (user_vk_id,))

    user = cursor.fetchone()

    if user is None:
        cursor.close()
        connection.close()
        return False

    cursor.execute("""
        INSERT INTO favorites (user_id, favorite_vk_id)
        VALUES (%s, %s)
        ON CONFLICT (user_id, favorite_vk_id)
        DO NOTHING;
    """, (user[0], favorite_vk_id))

    connection.commit()

    cursor.close()
    connection.close()

    return True


def get_favorites(user_vk_id):
    """Получает список избранных пользователей."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT f.favorite_vk_id
        FROM favorites f
        JOIN users u ON u.id = f.user_id
        WHERE u.vk_id = %s
        ORDER BY f.id;
    """, (user_vk_id,))

    favorites = cursor.fetchall()

    cursor.close()
    connection.close()

    return [favorite[0] for favorite in favorites]


def add_viewed(user_vk_id, candidate_vk_id):
    """Записывает показанного кандидата."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM users
        WHERE vk_id = %s;
    """, (user_vk_id,))

    user = cursor.fetchone()

    if user is None:
        cursor.close()
        connection.close()
        return False

    cursor.execute("""
        INSERT INTO viewed (user_id, candidate_vk_id)
        VALUES (%s, %s)
        ON CONFLICT (user_id, candidate_vk_id)
        DO NOTHING;
    """, (user[0], candidate_vk_id))

    connection.commit()

    cursor.close()
    connection.close()

    return True


def get_viewed(user_vk_id):
    """Получает список уже показанных кандидатов."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT v.candidate_vk_id
        FROM viewed v
        JOIN users u ON u.id = v.user_id
        WHERE u.vk_id = %s;
    """)

    viewed = cursor.fetchall()

    cursor.close()
    connection.close()

    return [candidate[0] for candidate in viewed]
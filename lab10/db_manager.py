import psycopg2
from psycopg2 import sql
import json

class GameDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="snake_game",
            user="bekshh",
            password="wldr007"
        )
        self.cur = self.conn.cursor()
        self._initialize_tables()
        self._initialize_levels()

    def _initialize_tables(self):
        """Создание таблиц, если они не существуют"""
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS user_scores (
                score_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                level INTEGER NOT NULL,
                score INTEGER NOT NULL,
                saved_state JSONB,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS game_levels (
                level_id SERIAL PRIMARY KEY,
                level_name VARCHAR(50) NOT NULL,
                speed INTEGER NOT NULL,
                walls_config JSONB NOT NULL,
                required_score INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def _initialize_levels(self):
        """Инициализация уровней игры"""
        levels = [
            {
                "level_name": "Beginner",
                "speed": 10,
                "walls_config": {"walls": []},
                "required_score": 0
            },
            {
                "level_name": "Intermediate",
                "speed": 15,
                "walls_config": {"walls": [[100, 100, 200, 20]]},
                "required_score": 100
            },
            {
                "level_name": "Advanced",
                "speed": 20,
                "walls_config": {"walls": [[100, 100, 200, 20], [300, 300, 200, 20]]},
                "required_score": 250
            }
        ]
        
        for level in levels:
            self.cur.execute("""
                INSERT INTO game_levels (level_name, speed, walls_config, required_score)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                level["level_name"],
                level["speed"],
                json.dumps(level["walls_config"]),
                level["required_score"]
            ))
        self.conn.commit()

    def get_or_create_user(self, username):
        """Получение или создание пользователя"""
        self.cur.execute("""
            INSERT INTO users (username) VALUES (%s)
            ON CONFLICT (username) DO UPDATE SET username = EXCLUDED.username
            RETURNING user_id
        """, (username,))
        user_id = self.cur.fetchone()[0]
        self.conn.commit()
        return user_id

    def get_user_level(self, user_id):
        """Получение текущего уровня пользователя"""
        self.cur.execute("""
            SELECT MAX(level) FROM user_scores WHERE user_id = %s
        """, (user_id,))
        result = self.cur.fetchone()
        return result[0] if result[0] is not None else 1

    def get_level_config(self, level):
        """Получение конфигурации уровня"""
        self.cur.execute("""
            SELECT speed, walls_config FROM game_levels WHERE level_id = %s
        """, (level,))
        return self.cur.fetchone()

    def save_game_state(self, user_id, level, score, game_state):
        """Сохранение состояния игры"""
        self.cur.execute("""
            INSERT INTO user_scores (user_id, level, score, saved_state)
            VALUES (%s, %s, %s, %s)
        """, (user_id, level, score, json.dumps(game_state)))
        self.conn.commit()

    def close(self):
        """Закрытие соединения"""
        self.cur.close()
        self.conn.close()
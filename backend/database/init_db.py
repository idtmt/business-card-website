from backend.database.connection import get_connection


class DatabaseInitializer:
    @staticmethod
    async def initialize() -> None:
        async with get_connection() as connection:
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS company (
                    id INTEGER PRIMARY KEY CHECK(id = 1),
                    name TEXT NOT NULL,
                    description TEXT
                )
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    position INTEGER NOT NULL DEFAULT 0,
                    is_hidden INTEGER NOT NULL DEFAULT 0
                        CHECK(is_hidden IN (0, 1))
                )
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    price TEXT NOT NULL,
                    position INTEGER NOT NULL DEFAULT 0,
                    is_hidden INTEGER NOT NULL DEFAULT 0
                        CHECK(is_hidden IN (0, 1)),
                    FOREIGN KEY (service_id)
                        REFERENCES services(id)
                        ON DELETE CASCADE
                )
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS faq (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    position INTEGER NOT NULL DEFAULT 0,
                    is_hidden INTEGER NOT NULL DEFAULT 0
                        CHECK(is_hidden IN (0, 1))
                )
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    value TEXT NOT NULL,
                    url TEXT,
                    icon TEXT,
                    position INTEGER NOT NULL DEFAULT 0,
                    is_hidden INTEGER NOT NULL DEFAULT 0
                        CHECK(is_hidden IN (0, 1))
                )
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    address TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    position INTEGER NOT NULL DEFAULT 0,
                    is_hidden INTEGER NOT NULL DEFAULT 0
                        CHECK(is_hidden IN (0, 1))
                )
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location_id INTEGER NOT NULL,
                    weekday INTEGER NOT NULL
                        CHECK(weekday BETWEEN 0 AND 6),
                    start_time TEXT,
                    end_time TEXT,
                    is_day_off INTEGER NOT NULL DEFAULT 0
                        CHECK(is_day_off IN (0, 1)),
                    CHECK (
                        (is_day_off = 1
                            AND start_time IS NULL
                            AND end_time IS NULL)
                        OR
                        (is_day_off = 0
                            AND start_time IS NOT NULL
                            AND end_time IS NOT NULL)
                    ),
                    FOREIGN KEY (location_id)
                        REFERENCES locations(id)
                        ON DELETE CASCADE,
                    UNIQUE(location_id, weekday)
                )
            """)

            await connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_services_visible_position
                ON services(is_hidden, position)
            """)

            await connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_prices_service_visible_position
                ON prices(service_id, is_hidden, position)
            """)

            await connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_faq_visible_position
                ON faq(is_hidden, position)
            """)

            await connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_contacts_visible_position
                ON contacts(is_hidden, position)
            """)

            await connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_locations_visible_position
                ON locations(is_hidden, position)
            """)

            await connection.commit()
from typing import Any

from backend.database.connection import get_connection


class CompanyRepository:
    async def get(self) -> dict[str, Any] | None:
        async with get_connection() as connection:
            cursor = await connection.execute("""
                SELECT
                    id,
                    name,
                    description
                FROM company
                WHERE id = 1
            """)

            row = await cursor.fetchone()

            if row is None:
                return None

            return dict(row)

    async def create(
        self,
        name: str,
        description: str | None = None,
    ) -> None:
        async with get_connection() as connection:
            await connection.execute("""
                INSERT INTO company (
                    id,
                    name,
                    description
                )
                VALUES (1, ?, ?)
            """, (name, description))

            await connection.commit()

    async def update(
        self,
        name: str,
        description: str | None = None,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute("""
                UPDATE company
                SET
                    name = ?,
                    description = ?
                WHERE id = 1
            """, (name, description))

            await connection.commit()

            return cursor.rowcount > 0
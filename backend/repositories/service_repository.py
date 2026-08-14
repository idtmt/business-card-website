from typing import Any

from backend.database.connection import get_connection


class ServiceRepository:
    async def create(
        self,
        name: str,
        description: str | None = None,
        position: int = 0,
        is_hidden: bool = False,
    ) -> int:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                INSERT INTO services (
                    name,
                    description,
                    position,
                    is_hidden
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    description,
                    position,
                    int(is_hidden),
                ),
            )

            await connection.commit()

            return cursor.lastrowid

    async def get_by_id(
        self,
        service_id: int,
    ) -> dict[str, Any] | None:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                SELECT
                    id,
                    name,
                    description,
                    position,
                    is_hidden
                FROM services
                WHERE id = ?
                """,
                (service_id,),
            )

            row = await cursor.fetchone()

            if row is None:
                return None

            return dict(row)

    async def get_all(
        self,
        is_hidden: bool | None = None,
    ) -> list[dict[str, Any]]:
        async with get_connection() as connection:
            if is_hidden is None:
                cursor = await connection.execute(
                    """
                    SELECT
                        id,
                        name,
                        description,
                        position,
                        is_hidden
                    FROM services
                    ORDER BY position, id
                    """
                )
            else:
                cursor = await connection.execute(
                    """
                    SELECT
                        id,
                        name,
                        description,
                        position,
                        is_hidden
                    FROM services
                    WHERE is_hidden = ?
                    ORDER BY position, id
                    """,
                    (int(is_hidden),),
                )

            rows = await cursor.fetchall()

            return [dict(row) for row in rows]

    async def update(
        self,
        service_id: int,
        name: str,
        description: str | None = None,
        position: int = 0,
        is_hidden: bool = False,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                UPDATE services
                SET
                    name = ?,
                    description = ?,
                    position = ?,
                    is_hidden = ?
                WHERE id = ?
                """,
                (
                    name,
                    description,
                    position,
                    int(is_hidden),
                    service_id,
                ),
            )

            await connection.commit()

            return cursor.rowcount > 0

    async def delete(
        self,
        service_id: int,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                DELETE FROM services
                WHERE id = ?
                """,
                (service_id,),
            )

            await connection.commit()

            return cursor.rowcount > 0
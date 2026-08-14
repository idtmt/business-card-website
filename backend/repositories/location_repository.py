from typing import Any

from backend.database.connection import get_connection


class LocationRepository:
    async def create(
        self,
        title: str,
        address: str,
        latitude: float,
        longitude: float,
        position: int = 0,
        is_hidden: bool = False,
    ) -> int:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                INSERT INTO locations (
                    title,
                    address,
                    latitude,
                    longitude,
                    position,
                    is_hidden
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    title,
                    address,
                    latitude,
                    longitude,
                    position,
                    int(is_hidden),
                ),
            )

            await connection.commit()

            return cursor.lastrowid

    async def get_by_id(
        self,
        location_id: int,
    ) -> dict[str, Any] | None:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                SELECT
                    id,
                    title,
                    address,
                    latitude,
                    longitude,
                    position,
                    is_hidden
                FROM locations
                WHERE id = ?
                """,
                (location_id,),
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
                        title,
                        address,
                        latitude,
                        longitude,
                        position,
                        is_hidden
                    FROM locations
                    ORDER BY position, id
                    """
                )
            else:
                cursor = await connection.execute(
                    """
                    SELECT
                        id,
                        title,
                        address,
                        latitude,
                        longitude,
                        position,
                        is_hidden
                    FROM locations
                    WHERE is_hidden = ?
                    ORDER BY position, id
                    """,
                    (int(is_hidden),),
                )

            rows = await cursor.fetchall()

            return [dict(row) for row in rows]

    async def update(
        self,
        location_id: int,
        title: str,
        address: str,
        latitude: float,
        longitude: float,
        position: int = 0,
        is_hidden: bool = False,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                UPDATE locations
                SET
                    title = ?,
                    address = ?,
                    latitude = ?,
                    longitude = ?,
                    position = ?,
                    is_hidden = ?
                WHERE id = ?
                """,
                (
                    title,
                    address,
                    latitude,
                    longitude,
                    position,
                    int(is_hidden),
                    location_id,
                ),
            )

            await connection.commit()

            return cursor.rowcount > 0

    async def delete(
        self,
        location_id: int,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                DELETE FROM locations
                WHERE id = ?
                """,
                (location_id,),
            )

            await connection.commit()

            return cursor.rowcount > 0
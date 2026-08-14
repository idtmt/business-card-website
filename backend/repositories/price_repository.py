from typing import Any

from backend.database.connection import get_connection


class PriceRepository:
    async def create(
        self,
        service_id: int,
        title: str,
        price: str,
        position: int = 0,
        is_hidden: bool = False,
    ) -> int:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                INSERT INTO prices (
                    service_id,
                    title,
                    price,
                    position,
                    is_hidden
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    service_id,
                    title,
                    price,
                    position,
                    int(is_hidden),
                ),
            )

            await connection.commit()

            return cursor.lastrowid

    async def get_by_id(
        self,
        price_id: int,
    ) -> dict[str, Any] | None:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                SELECT
                    id,
                    service_id,
                    title,
                    price,
                    position,
                    is_hidden
                FROM prices
                WHERE id = ?
                """,
                (price_id,),
            )

            row = await cursor.fetchone()

            if row is None:
                return None

            return dict(row)

    async def get_by_service(
        self,
        service_id: int,
        is_hidden: bool | None = None,
    ) -> list[dict[str, Any]]:
        async with get_connection() as connection:
            if is_hidden is None:
                cursor = await connection.execute(
                    """
                    SELECT
                        id,
                        service_id,
                        title,
                        price,
                        position,
                        is_hidden
                    FROM prices
                    WHERE service_id = ?
                    ORDER BY position, id
                    """,
                    (service_id,),
                )
            else:
                cursor = await connection.execute(
                    """
                    SELECT
                        id,
                        service_id,
                        title,
                        price,
                        position,
                        is_hidden
                    FROM prices
                    WHERE service_id = ?
                    AND is_hidden = ?
                    ORDER BY position, id
                    """,
                    (
                        service_id,
                        int(is_hidden),
                    ),
                )

            rows = await cursor.fetchall()

            return [dict(row) for row in rows]

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
                        service_id,
                        title,
                        price,
                        position,
                        is_hidden
                    FROM prices
                    ORDER BY service_id, position, id
                    """
                )
            else:
                cursor = await connection.execute(
                    """
                    SELECT
                        id,
                        service_id,
                        title,
                        price,
                        position,
                        is_hidden
                    FROM prices
                    WHERE is_hidden = ?
                    ORDER BY service_id, position, id
                    """,
                    (int(is_hidden),),
                )

            rows = await cursor.fetchall()

            return [dict(row) for row in rows]

    async def update(
        self,
        price_id: int,
        title: str,
        price: str,
        position: int = 0,
        is_hidden: bool = False,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                UPDATE prices
                SET
                    title = ?,
                    price = ?,
                    position = ?,
                    is_hidden = ?
                WHERE id = ?
                """,
                (
                    title,
                    price,
                    position,
                    int(is_hidden),
                    price_id,
                ),
            )

            await connection.commit()

            return cursor.rowcount > 0

    async def delete(
        self,
        price_id: int,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                DELETE FROM prices
                WHERE id = ?
                """,
                (price_id,),
            )

            await connection.commit()

            return cursor.rowcount > 0
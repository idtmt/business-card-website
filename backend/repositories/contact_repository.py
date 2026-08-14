from typing import Any

from backend.database.connection import get_connection


class ContactRepository:
    async def create(
        self,
        title: str,
        value: str,
        url: str | None = None,
        icon: str | None = None,
        position: int = 0,
        is_hidden: bool = False,
    ) -> int:
        async with get_connection() as connection:
            cursor = await connection.execute("""
                INSERT INTO contacts (
                    title,
                    value,
                    url,
                    icon,
                    position,
                    is_hidden
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                title,
                value,
                url,
                icon,
                position,
                int(is_hidden),
            ))

            await connection.commit()

            return cursor.lastrowid

    async def get_by_id(
        self,
        contact_id: int,
    ) -> dict[str, Any] | None:
        async with get_connection() as connection:
            cursor = await connection.execute("""
                SELECT
                    id,
                    title,
                    value,
                    url,
                    icon,
                    position,
                    is_hidden
                FROM contacts
                WHERE id = ?
            """, (contact_id,))

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
                cursor = await connection.execute("""
                    SELECT
                        id,
                        title,
                        value,
                        url,
                        icon,
                        position,
                        is_hidden
                    FROM contacts
                    ORDER BY position, id
                """)
            else:
                cursor = await connection.execute("""
                    SELECT
                        id,
                        title,
                        value,
                        url,
                        icon,
                        position,
                        is_hidden
                    FROM contacts
                    WHERE is_hidden = ?
                    ORDER BY position, id
                """, (int(is_hidden),))

            rows = await cursor.fetchall()

            return [dict(row) for row in rows]

    async def update(
        self,
        contact_id: int,
        title: str,
        value: str,
        url: str | None = None,
        icon: str | None = None,
        position: int = 0,
        is_hidden: bool = False,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute("""
                UPDATE contacts
                SET
                    title = ?,
                    value = ?,
                    url = ?,
                    icon = ?,
                    position = ?,
                    is_hidden = ?
                WHERE id = ?
            """, (
                title,
                value,
                url,
                icon,
                position,
                int(is_hidden),
                contact_id,
            ))

            await connection.commit()

            return cursor.rowcount > 0

    async def delete(
        self,
        contact_id: int,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute("""
                DELETE FROM contacts
                WHERE id = ?
            """, (contact_id,))

            await connection.commit()

            return cursor.rowcount > 0
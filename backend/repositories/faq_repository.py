from typing import Any

from backend.database.connection import get_connection


class FaqRepository:
    async def create(
        self,
        question: str,
        answer: str,
        position: int = 0,
        is_hidden: bool = False,
    ) -> int:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                INSERT INTO faq (
                    question,
                    answer,
                    position,
                    is_hidden
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    question,
                    answer,
                    position,
                    int(is_hidden),
                ),
            )

            await connection.commit()

            return cursor.lastrowid

    async def get_by_id(
        self,
        faq_id: int,
    ) -> dict[str, Any] | None:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                SELECT
                    id,
                    question,
                    answer,
                    position,
                    is_hidden
                FROM faq
                WHERE id = ?
                """,
                (faq_id,),
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
                        question,
                        answer,
                        position,
                        is_hidden
                    FROM faq
                    ORDER BY position, id
                    """
                )
            else:
                cursor = await connection.execute(
                    """
                    SELECT
                        id,
                        question,
                        answer,
                        position,
                        is_hidden
                    FROM faq
                    WHERE is_hidden = ?
                    ORDER BY position, id
                    """,
                    (int(is_hidden),),
                )

            rows = await cursor.fetchall()

            return [dict(row) for row in rows]

    async def update(
        self,
        faq_id: int,
        question: str,
        answer: str,
        position: int = 0,
        is_hidden: bool = False,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                UPDATE faq
                SET
                    question = ?,
                    answer = ?,
                    position = ?,
                    is_hidden = ?
                WHERE id = ?
                """,
                (
                    question,
                    answer,
                    position,
                    int(is_hidden),
                    faq_id,
                ),
            )

            await connection.commit()

            return cursor.rowcount > 0

    async def delete(
        self,
        faq_id: int,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                DELETE FROM faq
                WHERE id = ?
                """,
                (faq_id,),
            )

            await connection.commit()

            return cursor.rowcount > 0
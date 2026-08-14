from typing import Any

from backend.database.connection import get_connection


class ScheduleRepository:
    async def create(
        self,
        location_id: int,
        weekday: int,
        start_time: str | None = None,
        end_time: str | None = None,
        is_day_off: bool = False,
    ) -> int:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                INSERT INTO schedules (
                    location_id,
                    weekday,
                    start_time,
                    end_time,
                    is_day_off
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    location_id,
                    weekday,
                    start_time,
                    end_time,
                    int(is_day_off),
                ),
            )

            await connection.commit()

            return cursor.lastrowid

    async def get_by_id(
        self,
        schedule_id: int,
    ) -> dict[str, Any] | None:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                SELECT
                    id,
                    location_id,
                    weekday,
                    start_time,
                    end_time,
                    is_day_off
                FROM schedules
                WHERE id = ?
                """,
                (schedule_id,),
            )

            row = await cursor.fetchone()

            if row is None:
                return None

            return dict(row)

    async def get_by_location(
        self,
        location_id: int,
    ) -> list[dict[str, Any]]:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                SELECT
                    id,
                    location_id,
                    weekday,
                    start_time,
                    end_time,
                    is_day_off
                FROM schedules
                WHERE location_id = ?
                ORDER BY weekday
                """,
                (location_id,),
            )

            rows = await cursor.fetchall()

            return [dict(row) for row in rows]

    async def get_by_location_and_weekday(
        self,
        location_id: int,
        weekday: int,
    ) -> dict[str, Any] | None:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                SELECT
                    id,
                    location_id,
                    weekday,
                    start_time,
                    end_time,
                    is_day_off
                FROM schedules
                WHERE location_id = ?
                AND weekday = ?
                """,
                (location_id, weekday),
            )

            row = await cursor.fetchone()

            if row is None:
                return None

            return dict(row)

    async def update(
        self,
        schedule_id: int,
        weekday: int,
        start_time: str | None = None,
        end_time: str | None = None,
        is_day_off: bool = False,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                UPDATE schedules
                SET
                    weekday = ?,
                    start_time = ?,
                    end_time = ?,
                    is_day_off = ?
                WHERE id = ?
                """,
                (
                    weekday,
                    start_time,
                    end_time,
                    int(is_day_off),
                    schedule_id,
                ),
            )

            await connection.commit()

            return cursor.rowcount > 0

    async def delete(
        self,
        schedule_id: int,
    ) -> bool:
        async with get_connection() as connection:
            cursor = await connection.execute(
                """
                DELETE FROM schedules
                WHERE id = ?
                """,
                (schedule_id,),
            )

            await connection.commit()

            return cursor.rowcount > 0
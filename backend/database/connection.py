from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiosqlite

from backend.config import settings


@asynccontextmanager
async def get_connection() -> AsyncGenerator[
    aiosqlite.Connection,
    None,
]:
    async with aiosqlite.connect(
        settings.database_path,
    ) as connection:
        connection.row_factory = aiosqlite.Row

        await connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        yield connection
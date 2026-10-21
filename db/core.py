import asyncio
import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import aiosqlite


class Database:
    def __init__(self, path: str):
        self.path = path
        self._conn: aiosqlite.Connection | None = None
        self._lock = asyncio.Lock()

    @property
    def conn(self) -> aiosqlite.Connection:
        if self._conn is None:
            raise RuntimeError("Database not connected. Call `await db.connect()` first.")
        return self._conn

    async def connect(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = await aiosqlite.connect(self.path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.execute("PRAGMA journal_mode=WAL")
        await self._conn.execute("PRAGMA foreign_keys=ON")
        schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        await self._conn.executescript(schema)

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def fetch_value(self, query, params=(), default: Any = None) -> Any:
        async with self.conn.execute(query, params) as cur:
            row = await cur.fetchone()
        return default if row is None else row[0]

    async def fetch_one(self, query, params=()):
        async with self.conn.execute(query, params) as cur:
            return await cur.fetchone()

    async def fetch_all(self, query, params=()):
        async with self.conn.execute(query, params) as cur:
            return await cur.fetchall()

    async def execute(self, query, params=()):
        async with self._lock:
            cur = await self.conn.execute(query, params)
            await self.conn.commit()
            return cur

    @asynccontextmanager
    async def transaction(self):
        async with self._lock:
            try:
                yield self.conn
                await self.conn.commit()
            except BaseException:
                await self.conn.rollback()
                raise

async def sync_catalog(db: Database, path="gifs.json"):
    with open(path, encoding="utf-8") as f:
        gifs = json.load(f)

    async with db.transaction() as conn:
        await conn.executemany(
            """INSERT INTO gifs (id, url, tier, series)
               VALUES (:id, :url, :tier, :series)
               ON CONFLICT(id) DO UPDATE SET
                   url = excluded.url,
                   tier = excluded.tier,
                   series = excluded.series""",
            gifs,
        )
        ids = [g["id"] for g in gifs]
        marks = ",".join("?" * len(ids))
        await conn.execute(f"UPDATE gifs SET active = 0 WHERE id NOT IN ({marks})", ids)
        await conn.execute(f"UPDATE gifs SET active = 1 WHERE id IN ({marks})", ids)


import asyncio
import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import aiosqlite

MIGRATIONS_DIR = Path(__file__).with_name("migrations")

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
        await self.migrate()

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def migrate(self):
        current = await fetch_value_required(self.conn, "PRAGMA user_version")

        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            version = int(path.stem.split("_")[0])
            if version <= current:
                continue
            sql = path.read_text(encoding="utf-8")
            try:
                await self.conn.executescript(
                    f"BEGIN;\n{sql}\nPRAGMA user_version = {version};\nCOMMIT;"
                )
            except BaseException:
                try: 
                    await self.conn.execute("ROLLBACK")
                except Exception:
                    pass
                raise
            print(f"Applied migration {path.name}")


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

    # NOTE: This is invoked before any calls
    async def ensure_user(self, user_id: int):
        async with self.transaction() as conn:
            await conn.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id, )
            )

async def fetch_required(conn: aiosqlite.Connection, query: str, params=()) -> aiosqlite.Row:
    """Fetch one row, raising if the query returned nothing."""
    async with conn.execute(query, params) as cur:
        row = await cur.fetchone()
    if row is None:
        raise LookupError(f"Expected a row but found none: {' '.join(query.split())[:80]}")
    return row

async def fetch_value_required(conn: aiosqlite.Connection, query: str, params=()) -> Any:
    """Fetch the first column of one row, raising if there is no row."""
    return (await fetch_required(conn, query, params))[0]

async def fetch_optional(
    conn: aiosqlite.Connection, query: str, params=()
) -> aiosqlite.Row | None:
    """Fetch one row, or None if the query returned nothing."""
    async with conn.execute(query, params) as cur:
        return await cur.fetchone()

async def sync_catalog(db: Database, path="gifs.json"):
    with open(path, encoding="utf-8") as f:
        gifs = json.load(f)

    async with db.transaction() as conn:
        await conn.executemany(
            """INSERT INTO gifs (id, url, tier, series, media_url)
               VALUES (:id, :url, :tier, :series, :media_url)
               ON CONFLICT(id) DO UPDATE SET
                   url = excluded.url,
                   tier = excluded.tier,
                   series = excluded.series,
                   media_url = excluded.media_url
            """,
            gifs,
        )
        ids = [g["id"] for g in gifs]
        marks = ",".join("?" * len(ids))
        await conn.execute(f"UPDATE gifs SET active = 0 WHERE id NOT IN ({marks})", ids)
        await conn.execute(f"UPDATE gifs SET active = 1 WHERE id IN ({marks})", ids)


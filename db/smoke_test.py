import asyncio
from core import Database, sync_catalog

async def main():
    db = Database("db/data/bot.db")
    await db.connect()
    await sync_catalog(db)
    print(await db.fetch_value("SELECT COUNT(*) FROM gifs"))
    await db.close()

asyncio.run(main())

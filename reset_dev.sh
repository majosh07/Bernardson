# reset_dev.sh
set -e
rm -f db/data/bot.db db/data/bot.db-wal db/data/bot.db-shm
python -c "
import asyncio
from db.core import Database, sync_catalog
async def main():
    db = Database('db/data/bot.db')
    await db.connect()          # runs migrations
    await sync_catalog(db, 'db/gifs.json')      # fills gifs
    await db.close()
asyncio.run(main())
"
sqlite3 db/data/bot.db < db/seed.sql
echo "reset done"

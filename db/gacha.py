from .core import Database


class GachaRepo:
    def __init__(self, db: Database):
        self.db = db

    async def ensure_user(self, user_id: int, starting_rolls: int = 10):
        async with self.db.transaction() as conn:
            await conn.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id, )
            )
            await conn.execute(
                "INSERT OR IGNORE INTO user_gacha (user_id, roll_count) VALUES (?, ?)", 
                (user_id, starting_rolls),
            )

    async def get_rolls(self, user_id: int) -> int:
        await self.ensure_user(user_id)
        return await self.db.fetch_value(
            """SELECT roll_count FROM user_gacha WHERE user_id = ?""",
            (user_id,),
            default=0,
        )

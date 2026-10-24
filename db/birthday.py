from dataclasses import dataclass
from zoneinfo import ZoneInfo
from db.core import Database
import datetime as dt

EASTERN = ZoneInfo("America/New_York")

@dataclass(frozen=True)
class IdAndAge:
    id: int
    age: int | None

@dataclass(frozen=True)
class BirthdayDate:
    month: int
    day: int
    year: int | None

class BirthdayRepo:
    def __init__(self, db: Database) -> None:
        self.db = db

    # list of tuples, [0: id, 1: age(can be None)]
    async def todays_birthdays(self) -> list[IdAndAge]:
        today = dt.datetime.now(EASTERN).date()
        params = [(today.month, today.day)]

        is_leap = today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0)
        if today.month == 2 and today.day == 28 and not is_leap:
            params.append((2, 29))

        ids_and_age: list[IdAndAge] = []
        for month, day in params:
            rows = await self.db.fetch_all(
                """SELECT user_id, year FROM birthdays WHERE month = ? AND day = ?""",
                (month, day),
            )
            for r in rows:
                ids_and_age.append(
                    IdAndAge(
                        id=r["user_id"],
                        age=today.year - r["year"] if r["year"] is not None else None
                    )
                )

        return ids_and_age

    async def claim_today(self) -> bool:
        today = dt.datetime.now(EASTERN).date().isoformat()
        async with self.db.transaction() as conn:
            cur = await conn.execute(
                """
                INSERT INTO bot_state (key, value) VALUES ('last_birthday_date', ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                WHERE bot_state.value < excluded.value
                """,
                (today,)
            )
            return cur.rowcount == 1

    async def set_birthday(self, user_id: int, month: int, day: int, year: int | None = None):
        await self.db.execute(
            """
            INSERT INTO birthdays (user_id, month, day, year) VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET 
            month = excluded.month, 
            day = excluded.day,
            year = excluded.year
            """,
            (user_id, month, day, year),
        )
    async def remove_birthday(self, user_id: int):
        await self.db.execute(
            """DELETE FROM birthdays WHERE user_id = ?""", (user_id, ),
        )

    async def check_birthday(self, user_id: int) -> BirthdayDate:
        cur = await self.db.execute(
            """SELECT month, day, year FROM birthdays WHERE user_id = ?""", (user_id, ),
        )
        row = await cur.fetchone()
        if cur.rowcount == 0 or row is None:
            raise ValueError("User does not have a birthday set...")

        return BirthdayDate(
            month=row["month"],
            day=row["day"],
            year=row["year"],
        )









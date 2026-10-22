from .core import Database, fetch_required, fetch_value_required, fetch_optional
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from models import DailyResult, DailyProgress, DailyReveal, Gif

EASTERN = ZoneInfo("America/New_York")



class GachaRepo:
    def __init__(self, db: Database):
        self.db = db

    async def daily_gif(self, user_id: int) -> DailyResult:
        today_d = datetime.now(EASTERN).date()
        today = today_d.isoformat()
        yesterday = (today_d - timedelta(days=1)).isoformat()

        async with self.db.transaction() as conn:
            row = await fetch_optional(conn,
                """
                INSERT OR IGNORE INTO daily_gifs (date, gif_id, triggered_by)
                SELECT ?, id, ? FROM gifs WHERE active = 1
                ORDER BY RANDOM() LIMIT 1
                RETURNING created_at, triggered_by
                """,
                (today, user_id),
            )
            first_of_day = row is not None
            if row is None:
                row = await fetch_required(
                    conn,
                    """
                    SELECT created_at, triggered_by FROM daily_gifs WHERE date = ?
                    """,
                    (today,)
                )
            time_created = row["created_at"]
            triggered_by = row["triggered_by"]

            prev_streak = await fetch_value_required(conn,
                """
                SELECT roll_streak FROM user_gacha WHERE user_id = ?
                """,
                (user_id,)
            )

            # update streak, update rolls, 
            row = await fetch_optional(conn,
                """
                UPDATE user_gacha
                SET roll_count = roll_count + 1,
                    roll_streak = CASE WHEN last_daily_date = ? THEN roll_streak + 1 ELSE 1 END,
                    last_daily_date = ?
                WHERE user_id = ? AND (last_daily_date IS NULL OR last_daily_date < ?)
                RETURNING roll_count, roll_streak
                """,
                (yesterday, today, user_id, today),
            )
            roll_granted = row is not None
            if row is None:
                row = await fetch_required(
                    conn,
                    "SELECT roll_count, roll_streak FROM user_gacha WHERE user_id = ?",
                    (user_id,),
                )
            num_rolls = row["roll_count"]
            streak = row["roll_streak"]

            row = await fetch_required(conn,
                """
                SELECT g.id, g.tier, g.url, g.media_url
                FROM daily_gifs AS d JOIN gifs AS g ON g.id = d.gif_id
                WHERE d.date = ?
                """,
                (today, ),
            )
            gif = Gif.from_row(row)

        return DailyResult(
            gif=gif,
            progress=DailyProgress(
                num_rolls=num_rolls, 
                streak=streak, 
                prev_num_rolls=num_rolls - 1 if roll_granted else num_rolls,
                prev_streak=prev_streak,
                roll_given=roll_granted
            ),
            reveal=DailyReveal(
                time_created=time_created,
                triggered_by=triggered_by
            ),
            first_of_day=first_of_day
        )

    async def roll(self, user_id: int):
        pass


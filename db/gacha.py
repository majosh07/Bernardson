from .core import Database, fetch_required, fetch_value_required, fetch_optional
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from .models import (
    DailyResult,
    DailyProgress,
    DailyReveal,
    Gif,
    RollResult,
    UserGifsStats,
    UserInfo,
    UserStatsResult
)
from gacha.gacha_probabilities import choose_tier

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

    # If return None, then error
    async def roll(self, user_id: int) -> RollResult:
        async with self.db.transaction() as conn:
            cur = await conn.execute(
                """
                UPDATE user_gacha
                SET roll_count = roll_count - 1
                WHERE user_id = ? AND roll_count > 0
                RETURNING a_pity, s_pity, roll_count
                """,
                (user_id,),
            )
            row = await cur.fetchone()
            # Could not subtract roll
            if cur.rowcount == 0 or row is None:
                raise ValueError("Could not subtract rolls")

            tier, used_pity = choose_tier(row["a_pity"], row["s_pity"])
            roll_count = row["roll_count"]

            row = await fetch_required(
                conn,
                """
                SELECT id, url, tier, media_url
                FROM gifs
                WHERE tier = ?
                ORDER BY RANDOM()
                LIMIT 1
                """,
                (tier,)
            )
            gif = Gif.from_row(row)

            return RollResult(
                gif=gif,
                num_rolls_left=roll_count,
                used_pity=used_pity,
            )


    # Returns None if not a current user
    async def user_stats(self, user_id: int) -> UserStatsResult:
        async with self.db.transaction() as conn:
            cur = await conn.execute(
                """
                SELECT 
                    us.user_id,
                    ug.roll_count, 
                    ug.roll_streak, 
                    ug.last_daily_date, 
                    ug.s_pity, 
                    ug.a_pity, 
                    us.created_at
                FROM users AS us 
                JOIN user_gacha AS ug 
                ON us.user_id = ?
                """,
                (user_id,),
            )

            # Could not find user
            row = await cur.fetchone()
            if cur.rowcount == 0 or row is None:
                raise ValueError("User does not exist")
            
            user_info = UserInfo.from_row(row)

            row = await fetch_required(
                conn,
                """
                SELECT
                    COUNT(*) AS num_gifs,
                    COUNT(CASE WHEN g.tier = 'S' THEN 1 END) AS num_s,
                    COUNT(CASE WHEN g.tier = 'A' THEN 1 END) AS num_a,
                    COUNT(CASE WHEN g.tier = 'B' THEN 1 END) AS num_b,
                    COUNT(CASE WHEN g.tier = 'C' THEN 1 END) AS num_c
                FROM user_gifs AS ug
                INNER JOIN gifs AS g ON ug.gif_id = g.id
                WHERE ug.user_id = ?
                """,
                (user_id,)
            )
            gif_stats = UserGifsStats(
                num_gifs=row["num_gifs"],
                num_s=row["num_s"],
                num_a=row["num_a"],
                num_b=row["num_b"],
                num_c=row["num_c"],
            )

            return UserStatsResult(
                user_info=user_info,
                gif_stats=gif_stats
            )




from dataclasses import dataclass

@dataclass(frozen=True)
class UserInfo:
    user_id: int
    roll_count: int
    roll_streak: int
    last_daily_date: None
    a_pity: int
    s_pity: int
    created_at: int

    @classmethod
    def from_row(cls, row) -> "UserInfo":
        return cls(
            user_id=row["user_id"],
            roll_count=row["roll_count"],
            roll_streak=row["roll_streak"],
            last_daily_date=row["last_daily_date"],
            a_pity=row["a_pity"],
            s_pity=row["s_pity"],
            created_at=row["created_at"],
        )
@dataclass(frozen=True)
class Gif:
    id: int
    tier: str
    url: str
    media_url: str

    @classmethod
    def from_row(cls, row) -> "Gif":
        return cls(
            id=row["id"],
            tier=row["tier"],
            url=row["url"],
            media_url=row["media_url"],
        )
@dataclass(frozen=True)
class DailyProgress:
    """User's daily state"""
    num_rolls: int
    streak: int
    prev_num_rolls: int
    prev_streak: int
    roll_given: bool # true if first daily today, so get roll

@dataclass(frozen=True)
class DailyReveal:
    """Who triggered reveal and when"""
    time_created: int # discord will render this to own timezone
    triggered_by: int

@dataclass(frozen=True)
class DailyResult:
    gif: Gif
    progress: DailyProgress
    reveal: DailyReveal
    first_of_day: bool # user did gif of the day

@dataclass(frozen=True)
class RollResult:
    gif: Gif
    num_rolls_left: int
    used_pity: bool

@dataclass(frozen=True)
class UserGifsStats:
    num_gifs: int
    num_s: int
    num_a: int
    num_b: int
    num_c: int

@dataclass(frozen=True)
class UserStatsResult:
    user_info: UserInfo
    gif_stats: UserGifsStats



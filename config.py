import os
from dataclasses import dataclass
from dotenv import load_dotenv 

load_dotenv()

def _flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("true", "1", "t", "yes")

def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is not set (check your .env)")
    return value

@dataclass(frozen=True)
class Config:
    token: str
    is_test: bool
    prefix: str
    db_path: str
    birthday_channel_id: int
    gacha_channel_id: int

    @classmethod
    def load(cls) -> "Config":
        is_test = _flag("TEST_BOT")
        return cls(
            token=_require("DISCORD_TOKEN"),
            is_test=is_test,
            prefix="!" if is_test else ";;",
            db_path="db/data/test.db" if is_test else "db/data/bot.db",
            birthday_channel_id=int(_require("BIRTHDAY_CHANNEL_ID")),
            gacha_channel_id=int(_require("GACHA_CHANNEL_ID"))
        )

config = Config.load()

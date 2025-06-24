from zoneinfo import ZoneInfo
from discord.ext import commands, tasks
from gacha.database import has_day_passed, get_last_status
from datetime import datetime
from queries import *




dates = [
    datetime(year=2025, month=6, day=23),
    datetime(year=2025, month=6, day=23),
]

CHANNEL_ID = 1136423792822997002

class Birthdays(commands.Cog):
    def __init__(self, bot, args) -> None:
        self.bot = bot
        self.args = args
        self.last_status = get_last_status()

        self.est = ZoneInfo('US/Eastern')

        self.celebrate.start()

    def cog_unload(self) -> None: #pyright: ignore
        self.celebrate.cancel()

    @tasks.loop(seconds=5.0)
    async def celebrate(self):
        if not has_day_passed(self.last_status):
            return

        channel = self.bot.get_channel(CHANNEL_ID)
        today = datetime.now()
        for birth in dates:
            if birth.date() == today.date():
                await channel.send(f"It is {birth}")
        self.last_status = datetime.now().astimezone(self.est)

    @celebrate.before_loop
    async def before_celebrate(self):
        await self.bot.wait_until_ready()




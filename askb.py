from dotenv import load_dotenv
import os
import discord
from discord.ext.commands import Bot
from gacha import Gacha
from database import Database
from keep_alive import keep_alive
import asyncio
import signal
# import logging

# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--admin', action='store_true', help='Enables Unlimited for Admin')
args = parser.parse_args()


load_dotenv()
TOKEN = os.environ.get('TOKEN')
if TOKEN is None:
  raise ValueError("TOKEN not set correctly, check .env...")

intents = discord.Intents.default()
intents.message_content= True


class askBernardson(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
    async def setup_hook(self) -> None:
        await self.add_cog(Gacha(self, self.db, args))

    async def on_ready(self):
        print(f'{self.user} has connected to Discord.')

    async def on_close(self):
        await self.shutdown()

    async def shutdown(self):
        await self.db.close()
        await self.close()

load_dotenv()
db_url = os.environ.get('DATABASE_URL')
if db_url:
    bot = askBernardson(command_prefix=';;', intents=intents)
else:
    bot = askBernardson(command_prefix='!', intents=intents)
# bot.run(TOKEN, log_handler=handler, root_logger=True)
async def main(TOKEN):
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(bot.shutdown()))

    await bot.db.open_pool()
    keep_alive(bot.db)
    await bot.start(TOKEN)

asyncio.run(main(TOKEN))




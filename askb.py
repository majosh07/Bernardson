from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from gacha.cog import Gacha
from jokebox.cog import Jokebox
from notifs.cog import Notifs
from keep_alive import keep_alive
import asyncio
import signal
from pool import pool
from logging_config import logger
from gacha.database import OWNER_ID

# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--admin-daily', dest='admin_daily', action='store_true', help='Enable daily admin mode')
parser.add_argument('--admin-streak', dest='admin_streak', action='store_true', help='Enable streak admin mode')
parser.add_argument('--admin', action='store_true', help='Enable all admin features')

args = parser.parse_args()

# Handle --admin manually
if args.admin:
    args.admin_daily = True
    args.admin_streak = True
if args.admin_daily: logger.info("ADMIN DAILY IS TRUE")
if args.admin_streak: logger.info("ADMIN STREAK IS TRUE")


load_dotenv()
TOKEN = os.environ.get('TOKEN')
if TOKEN is None:
  raise ValueError("TOKEN not set correctly, check .env...")

intents = discord.Intents.default()
intents.message_content= True
intents.reactions = True
intents.messages = True

class askBernardson(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    async def setup_hook(self) -> None:
        await self.add_cog(Gacha(self, args))
        await self.add_cog(Jokebox(self, args))
        await self.add_cog(Notifs(self, args))

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord.')

    async def on_close(self):
        await self.shutdown()

    async def shutdown(self):
        await pool.close()
        await self.close()

@commands.command(aliases=["sh"])
async def shutdown(ctx):
    if ctx.author.id == OWNER_ID:
        await ctx.send("Stopping bot...")
        await ctx.bot.shutdown()

load_dotenv()
db_url = os.environ.get('DATABASE_URL')
if db_url:
    bot = askBernardson(command_prefix=';;', intents=intents)
else:
    bot = askBernardson(command_prefix='!', intents=intents)
bot.add_command(shutdown)
# bot.run(TOKEN, log_handler=handler, root_logger=True)
async def main(TOKEN):
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(bot.shutdown()))

    await pool.open()
    keep_alive()
    await bot.start(TOKEN)


asyncio.run(main(TOKEN))




from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
# from gacha.database import OWNER_ID
import asyncio
import signal
from gacha.cog import Gacha
from jokebox.cog import Jokebox
from birthdays.cog import Birthdays
from logging_config import logger
from db.core import Database, sync_catalog
import traceback

from config import config

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
intents.members = True

class askBernardson(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db: Database | None = None

    async def before_invoke_hook(self, ctx):
        await self.db.ensure_user(ctx.author.id) # pyright: ignore

    async def setup_hook(self) -> None:
        self.db = Database(config.db_path)
        await self.db.connect()

        await sync_catalog(self.db, "db/gifs.json")
        self.before_invoke(self.before_invoke_hook)

        await self.add_cog(Gacha(self, args, self.db))
        await self.add_cog(Jokebox(self, args))
        await self.add_cog(Birthdays(self, args, self.db))

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord.')

    async def handle_unexpected_error(self, ctx, error):
        # ignore commands that don't exist, so typos don't spam the console
        if isinstance(error, commands.CommandNotFound):
            return

        # failed checks (like your wrong-channel check) are expected
        if isinstance(error, commands.CheckFailure):
            return

        # if the command itself crashed, the real exception is wrapped
        original = getattr(error, "original", error)

        traceback.print_exception(type(original), original, original.__traceback__)
        await ctx.send(f"Something went wrong: `{type(original).__name__}: {original}`")

    async def on_command_error(self, ctx, error):
        # a command-level or cog-level handler already dealt with it
        if hasattr(ctx.command, "on_error"):
            return
        if ctx.cog and ctx.cog.has_error_handler():
            return
        await self.handle_unexpected_error(ctx, error)


    async def shutdown(self):
        try:
            await super().close()
        finally:
            if self.db is not None:
                await self.db.close()


@commands.command(aliases=["sh"])
async def shutdown(ctx):
    # if ctx.author.id == OWNER_ID:
        await ctx.send("Stopping bot...")
        await ctx.bot.close()

load_dotenv()

bot = askBernardson(command_prefix=config.prefix, intents=intents)
bot.add_command(shutdown)

async def main(token):
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(bot.shutdown()))

    try:
        await bot.start(token)
    finally:
        await bot.close()


asyncio.run(main(config.token))




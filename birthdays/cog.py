import traceback
from typing import Optional

import discord
from discord import Member
from discord.ext import commands, tasks
import datetime as dt
from db.birthday import EASTERN, BirthdayRepo, BirthdayDate
from config import config


class Birthdays(commands.Cog):
    def __init__(self, bot, args, db) -> None:
        self.bot = bot
        self.args = args
        self.repo = BirthdayRepo(db)

    async def cog_load(self) -> None: # pyright: ignore
        self.celebrate.start() # pyright: ignore
        self.bot.loop.create_task(self._catch_up())

    async def cog_unload(self) -> None: # pyright: ignore
        self.celebrate.cancel() # pyright: ignore

    async def _catch_up(self):
        await self.bot.wait_until_ready()
        now = dt.datetime.now(EASTERN)
        if now.hour >= 9:
            try:
                await self.announce_today()
            except Exception:
                traceback.print_exc()

    @tasks.loop(time=dt.time(hour=9, minute=0, tzinfo=EASTERN))
    async def celebrate(self):
        await self.bot.wait_until_ready()
        try:
            await self.announce_today()
        except Exception:
            traceback.print_exc()

    @commands.group(invoke_without_command=True)
    async def birthday(self, ctx):
        await ctx.send(
            f"""
            Usage: 
                   `{ctx.prefix}birthday set <month> <day> [year]`
                   `{ctx.prefix}birthday remove`
                   `{ctx.prefix}birthday check [@mention]`
            """
        )

    @birthday.command(name="set")
    async def birthday_set(self, ctx, month: int, day: int, year:int | None = None):
        try:
            proposed = dt.date(year or 2000, month, day)
        except ValueError:
            return await ctx.send("That is not a real date...")

        # Check to see if birthday is not in the future
        today = dt.datetime.now(EASTERN).date()
        if year is not None and proposed > today:
            return await ctx.send("That date is in the future...")

        await self.repo.set_birthday(ctx.author.id, month, day, year)
        if year is not None:
            date = dt.date(year, month, day).strftime("%B %d %Y")
            await ctx.send(f"Birthday added for {date}!")
        else:
            date = dt.date(2000, month, day).strftime("%B %d")
            await ctx.send(f"Birthday added for {date}!")


    @birthday.command(name="remove")
    async def birthday_remove(self, ctx):
        await self.repo.remove_birthday(ctx.author.id)
        await ctx.send("Birthday removed.")

    @birthday.command(name="check")
    async def birthday_check(self, ctx, member: Optional[Member] = None):
        user = member or ctx.author
        try:
            date: BirthdayDate = await self.repo.check_birthday(user.id)
        except ValueError:
            return await ctx.send(f"{user.name} does not have a birthday set...")

        if date.year is not None:
            str_date = dt.date(date.year, date.month, date.day).strftime("%B %d %Y")
        else:
            str_date = dt.date(2000, date.month, date.day).strftime("%B %d")
        await ctx.send(f"{user.name}'s birthday is {str_date}!")


    async def announce_today(self):
        channel = self.bot.get_channel(config.birthday_channel_id)
        if not isinstance(channel, discord.abc.Messageable):
            return
        if not await self.repo.claim_today():
            return
        birthdays = await self.repo.todays_birthdays()
        if not birthdays:
            return

        # NOTE: this might be a problem if there are too many people on one day
        for b in birthdays:
            if b.age is not None:
                greeting = f"Happy {get_ordinal(b.age)} Birthday!"
            else:
                greeting = f"Happy Birthday!"
            await channel.send(f"🎂🥳 {greeting} <@{b.id}>")

def get_ordinal(num: int) -> str:
    if 10 <= num % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(num % 10, "th")
    return f"{num}{suffix}"


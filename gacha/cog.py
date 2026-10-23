import asyncio
import discord
from typing import Optional
from discord import Embed, Member
from discord.ext import commands
from datetime import datetime, timezone

from db.gacha import GachaRepo, NotEnoughRolls
from db.models import DailyResult, RollResult, UserStatsResult, RollListResult
from gacha.utils import get_display_name
import time
import random

GACHA_CHANNEL_ID = 1129160056387153990
TESTING_CHANNEL_ID = 1136423792822997002

SECONDS_IN_A_DAY = 86400


class Gacha(commands.Cog):
    def __init__(self, bot, args, db) -> None:
        self.bot = bot
        self.args = args
        self.repo = GachaRepo(db)

    @commands.Cog.listener()
    async def on_ready(self):
        from gacha.help import help_texts
        for name, data in help_texts.items():
            command = self.bot.get_command(name)
            if command:
                command.help = data["help"]
                command.brief = data["brief"]
                command.usage = data["usage"]

    async def cog_check(self, ctx): # pyright: ignore
        if ctx.prefix == ";;" and ctx.channel.id != GACHA_CHANNEL_ID and ctx.channel.id != TESTING_CHANNEL_ID:
            return False
        return True

    @commands.command(aliases=['d', 'b', 'askbofday', 'askboftheday',])
    async def the_day(self, ctx):
        info: DailyResult = await self.repo.daily_gif(user_id=ctx.author.id)
        
        name = await get_display_name(self.bot, ctx.guild, info.reveal.triggered_by)
        embed = make_daily_embed(info, name)

        await ctx.send(embed=embed)


    @commands.command(aliases=['r', 'roll'])
    async def the_roll(self, ctx, count: int = 1):
        if count not in (1, 10):
            return await ctx.send("You can only pull 1 or 10 at a time...")
        try:
            roll: RollListResult = await self.repo.roll(user_id=ctx.author.id, count=count)
        except NotEnoughRolls:
            await ctx.send("You don't have any rolls left ...")
            return

        name = await get_display_name(self.bot, ctx.guild, ctx.author.id)
        if count == 1:
            embed = make_rolled_embed(roll.roll_list[0], name, roll.num_rolls_left)
            await ctx.send(embed=embed)
        else:
            await show_multi(ctx, roll.roll_list, name, roll.num_rolls_left)

    @commands.command(aliases=['tr'])
    async def testroll(self, ctx, *tiers: str):
        gifs = await self.repo.random_gifs_for_test()  # or grab any Gif row
        fake = [RollResult(gif=gif, used_pity=False) for gif in gifs]  # or grab any Gif row 
        await show_multi(ctx, fake, "name", 1000000)

    @commands.command(aliases=['s',])
    async def stats(self, ctx, member: Optional[Member] = None):
        member = member or ctx.author
        try:
            stats = await self.repo.user_stats(member.id)
        except ValueError:
            await ctx.send("User is not in the database...")
            return
        
        stats_name = await get_display_name(self.bot, ctx.guild, stats.user_info.user_id)
        triggered_by = await get_display_name(self.bot, ctx.guild, ctx.author.id)
        pfp = member.display_avatar.url

        embeds = make_stats_embeds(stats, stats_name, pfp, triggered_by)
        await ctx.send(embeds=embeds)

    @commands.command(aliases=['f',])
    async def favorite(self, ctx, check_gif_id: Optional[str] = None):
        if check_gif_id is None:
            await ctx.send("Missing GIF_ID")
            return
        if not isinstance(check_gif_id, str) or not check_gif_id.isdigit():
            await ctx.send("Not a valid GIF_ID")
            return

        gif_id = int(check_gif_id) 
        # get the gif, 
        # need to check to see if in inventory



    # @commands.command(aliases=['f',])
    # async def favorite(self, ctx, gif_id: Optional[str] = None):
    #     if gif_id is None:
    #         await ctx.send("Missing GIF_ID")
    #         return
    #     if not isinstance(gif_id, str) or not gif_id.isdigit():
    #         await ctx.send("Not a valid GIF_ID")
    #         return
    #
    #     gif_id = int(gif_id) # pyright: ignore
    #
    #     gifs = find_user_gifs(gif_id, ctx.author)
    #
    #     if gifs is None or not isinstance(gifs, list):
    #         await ctx.send("Couldn't Find GIF in Inventory(Are you sure you have it?)")
    #         return
    #
    #     gif = await self.select_gif(ctx, gifs)
    #
    #     if gif is None:
    #         await ctx.send("Cancelled Favorite...")
    #         return
    #     elif gif is False:
    #         await ctx.send("Already have GIF added")
    #         return
    #
    #     add_fav_gif(gif, ctx.author)
    #     await ctx.send(f"Added GIF ID: {gif['id']} to {ctx.author.name}'s favorites.")
    #
    #
    # @commands.command(aliases=['uf',])
    # async def unfavorite(self, ctx, gif_id: Optional[str] = None):
    #     if gif_id is None:
    #         await ctx.send("Missing GIF_ID")
    #         return
    #     if not isinstance(gif_id, str) or not gif_id.isdigit():
    #         await ctx.send("Not a valid GIF_ID")
    #         return
    #
    #     gif_id = int(gif_id) # pyright: ignore
    #
    #     gif = check_gif_in_fav(gif_id, ctx.author.id)
    #
    #     if gif is None:
    #         await ctx.send(f"GIF ID: {gif_id} is not in your favorites...")
    #         return
    #
    #     other_gif_info = get_gif_from_gif_id(gif_id)
    #     gif['tier'] = other_gif_info['tier']
    #     gif['url'] = other_gif_info['url']
    #     gif['id'] = gif_id
    #
    #     embeds = self.make_fav_embed(gif, ctx.author.name, False)
    #
    #     message = await ctx.send(embeds=embeds)
    #
    #     if await self.are_you_sure(ctx, message) == "✅":
    #         remove_fav_gif(gif_id, ctx.author.id)
    #         await ctx.send(f"Removed GIF ID: {gif_id} from {ctx.author.name}'s favorites")
    #     else:
    #         await ctx.send(f"Cancelled unfavorite...")
    #
    #
    #
    #
    # # today_gif, is_new, roll_count, roll_count, prev_roll_count, daily_streak, prev_daily_streak, was_bonus
def make_daily_embed(info: DailyResult, name: str):
    embed = None

    if info.first_of_day:
        embed = Embed(
            title="New Daily GIF!",
            color=0xFF0000,
        )
    else:
        embed = Embed(
            title="Daily GIF",
            color=0x0000FF,
        )

    prog = info.progress

    num_rolls = str(prog.num_rolls) if prog.prev_num_rolls == prog.num_rolls else f"({prog.prev_num_rolls}) -> **{prog.num_rolls}**"
    daily_streak = str(prog.prev_streak) if prog.prev_streak == prog.streak else f"({prog.prev_streak}) -> **{prog.streak}**"

    embed.add_field(name="Tier", value=info.gif.tier)
    # if info.:
    #     embed.add_field(name="Daily Streak!!!", value=daily_streak)
    #     embed.add_field(name="Num Rolls", value=f"{num_rolls}!!!")
    # else:
    embed.add_field(name="Daily Streak", value=daily_streak)
    embed.add_field(name="Num Rolls", value=num_rolls)
    embed.timestamp = datetime.fromtimestamp(info.reveal.time_created, tz=timezone.utc)
    embed.set_footer(text=f"Triggered by: {name}")

    embed.set_image(url=info.gif.media_url)
    return embed

TIER_COLOR = {"S": 0xFFD700, "A": 0x7F00FF, "B": 0x00CC66, "C": 0x000099}
TIER_TITLE = {"S": "👑 S 👑", "A": "🔮 A 🔮", "B": "B", "C": "C"}
TIER_RANK = {"C":0, "B": 1, "A": 2, "S": 3}

def make_rolled_embed(roll: RollResult, name: str, num_rolls_left: int):
    embed = Embed()
    gif = roll.gif
    embed.color = TIER_COLOR[gif.tier]
    embed.title = TIER_TITLE[gif.tier]

    embed.add_field(name="Tier", value=gif.tier)
    embed.add_field(name="GIF ID", value=gif.id)
    embed.add_field(name="Num Rolls Left", value=str(num_rolls_left))
    if roll.used_pity:
        embed.add_field(name="HARD PITY", value="HIT HARD PITY")
    embed.set_footer(text=f"For {name}")
    if gif.tier in ("S", "A"):
        embed.set_image(url=gif.media_url)
    else:
        embed.set_thumbnail(url=gif.media_url)


    return embed


TEASER_GIFS: list[str] = [
    "https://c.tenor.com/xy2XPgbXW7cAAAAd/tenor.gif",
    "https://c.tenor.com/fa2VEMOWWpEAAAAd/tenor.gif"
    "https://c.tenor.com/fxLi6csjaXwAAAAd/tenor.gif",
]

async def show_multi(ctx, results: list[RollResult], name: str, rolls_left: int):
    embeds = [make_rolled_embed(res, name, rolls_left) for res in results]

    view = RevealView(ctx.author.id)

    teaser = discord.Embed(title="🎰")
    teaser.set_image(url=random.choice(TEASER_GIFS))
    msg = await ctx.send("Rolling...", embed=teaser, view=view)

    await view.wait_or_skip(3)

    # add 2 card per 1.5 seconds, rarest last
    for n in range(2, len(embeds), 2):
        if view.skipped.is_set():
            break
        await msg.edit(embeds=embeds[:n])
        await view.wait_or_skip(1.5)

    # everything shown, text and button removed
    await msg.edit(content=None, embeds=embeds, view=None)
    view.stop()

    await asyncio.sleep(1.5)
    await msg.edit(embeds=embeds)


def make_stats_embeds(stats: UserStatsResult, name: str, pfp: str, triggered_by: str):
    user_info = stats.user_info
    gif_stats = stats.gif_stats

    days_since_created = int((time.time() - user_info.created_at) / SECONDS_IN_A_DAY)

    embed1 = Embed()
    embed1.title = f"{name}'s Info"
    embed1.set_footer(text=f"Triggered by {triggered_by}")

    embed1.add_field(name="Num Rolls", value=user_info.roll_count, inline=True)
    embed1.add_field(name="Daily Streak", value=user_info.roll_streak, inline=True)
    embed1.add_field(name="S Pity", value=user_info.s_pity, inline=True)
    embed1.add_field(name="A Pity", value=user_info.a_pity, inline=True)
    embed1.add_field(name="Created Account", value=f"({days_since_created} days old)", inline=True)

    embed1.set_image(url=pfp)

    embed2 = Embed()
    embed2.title = f"{name}'s Stats"
    embed2.set_footer(text=f"Triggered by {triggered_by}")

    embed2.add_field(name="Num Gifs", value=gif_stats.num_gifs, inline=True)
    embed2.add_field(name="S tiers", value=gif_stats.num_s, inline=True)
    embed2.add_field(name="A tiers", value=gif_stats.num_a, inline=True)
    embed2.add_field(name="B tiers", value=gif_stats.num_b, inline=True)
    embed2.add_field(name="C tiers", value=gif_stats.num_c, inline=True)
    embed2.add_field(name="Can add gif", value="Coming Soon...", inline=True)

    # if is_local:
    #     embed1.url = f"http://localhost:8080/user/{user_info['username']}"
    #     embed1.add_field(name="URL", value=f"http://localhost:8080/user/{user_info['username']}", inline=True)
    # else:
    #     embed1.url = f"https://bernardson.onrender.com/user/{user_info['username']}"
    #     embed1.add_field(name="URL", value=f"https://bernardson.onrender.com/user/{user_info['username']}", inline=True)

    return [embed1, embed2]

    # async def select_gif(self, ctx, gifs):
    #     user_info = get_user_info(ctx.author.id)
    #
    #     gif = get_gif_from_gif_id(gifs[0][2])
    #     gif['new_obtain_date'] = gifs[0][1]
    #     gif['old_obtain_date'] = gifs[-1][1]
    #     gif['id'] = gifs[0][2]
    #
    #     # do a check to see if already in user_favorites
    #     if check_gif_in_fav(gif['id'], user_info['user_id']):
    #         return False
    #
    #     embeds = self.make_fav_embed(gif, user_info['username'], True)
    #
    #     message = await ctx.send(embeds=embeds)
    #
    #     if await self.are_you_sure(ctx, message) == "✅":
    #         return gif
    #     else:
    #         return None

    #
    #
    # def make_fav_embed(self, gif, username, is_add):
    #     if is_add:
    #         est = ZoneInfo("US/Eastern")
    #         recent_date_time = gif['new_obtain_date'].astimezone(est)
    #         oldest_date_time = gif['old_obtain_date'].astimezone(est)
    #         new_date_readable = recent_date_time.strftime('%B %-d, %Y at %-I:%M %p')
    #         old_date_readable = oldest_date_time.strftime('%B %-d, %Y at %-I:%M %p')
    #
    #         embed1 = Embed()
    #         embed1.title = f"{username} is favoriting..."
    #         if gif['tier'] == 'S':
    #             embed1.color = 0xFFD700
    #         elif gif['tier'] == 'A':
    #             embed1.color = 0x7F00FF
    #         elif gif['tier'] == 'B':
    #             embed1.color = 0x00CC66
    #         elif gif['tier'] == 'C':
    #             embed1.color = 0x000099
    #
    #         embed1.add_field(name="Tier", value=gif['tier'])
    #         embed1.add_field(name="GIF ID", value=gif['id'])
    #         if gif['new_obtain_date'] == gif['old_obtain_date']:
    #             embed1.add_field(name="Date Rolled", value=new_date_readable)
    #         else:
    #             embed1.add_field(name="Oldest Date Rolled", value=old_date_readable)
    #             embed1.add_field(name="Newest Date Rolled", value=new_date_readable)
    #         embed1.set_image(url=gif['url'])
    #
    #         embed2 = Embed()
    #         embed2.color = embed1.color
    #         embed2.title = f"Please Confirm adding to Favorites"
    #         embed2.description = f"Use the ✅(confirms fav), ❌(Cancels)."
    #
    #         return [embed1, embed2]
    #     else:
    #         est = ZoneInfo("US/Eastern")
    #         date_time = gif['favorited_at'].astimezone(est)
    #         date_readable = date_time.strftime('%B %-d, %Y at %-I:%M %p')
    #
    #         embed1 = Embed()
    #         embed1.title = f"{username} is UNfavoriting..."
    #         if gif['tier'] == 'S':
    #             embed1.color = 0xFFD700
    #         elif gif['tier'] == 'A':
    #             embed1.color = 0x7F00FF
    #         elif gif['tier'] == 'B':
    #             embed1.color = 0x00CC66
    #         elif gif['tier'] == 'C':
    #             embed1.color = 0x000099
    #
    #         embed1.add_field(name="Tier", value=gif['tier'])
    #         embed1.add_field(name="GIF ID", value=gif['id'])
    #         embed1.add_field(name="Favorited Date", value=date_readable)
    #         embed1.set_image(url=gif['url'])
    #
    #         embed2 = Embed()
    #         embed2.color = embed1.color
    #         embed2.title = f"Please Confirm REMOVING FROM Favorites"
    #         embed2.description = f"Use the ✅(confirms REMOVAL), ❌(Cancels)."
    #
    #         return [embed1, embed2]
    #
    # async def are_you_sure(self, ctx, message):
    #     await asyncio.gather(
    #         message.add_reaction("✅"),
    #         message.add_reaction("❌"),
    #     )
    #
    #     def check(reaction, user):
    #         return (
    #             user == ctx.author and
    #             reaction.message.id == message.id and
    #             str(reaction.emoji) in ["✅", "❌"]
    #         )
    #
    #     # this can be different, turned to while
    #     try:
    #         reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30.0)
    #
    #     except asyncio.TimeoutError:
    #         await ctx.send("Longer than 30 second response")
    #         return None
class RevealView(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=90)
        self.author_id = author_id
        self.skipped = asyncio.Event()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("This isn't your pull.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.skipped.set()
        await interaction.response.defer()

    async def wait_or_skip(self, seconds: float) -> None:
        """Sleep for `seconds`, but wake up early if Skip was clicked."""
        try:
            await asyncio.wait_for(self.skipped.wait(), timeout=seconds)
        except asyncio.TimeoutError:
            pass

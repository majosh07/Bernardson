from typing import Optional
from discord import Embed, Member
from discord.ext import commands
from datetime import datetime, timezone

from db.gacha import GachaRepo
from db.models import DailyResult, RollResult, UserStatsResult
from gacha.utils import get_display_name
import time



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

    @commands.command(aliases=['test'])
    async def testing(self, ctx):
        await ctx.send("Hello world")

    @commands.command(aliases=['d', 'b', 'askbofday', 'askboftheday',])
    async def the_day(self, ctx):
        info: DailyResult = await self.repo.daily_gif(user_id=ctx.author.id)
        
        name = await get_display_name(self.bot, ctx.guild, info.reveal.triggered_by)
        embed = self.make_daily_embed(info, name)

        await ctx.send(embed=embed)


    @commands.command(aliases=['r', 'roll'])
    async def the_roll(self, ctx):
        # gif: tier, id, media_url
        # user_info: roll_count, username(passed from ctx.author)
        # know if we hit pity
        try:
            roll: RollResult | None = await self.repo.roll(user_id=ctx.author.id)
        except ValueError:
            await ctx.send("You don't have any rolls left ...")
            return

        name = await get_display_name(self.bot, ctx.guild, ctx.author.id)
        embed = self.make_rolled_embed(roll, name)

        await ctx.send(embed=embed)

    @commands.command(aliases=['s',])
    async def stats(self, ctx, member: Optional[Member] = None):
        member = member or ctx.author
        try:
            stats = await self.repo.user_stats(member.id)
        except ValueError:
            await ctx.send("User is not in the database...")
            return
        except Exception as e:
            await ctx.send("Something went wrong...")
            raise e
        
        stats_name = await get_display_name(self.bot, ctx.guild, stats.user_info.user_id)
        triggered_by = await get_display_name(self.bot, ctx.guild, ctx.author.id)
        pfp = member.display_avatar.url

        embeds = self.make_stats_embeds(stats, stats_name, pfp, triggered_by)
        await ctx.send(embeds=embeds)

    # @commands.command(aliases=['s',])
    # async def stats(self, ctx, member: Optional[Member] = None):
    #     member = member or ctx.author
    #
    #     try:
    #         user_info = get_user_info(member.id)
    #         if not isinstance(user_info, dict):
    #             raise ValueError("user_info is not dict")
    #
    #         user_info["num_gifs"] = get_num_gifs(member)
    #         user_info['num_S'] = get_num_tier_gifs(member, 'S')
    #         user_info['num_A'] = get_num_tier_gifs(member, 'A')
    #         user_info['num_B'] = get_num_tier_gifs(member, 'B')
    #         user_info['num_C'] = get_num_tier_gifs(member, 'C')
    #
    #         user_info['pfp'] = member.display_avatar.url
    #
    #         is_local = ctx.prefix == "!"
    #
    #         embeds = self.make_stats_embeds(user_info, ctx.author.name, is_local)
    #
    #         await ctx.send(embeds=embeds)
    #     except ValueError as e:
    #         await ctx.send("User is not in the database...")
    #     except Exception as e:
    #         await ctx.send("Something went wrong...")
    #         print("Stats general error:", e)
    #
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
    def make_daily_embed(self, info: DailyResult, name: str):
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

    def make_rolled_embed(self, roll: RollResult, name):
        gif = roll.gif
        embed = Embed()
        if gif.tier == 'S':
            embed.color = 0xFFD700
            embed.title = f"{name} just rolled a !!!"
        elif gif.tier == 'A':
            embed.color = 0x7F00FF
            embed.title = f"{name} just rolled a ..!"
        elif gif.tier == 'B':
            embed.color = 0x00CC66
            embed.title = f"{name} just rolled a ..."
        elif gif.tier == 'C':
            embed.color = 0x000099
            embed.title = f"{name} just rolled a ..."


        embed.add_field(name="Tier", value=gif.tier)
        embed.add_field(name="GIF ID", value=gif.id)
        embed.add_field(name="Num Rolls Left", value=str(roll.num_rolls_left))
        if roll.used_pity:
            embed.add_field(name="HARD PITY", value="HIT HARD PITY")
        embed.set_footer(text=f"For {name}")
        embed.set_image(url=gif.media_url)

        return embed

    def make_stats_embeds(self, stats: UserStatsResult, name: str, pfp: str, triggered_by: str):
        user_info = stats.user_info
        gif_stats = stats.gif_stats

        days_since_created = int((time.time() - user_info.created_at) / SECONDS_IN_A_DAY)

        # user created time, compare to now
        # name, could just use the get name
        # roll_count, streak, pities, 
        # Triggered by author

        # user_gifs, number of gifs
        # number of S, A, B, C


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
    #
    #
    #
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
    #


import asyncio
from typing import Optional
from discord import Embed, Member
from discord.ext import commands
from gacha.database import *
from gacha.gacha_probabilities import *
import random
from datetime import datetime
from zoneinfo import ZoneInfo
from dateutil.relativedelta import relativedelta
from logging_config import logger

GACHA_CHANNEL_ID = 1129160056387153990
TESTING_CHANNEL_ID = 1136423792822997002

class Gacha(commands.Cog):
    def __init__(self, bot, args) -> None:
        self.bot = bot
        self.args = args

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
        user_info = ctx.author
        if ctx.prefix == ";;" and ctx.channel.id != GACHA_CHANNEL_ID and ctx.channel.id != TESTING_CHANNEL_ID:

            return False
        await check_add_user(user_info)
        return True



    @commands.command(aliases=['d', 'b', 'askbofday', 'askboftheday',])
    async def the_day(self, ctx):
        # add logging that user is doing askbofday
        logger.info(f"{ctx.author.name} is doing daily...")
        today_gif, is_new = await get_daily_gif(ctx.author)

        user_info = await get_user_info(ctx.author.id)
        prev_roll_count = user_info['roll_count']
        prev_daily_streak = user_info['daily_streak']

        daily_streak, was_bonus = await check_add_daily_streak(ctx.author, self.args.admin_streak)

        roll_count = await check_add_roll(ctx.author, was_bonus, self.args.admin_daily)

        await set_last_status()

        logger.info(f"{ctx.author.name}'s RollCount: {roll_count}")
        info = {
            "today_gif": today_gif,
            "is_new": is_new,
            "roll_count": roll_count,
            "prev_roll_count": prev_roll_count,
            "daily_streak": daily_streak,
            "prev_daily_streak": prev_daily_streak,
            "was_bonus": was_bonus,
        }
        logger.info("going into daily_embed")
        embed = await self.make_daily_embed(**info)

        await ctx.send(embed=embed)

    @commands.command(aliases=['r', 'roll'])
    async def the_roll(self, ctx):
        logger.info(f"{ctx.author.name} is rolling")
        user_info = await get_user_info(ctx.author.id)

        if user_info['roll_count'] == 0:
            await ctx.send("You don't have any rolls left ...")
            return

        user_info['roll_count'] = await subtract_roll(user_info)

        user_info['s_pity'], user_info['a_pity'] = await add_pities(user_info)

        chosen_tier, hit_pity = self.choose_tier(user_info)

        chosen_gif = await get_rand_gif_with_tier(chosen_tier)

        await reset_pities(user_info, chosen_tier)

        await add_user_gif(user_info, chosen_gif)

        embed = self.make_rolled_embed(chosen_gif, user_info, hit_pity)

        await ctx.send(embed=embed)

    @commands.command(aliases=['s',])
    async def stats(self, ctx, member: Optional[Member] = None):
        member = member or ctx.author

        try:
            user_info = await get_user_info(member.id)
            if not isinstance(user_info, dict):
                raise ValueError("user_info is not dict")

            user_info["num_gifs"] = await get_num_gifs(member)
            user_info['num_S'] = await get_num_tier_gifs(member, 'S')
            user_info['num_A'] = await get_num_tier_gifs(member, 'A')
            user_info['num_B'] = await get_num_tier_gifs(member, 'B')
            user_info['num_C'] = await get_num_tier_gifs(member, 'C')

            user_info['pfp'] = member.display_avatar.url

            embeds = self.make_stats_embeds(user_info, ctx.author.name)

            await ctx.send(embeds=embeds)
        except ValueError as e:
            await ctx.send("User is not in the database...")
        except Exception as e:
            await ctx.send("Something went wrong...")
            print("Stats general error:", e)

    @commands.command(aliases=['f',])
    async def favorite(self, ctx, gif_id: Optional[str] = None):
        if gif_id is None:
            await ctx.send("Missing GIF_ID")
            return
        if not isinstance(gif_id, str) or not gif_id.isdigit():
            await ctx.send("Not a valid GIF_ID")
            return

        gif_id = int(gif_id) # pyright: ignore

        gifs = await find_user_gifs(gif_id, ctx.author)

        if gifs is None or not isinstance(gifs, list):
            await ctx.send("Couldn't Find GIF in Inventory(Are you sure you have it?)")
            return

        gif = await self.select_gif(ctx, gifs)

        if gif is None:
            await ctx.send("Cancelled Favorite...")
            return
        elif gif is False:
            await ctx.send("Already have GIF added")
            return

        await add_fav_gif(gif, ctx.author)
        await ctx.send(f"Added GIF ID: {gif['id']} to {ctx.author.name}'s favorites.")


    @commands.command(aliases=['uf',])
    async def unfavorite(self, ctx, gif_id: Optional[str] = None):
        if gif_id is None:
            await ctx.send("Missing GIF_ID")
            return
        if not isinstance(gif_id, str) or not gif_id.isdigit():
            await ctx.send("Not a valid GIF_ID")
            return

        gif_id = int(gif_id) # pyright: ignore

        gif = await check_gif_in_fav(gif_id, ctx.author.id)

        if gif is None:
            await ctx.send(f"GIF ID: {gif_id} is not in your favorites...")
            return

        other_gif_info = await get_gif_from_gif_id(gif_id)
        gif['tier'] = other_gif_info['tier']
        gif['url'] = other_gif_info['url']
        gif['id'] = gif_id

        embeds = self.make_fav_embed(gif, ctx.author.name, False)

        message = await ctx.send(embeds=embeds)

        if await self.are_you_sure(ctx, message) == "✅":
            await remove_fav_gif(gif_id, ctx.author.id)
            await ctx.send(f"Removed GIF ID: {gif_id} from {ctx.author.name}'s favorites")
        else:
            await ctx.send(f"Cancelled unfavorite...")
        



    # today_gif, is_new, roll_count, roll_count, prev_roll_count, daily_streak, prev_daily_streak, was_bonus
    async def make_daily_embed(self, **info):
        embed = None

        logger.info(info)

        if info['is_new']:
            embed = Embed(
                title="New Daily GIF!",
                color=0xFF0000,
            )
        else:
            embed = Embed(
                title="Daily GIF",
                color=0x0000FF,
            )
        if type(info['today_gif']) is not dict:
            print(type(info['today_gif']))
            raise ValueError("this should be a Dict")

        gif_info = await get_gif_from_gif_id(info['today_gif']['gif_id'])

        est = ZoneInfo("US/Eastern")
        date_time = info['today_gif']['created_at'].astimezone(est)
        date_readable = date_time.strftime('%I:%M %p')

        num_rolls = str(info['roll_count']) if info['prev_roll_count'] == info['roll_count'] else f"({info['prev_roll_count']}) -> **{info['roll_count']}**"
        daily_streak = str(info['daily_streak']) if info['prev_daily_streak'] == info['daily_streak'] else f"({info['prev_daily_streak']}) -> **{info['daily_streak']}**"

        embed.add_field(name="Tier", value=gif_info['tier'])
        if info['was_bonus']:
            embed.add_field(name="Daily Streak!!!", value=daily_streak)
            embed.add_field(name="Num Rolls", value=f"{num_rolls}!!!")
        else:
            embed.add_field(name="Daily Streak", value=daily_streak)
            embed.add_field(name="Num Rolls", value=num_rolls)
        embed.set_footer(text=f"Chosen by: {info['today_gif']['author']} at {date_readable}")
        embed.set_image(url=info['today_gif']['url'])

        return embed

    def make_rolled_embed(self, gif, user_info, hit_pity):
        embed = Embed()
        if gif['tier'] == 'S':
            embed.color = 0xFFD700
            embed.title = f"{user_info['username']} just rolled a !!!"
        elif gif['tier'] == 'A':
            embed.color = 0x7F00FF
            embed.title = f"{user_info['username']} just rolled a ..!"
        elif gif['tier'] == 'B':
            embed.color = 0x00CC66
            embed.title = f"{user_info['username']} just rolled a ..."
        elif gif['tier'] == 'C':
            embed.color = 0x000099
            embed.title = f"{user_info['username']} just rolled a ..."


        embed.add_field(name="Tier", value=gif['tier'])
        embed.add_field(name="GIF ID", value=gif['id'])
        embed.add_field(name="Num Rolls Left", value=str(user_info['roll_count']))
        if hit_pity:
            embed.add_field(name="HARD PITY", value="HIT HARD PITY")
        embed.set_footer(text=f"For {user_info['username']}")
        embed.set_image(url=gif['url'])

        return embed
    
    def make_stats_embeds(self, user_info, author):
        est = ZoneInfo("US/Eastern")
        date_time = user_info['created_at'].astimezone(est)
        date_readable = date_time.strftime('%B %-d, %Y')

        now = datetime.now(est)
        age = relativedelta(now, date_time)

        embed1 = Embed()
        embed1.title = "Info"

        embed1.add_field(name="Num Rolls", value=user_info['roll_count'], inline=True)
        embed1.add_field(name="Daily Streak", value=user_info['daily_streak'], inline=True)
        embed1.add_field(name="URL", value="Coming soon...", inline=True)
        embed1.add_field(name="S Pity", value=user_info['s_pity'], inline=True)
        embed1.add_field(name="A Pity", value=user_info['a_pity'], inline=True)
        embed1.add_field(name="Created Account", value=f"{date_readable}\n({age.days} days old)", inline=True)
        embed1.set_footer(text=f"For {author}")

        embed1.set_image(url=user_info['pfp'])

        embed2 = Embed()
        embed2.title = "Stats"

        embed2.set_footer(text=f"For {author}")

        embed2.add_field(name="Num Gifs", value=user_info['num_gifs'], inline=True)
        embed2.add_field(name="S tiers", value=user_info['num_S'], inline=True)
        embed2.add_field(name="A tiers", value=user_info['num_A'], inline=True)
        embed2.add_field(name="B tiers", value=user_info['num_B'], inline=True)
        embed2.add_field(name="C tiers", value=user_info['num_C'], inline=True)
        embed2.add_field(name="Can add gif", value="Coming Soon...", inline=True)

        return [embed1, embed2]

    def choose_tier(self, user_info):
        s_pity = user_info['s_pity']
        a_pity = user_info['a_pity']

        if s_pity >= S_HARD_PITY:
            logger.info(f"{user_info['username']} hit S hard pity")
            return 'S', True
        if a_pity >= A_HARD_PITY:
            logger.info(f"{user_info['username']} hit A hard pity")
            return 'A', True

        probabilities = self.get_probabilities(BASE_PROBABILITIES, s_pity, a_pity)
        tiers = list(probabilities.keys())
        weights = list(probabilities.values())

        return random.choices(tiers, weights=weights, k=1)[0], False

    def get_probabilities(self, probabilities, s_pity, a_pity):
        probs = probabilities
        s_chance = probs['S']
        a_chance = probs['A']
        if s_pity >= S_SOFT_PITY_START:
            s_chance = S_SLOPE * s_chance + S_INTERCEPT
        if a_pity >= A_SOFT_PITY_START:
            a_chance = A_SLOPE * a_chance + S_INTERCEPT
        rest_of_chance = 1 - (s_chance + a_chance)

        probs['S'] = s_chance
        probs['A'] = a_chance
        total_base = probs['B'] + probs['C']
        probs['B'] = rest_of_chance * (probs['B'] / total_base)
        probs['C'] = rest_of_chance * (probs['C'] / total_base)

        return probs


    async def select_gif(self, ctx, gifs):
        user_info = await get_user_info(ctx.author.id)

        gif = await get_gif_from_gif_id(gifs[0][2])
        for thing in gifs:
            logger.info(thing[1])
        gif['new_obtain_date'] = gifs[0][1]
        gif['old_obtain_date'] = gifs[-1][1]
        gif['id'] = gifs[0][2]

        # do a check to see if already in user_favorites
        if await check_gif_in_fav(gif['id'], user_info['user_id']):
            return False

        embeds = self.make_fav_embed(gif, user_info['username'], True)

        message = await ctx.send(embeds=embeds)

        if await self.are_you_sure(ctx, message) == "✅":
            return gif
        else:
            return None



    def make_fav_embed(self, gif, username, is_add):
        if is_add:
            est = ZoneInfo("US/Eastern")
            recent_date_time = gif['new_obtain_date'].astimezone(est)
            oldest_date_time = gif['old_obtain_date'].astimezone(est)
            new_date_readable = recent_date_time.strftime('%B %-d, %Y at %-I:%M %p')
            old_date_readable = oldest_date_time.strftime('%B %-d, %Y at %-I:%M %p')

            embed1 = Embed()
            embed1.title = f"{username} is favoriting..."
            if gif['tier'] == 'S':
                embed1.color = 0xFFD700
            elif gif['tier'] == 'A':
                embed1.color = 0x7F00FF
            elif gif['tier'] == 'B':
                embed1.color = 0x00CC66
            elif gif['tier'] == 'C':
                embed1.color = 0x000099

            embed1.add_field(name="Tier", value=gif['tier'])
            embed1.add_field(name="GIF ID", value=gif['id'])
            if gif['new_obtain_date'] == gif['old_obtain_date']:
                embed1.add_field(name="Date Rolled", value=new_date_readable)
            else:
                embed1.add_field(name="Oldest Date Rolled", value=old_date_readable)
                embed1.add_field(name="Newest Date Rolled", value=new_date_readable)
            embed1.set_image(url=gif['url'])

            embed2 = Embed()
            embed2.color = embed1.color
            embed2.title = f"Please Confirm adding to Favorites"
            embed2.description = f"Use the ✅(confirms fav), ❌(Cancels)."

            return [embed1, embed2]
        else:
            est = ZoneInfo("US/Eastern")
            date_time = gif['favorited_at'].astimezone(est)
            date_readable = date_time.strftime('%B %-d, %Y at %-I:%M %p')

            embed1 = Embed()
            embed1.title = f"{username} is UNfavoriting..."
            if gif['tier'] == 'S':
                embed1.color = 0xFFD700
            elif gif['tier'] == 'A':
                embed1.color = 0x7F00FF
            elif gif['tier'] == 'B':
                embed1.color = 0x00CC66
            elif gif['tier'] == 'C':
                embed1.color = 0x000099

            embed1.add_field(name="Tier", value=gif['tier'])
            embed1.add_field(name="GIF ID", value=gif['id'])
            embed1.add_field(name="Favorited Date", value=date_readable)
            embed1.set_image(url=gif['url'])

            embed2 = Embed()
            embed2.color = embed1.color
            embed2.title = f"Please Confirm REMOVING FROM Favorites"
            embed2.description = f"Use the ✅(confirms REMOVAL), ❌(Cancels)."

            return [embed1, embed2]

    async def are_you_sure(self, ctx, message):
        await asyncio.gather(
            message.add_reaction("✅"),
            message.add_reaction("❌"),
        )

        def check(reaction, user):
            return (
                user == ctx.author and
                reaction.message.id == message.id and
                str(reaction.emoji) in ["✅", "❌"]
            )

        # this can be different, turned to while
        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30.0)

        except asyncio.TimeoutError:
            await ctx.send("Longer than 30 second response")
            return None

        return reaction.emoji

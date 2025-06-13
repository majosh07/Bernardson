from typing import Optional
from discord import Embed, Member
from discord.ext import commands
from gacha.database import *
from gacha.gacha_probabilities import *
import random
from zoneinfo import ZoneInfo
from logging_config import logger


class Gacha(commands.Cog):
    def __init__(self, bot, args) -> None:
        self.bot = bot
        bot.add_check(self.check_add_register_user)
        self.args = args

    async def check_add_register_user(self, ctx):
        user_info = ctx.author
        await check_add_user(user_info)
        return True

    @commands.command(aliases=['d', 'b', 'askbofday', 'askboftheday',])
    async def the_day(self, ctx):
        # add logging that user is doing askbofday
        logger.info(f"{ctx.author.name} is doing daily...")
        today_gif, is_new = await get_daily_gif(ctx.author)

        user_info = await get_user_info(ctx.author.id)
        prev_roll_count = user_info['roll_count']

        roll_count = await check_add_roll(ctx.author, self.args.admin)

        await set_last_status()

        logger.info(f"Today gif: {today_gif}\nRollCount: {roll_count}")
        embed = await self.make_daily_embed(today_gif, is_new, roll_count, prev_roll_count)

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

        embed = self.make_rolled_embed(chosen_gif, user_info, hit_pity)

        await add_user_gif(user_info, chosen_gif)

        await ctx.send(embed=embed)

    @commands.command(aliases=['s',])
    async def stats(self, ctx, member: Optional[Member] = None):
        member = member or ctx.author

        try:
            user_info = await get_user_info(member.id)
            if not isinstance(user_info, dict):
                raise ValueError("user_info is not dict")

            logger.info("num_gifs")
            user_info["num_gifs"] = await get_num_gifs(member)
            logger.info("num_s")
            user_info['num_S'] = await get_num_tier_gifs(member, 'S')
            logger.info("num_a")
            user_info['num_A'] = await get_num_tier_gifs(member, 'A')
            user_info['num_B'] = await get_num_tier_gifs(member, 'B')
            user_info['num_C'] = await get_num_tier_gifs(member, 'C')

            logger.info("pfp")
            user_info['pfp'] = member.display_avatar.url

            embeds = self.make_stats_embeds(user_info, ctx.author.name)

            await ctx.send(embeds=embeds)
        except ValueError as e:
            await ctx.send("User is not in the database...")
        except Exception as e:
            await ctx.send("Something went wrong...")
            print("Stats general error:", e)


    @commands.command()
    async def askb(self, ctx, *, phrase:Optional[str]=None):
        logger.info('ASKING B')
        answers = [
            "It is certain.",
            "Without a doubt.",
            "Yes, definitely.",
            "My sources say yes.",
            "Yes.",
            "Ask again later.",
            "Cannot tell right now.",
            "Concentrate and ask again.",
            "My reply is no.",
            "No.",
            "My sources say no.",
        ]
        if (phrase == "is this true?"):
            await ctx.send(random.choice(answers))
        else:
            await ctx.send("Send the command ';;askb is this true?' exactly.")

    @commands.command()
    async def exit(self, ctx):
        if ctx.author.id == OWNER_ID:
            await ctx.send("Stopping bot...")
            await self.bot.shutdown()


    async def make_daily_embed(self, today_gif, is_new, roll_count, prev_roll_count):
        embed = None

        if is_new:
            embed = Embed(
                title="New Daily GIF!",
                color=0xFF0000,
            )
        else:
            embed = Embed(
                title="Daily GIF",
                color=0x0000FF,
            )
        if type(today_gif) is not dict:
            print(type(today_gif))
            raise ValueError("this should be a Dict")

        gif_info = await get_gif_from_gif_id(today_gif['gif_id'])

        est = ZoneInfo("US/Eastern")
        date_time = today_gif['created_at'].astimezone(est)
        date_readable = date_time.strftime('%I:%M %p')

        num_rolls = str(roll_count) if prev_roll_count == roll_count else f"({prev_roll_count}) -> **{roll_count}**"

        embed.add_field(name="Tier", value=gif_info['tier'])
        embed.add_field(name="Num Rolls", value=num_rolls)
        embed.set_footer(text=f"Chosen by: {today_gif['author']} at {date_readable}")
        embed.set_image(url=today_gif['url'])

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
        embed.add_field(name="Num Rolls Left", value=str(user_info['roll_count']))
        if hit_pity:
            embed.add_field(name="HARD PITY", value="HIT HARD PITY")
        embed.set_footer(text=f"For {user_info['username']}")
        embed.set_image(url=gif['url'])

        return embed
    
    def make_stats_embeds(self, user_info, author):
        embed1 = Embed()
        embed1.title = "Info"

        embed1.add_field(name="Num Rolls", value=user_info['roll_count'], inline=True)
        embed1.add_field(name="S Pity", value=user_info['s_pity'], inline=True)
        embed1.add_field(name="A Pity", value=user_info['a_pity'], inline=True)
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
        embed2.add_field(name="Roll Streak", value="Coming Soon...", inline=True)
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








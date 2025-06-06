from typing import Optional
from discord import Embed
from discord.ext import commands
from database import Database
from gacha_probabilities import *
from database import OWNER_ID
import sys
import random


class Gacha(commands.Cog):
    def __init__(self, bot, db : Database, args) -> None:
        self.bot = bot
        bot.add_check(self.check_add_register_user)
        self.db = db
        self.num_gifs = db.get_num_gifs()
        self.args = args

    async def check_add_register_user(self, ctx):
        user_info = ctx.author
        self.db.check_add_user(user_info)
        return True

    @commands.command(aliases=['d', 'b', 'askbofday', 'askboftheday',])
    async def the_day(self, ctx):
        # add logging that user is doing askbofday
        today_gif, is_new = self.db.get_daily_gif(ctx.author)
        
        roll_count = self.db.check_add_roll(ctx.author, self.args.admin)

        embed = self.make_daily_embed(today_gif, is_new, roll_count)

        self.db.set_last_status()

        await ctx.send(embed=embed)

    @commands.command(aliases=['r', 'roll'])
    async def the_roll(self, ctx):
        user_info = self.db.get_user_info(ctx.author.id)

        if user_info['roll_count'] == 0:
            await ctx.send("You don't have any rolls left ...")
            return

        user_info['roll_count'] = self.db.subtract_roll(user_info)

        chosen_tier = self.choose_tier(user_info)
        
        chosen_gif = self.db.get_rand_gif_with_tier(chosen_tier)

        self.db.reset_pities(user_info, chosen_tier)

        embed = self.make_rolled_embed(chosen_gif, user_info)

        self.db.add_user_gif(user_info, chosen_gif)

        await ctx.send(embed=embed)

    @commands.command()
    async def askb(self, ctx, *, phrase:Optional[str]=None):
        answers = [
            "It is certain.",
            "Without a doubt.",
            "Yes, definitely.",
            "My sources say yes.",
            "Yes",
            "Ask again later.",
            "Cannot tell right now.",
            "Concentrate and ask again",
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
            sys.exit(0)

    def make_daily_embed(self, today_gif, is_new, roll_count):
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

        gif_info = self.db.get_gif_from_gif_id(today_gif['gif_id'])
        embed.add_field(name="Tier", value=gif_info['tier'])
        embed.add_field(name="Num Rolls", value=str(roll_count))
        embed.set_footer(text=f"Chosen by: {today_gif['author']}")
        embed.set_image(url=today_gif['url'])

        return embed

    def make_rolled_embed(self, gif, user_info):
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
        embed.set_footer(text=f"For {user_info['username']}")
        embed.set_image(url=gif['url'])

        return embed

    def choose_tier(self, user_info):
        s_pity = user_info['s_pity']
        a_pity = user_info['a_pity']

        if s_pity >= S_HARD_PITY:
            return 'S'
        if a_pity >= A_HARD_PITY:
            return 'A'

        probabilities = self.get_probabilities(BASE_PROBABILITIES, s_pity, a_pity)
        tiers = list(probabilities.keys())
        weights = list(probabilities.values())

        return random.choices(tiers, weights=weights, k=1)[0]
        

    def get_probabilities(self, probabilities, s_pity, a_pity):
        s_chance = probabilities['S']
        a_chance = probabilities['A']
        if s_pity >= S_SOFT_PITY_START:
            s_chance = S_SLOPE * s_chance + S_INTERCEPT
        if a_pity >= A_SOFT_PITY_START:
            a_chance = A_SLOPE * a_chance + S_INTERCEPT
        rest_of_chance = 1 - (s_chance + a_chance)

        probabilities['S'] = s_chance
        probabilities['A'] = a_chance
        total_base = probabilities['B'] + probabilities['C']
        probabilities['B'] = rest_of_chance * (probabilities['B'] / total_base)
        probabilities['C'] = rest_of_chance * (probabilities['C'] / total_base)

        return probabilities
    

        



# NEED TO HAVE SOMETHING THAT HAS THE NAME OF THE USER(add this to db)
# AND NEED TO HAVE IT CHANGE based on server name?





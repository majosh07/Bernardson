from typing import Optional
from discord import Embed, Member
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
        self.args = args

    async def check_add_register_user(self, ctx):
        user_info = ctx.author
        await self.db.check_add_user(user_info)
        return True

    @commands.command(aliases=['d', 'b', 'askbofday', 'askboftheday',])
    async def the_day(self, ctx):
        # add logging that user is doing askbofday
        today_gif, is_new = await self.db.get_daily_gif(ctx.author)
        
        roll_count = await self.db.check_add_roll(ctx.author, self.args.admin)

        embed = await self.make_daily_embed(today_gif, is_new, roll_count)

        await self.db.set_last_status()

        await ctx.send(embed=embed)

    @commands.command(aliases=['r', 'roll'])
    async def the_roll(self, ctx):
        print(f"{ctx.author.name} is rolling")
        user_info = await self.db.get_user_info(ctx.author.id)

        if user_info['roll_count'] == 0:
            await ctx.send("You don't have any rolls left ...")
            return

        user_info['roll_count'] = await self.db.subtract_roll(user_info)

        user_info['s_pity'], user_info['a_pity'] = await self.db.add_pities(user_info)

        chosen_tier = self.choose_tier(user_info)
        
        chosen_gif = await self.db.get_rand_gif_with_tier(chosen_tier)

        await self.db.reset_pities(user_info, chosen_tier)

        embed = self.make_rolled_embed(chosen_gif, user_info)

        print(f"adding gif to users")
        await self.db.add_user_gif(user_info, chosen_gif)

        print(f"sending gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx, member: Optional[Member] = None):
        member = member or ctx.author

        try:
            user_info = self.db.get_user_info(member.id)

        except ValueError as e:
            await ctx.send("User is not in the database...")
            print("Stats ValueError:", e)
        except Exception as e:
            await ctx.send("Something went wrong...")
            print("Stats general error:", e)




    @commands.command()
    async def askb(self, ctx, *, phrase:Optional[str]=None):
        print('ASKING B')
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

            await self.db.close()

            await self.bot.close()

    async def make_daily_embed(self, today_gif, is_new, roll_count):
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

        gif_info = await self.db.get_gif_from_gif_id(today_gif['gif_id'])
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
    
    def make_stats_embed(self, user_info):
        embed = Embed()
        # num gifs that they have
            # number S tier
            # number A tier
        # rolls left
        # roll_streak (have to start keeping track of this)
        # can add gif(put "coming soon")
        # link to inventory("coming soon")


        return embed

    def choose_tier(self, user_info):
        s_pity = user_info['s_pity']
        a_pity = user_info['a_pity']

        if s_pity >= S_HARD_PITY:
            print(f"{user_info['username']} hit S hard pity")
            return 'S'
        if a_pity >= A_HARD_PITY:
            print(f"{user_info['username']} hit A hard pity")
            return 'A'

        probabilities = self.get_probabilities(BASE_PROBABILITIES, s_pity, a_pity)
        tiers = list(probabilities.keys())
        weights = list(probabilities.values())

        return random.choices(tiers, weights=weights, k=1)[0]
        

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
    









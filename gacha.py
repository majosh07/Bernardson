from discord import Embed
from discord.ext import commands
from database import Database
import random


class Gacha(commands.Cog):
    def __init__(self, bot, db : Database, args) -> None:
        self.bot = bot
        bot.add_check(self.check_add_register_user)
        self.db = db
        self.num_gifs = db.get_num_gifs()
        self.args = args
        self.probabilities = {'S': 0.1, 'A': 0.2, 'B': 0.3, 'C': 0.4}

    async def check_add_register_user(self, ctx):
        user_info = ctx.author
        self.db.check_add_user(user_info)
        return True

    @commands.command(aliases=['d', 'b', 'askbofday', 'askb'])
    async def the_day(self, ctx):
        today_gif, is_new = self.db.get_daily_gif(ctx.author)
        
        roll_count = self.db.check_add_roll(ctx.author, self.args.admin)

        embed = self.make_daily_embed(today_gif, is_new, roll_count)

        self.db.set_last_status()

        await ctx.send(embed=embed)

    @commands.command(aliases=['r', 'roll'])
    async def the_roll(self, ctx):
        tiers = list(self.probabilities.keys())
        weights = list(self.probabilities.values())
        chosen_tier = random.choices(tiers, weights=weights, k=1)[0]
        
        chosen_gif = self.db.get_rand_gif_with_tier(chosen_tier)
        user_info = self.db.get_user_info(ctx.author.id)

        embed = self.make_rolled_embed(chosen_gif, user_info)

        await ctx.send(embed=embed)

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

        



# NEED TO HAVE SOMETHING THAT HAS THE NAME OF THE USER(add this to db)
# AND NEED TO HAVE IT CHANGE based on server name?




# def roll(author):
#   # This will hold:
#   # the gif, if hit s pity, if hit a pity
#   roll_list = [False, False, False]
#   id_key = str(author.id)
#   tiers = ['S', 'A', 'B', 'C']
#   if members[id_key].S_pity >= 29:
#     rand_tier_value = "S"
#     plus_pity(id_key, rand_tier_value)
#     roll_list[1] = True
#   elif members[id_key].A_pity >= 9:
#     rand_tier_value = "A"
#     plus_pity(id_key, rand_tier_value)
#     roll_list[2] = True
#   else:
#     rand_tier_value = find_roll(tiers, members[id_key].A_pity, members[id_key].S_pity)
#     plus_pity(id_key, rand_tier_value)
#
#   roll_list[0] = GIF(tier_value = rand_tier_value)
#   members[id_key].add_gif(roll_list[0])
#   members[id_key].subtract_rolls()
#   with open("members.json", 'w') as output_file:
#     output_file.write(jsonpickle.encode(members, indent=0))
#   return roll_list
#
# def plus_pity(id_key, rand_tier_value):
#   if rand_tier_value == 'S':
#     members[id_key].S_pity = 0
#     members[id_key].A_pity += 1
#   elif rand_tier_value == 'A':
#     members[id_key].S_pity += 1
#     members[id_key].A_pity = 0
#   else:
#     members[id_key].S_pity += 1
#     members[id_key].A_pity += 1
#
# def find_roll(tiers, A_pity, S_pity):
#   S_SOFT_PITY = 25
#   A_SOFT_PITY = 8
#   # Just tested weights to get these numbers, tried to aim for
#   # 10% for S when you were at max
#   # 20% for A when you were at max
#
#   return linear_percentage_rolls(tiers, A_pity, S_pity)
#
#
#
# # Linear equations end right before guaranteed
# # So S_pity end is 29 and A_pity end 9
# # Having start be at 2% and end at 10% for S
# # Having start be at 10% and end at 20% for A
# def linear_percentage_rolls(tiers, A_pity, S_pity, S_SOFT_PITY = 25, A_SOFT_PITY = 8, S_start = .02, S_end = .1,
#                             A_start = .1, A_end = .2):
#   S_slope = (S_end * 100 - S_start * 100) / (29 - S_SOFT_PITY)
#   S_intercept = S_start * 100 - (S_slope * S_SOFT_PITY)
#   A_slope = (A_end * 100 - A_start * 100) / (9 - A_SOFT_PITY)
#   A_intercept = A_start * 100 - (A_slope * A_SOFT_PITY)
#
#
#   S_chance = .01
#   A_chance = .09
#   if S_pity >= S_SOFT_PITY and A_pity >= A_SOFT_PITY:
#     S_chance = (S_slope * S_pity + S_intercept) / 100
#     A_chance = (A_slope * A_pity + A_intercept) / 100
#   elif S_pity >= S_SOFT_PITY:
#     S_chance = (S_slope * S_pity + S_intercept) / 100
#   elif A_pity >= A_SOFT_PITY:
#     A_chance = (A_slope * A_pity + A_intercept) / 100
#   B_and_C_chance = (1 - (S_chance + A_chance)) / 2
#
#   return numpy.random.choice(tiers, p=[S_chance, A_chance, B_and_C_chance, B_and_C_chance])
#
# def append_favorite(author, id_num):
#   members[str(author.id)].favorites.append(GIF("C", id_num))
#   with open("members.json", 'w') as output_file:
#     output_file.write(jsonpickle.encode(members, indent=2))
#
#

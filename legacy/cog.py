from discord.ext import commands
import discord.utils


class Legacy(commands.Cog):
    def __init__(self, bot, args) -> None:
        self.bot = bot
        self.args = args

    @commands.command(aliases=['au', 'mogus', 'amogus', 'peensus', 'sus'])
    async def among_us(self, ctx):
        await ctx.send(
          "STOP POSTING ABOUT AMONG US! I'M TIRED OF SEEING IT! MY FRIENDS ON TIKTOK SEND ME MEMES, ON DISCORD IT'S FUCKING MEMES! I was in a server, right? and ALL OF THE CHANNELS were just among us stuff. I-I showed my champion underwear to my girlfriend and t-the logo I flipped it and I said \"hey babe, when the underwear is sus HAHA DING DING DING DING DING DING DING DI DI DING\" I fucking looked at a trashcan and said \"THAT'S A BIT SUSSY\" I looked at my penis I think of an astronauts helmet and I go \"PENIS? MORE LIKE PENSUS\" AAAAAAAAAAAAAAHGESFG"
        )


    @commands.command(aliases=['os'])
    async def OmegaStrikers(self, ctx):
        await ctx.send(
          'OMEGA STRIKERS. I LOVE OMEGA STRIKERS SO MUCH, PLEASE HELP; I AM ADDICTED TO OMEGA STRIKERS; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS OMEGA STRIKERS; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS OMEGA STRIKERS. Even when I go to sleep, it is just OMEGA STRIKERS. I imagine the strategies, characters, and plays; just thinking about it now makes me want to play it. OMG, MGMMGNGM, I NEED TO GET ON OMEGA STRIKERS RIGHT NOW. GOD I LOVE OMEGA STRIKERS SO MUCH ❤️'
        )


    @commands.command(aliases=['bl', 'bobble'])
    async def Bobble_League(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="Bubble")
        message = "BOBBLE LEAGUE. I LOVE BOBBLE LEAGUE SO MUCH, PLEASE HELP; I AM ADDICTED TO BOBBLE LEAGUE; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS BOBBLE LEAGUE; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS BOBBLE LEAGUE. Even when I go to sleep, it is just BOBBLE LEAGUE. I imagine the strategies, bounces, and plays; just thinking about it now makes me want to play it. OMG, MGMMGNGM, I NEED TO GET ON BOBBLE LEAGUE RIGHT NOW. GOD I LOVE BOBBLE LEAGUE SO MUCH ❤️"

        if role:
            await ctx.send(message + role.mention)
        else:
            await ctx.send(message)


    @commands.command(aliases=['bc', 'bing-chilling'])
    async def Bing_Chilling(self, ctx):
        await ctx.send(
          "Zǎoshang hǎo zhōngguó xiànzài wǒ yǒu BING CHILLING 🥶🍦 wǒ hěn xǐhuān BING CHILLING 🥶🍦 dànshì sùdù yǔ jīqíng 9 bǐ BING CHILLING 🥶🍦 sùdù yǔ jīqíng sùdù yǔ jīqíng 9 wǒ zuì xǐhuān suǒyǐ…xiànzài shì yīnyuè shíjiān zhǔnbèi 1 2 3 liǎng gè lǐbài yǐhòu sùdù yǔ jīqíng 9 ×3 bùyào wàngjì bùyào cu òguò jìdé qù diànyǐngyuàn kàn sùdù yǔ jīqíng 9 yīn wéi fēicháng hǎo diànyǐng dòngzuò fēicháng hǎo chàbùduō yīyàng BING CHILLING 🥶🍦zàijiàn 🥶🍦"
        )


    @commands.command(aliases=['lol'])
    async def League_Of_Legends(self, ctx):
        await ctx.send(
          "LEAGUE OF LEGENDS. I LOVE LEAGUE OF LEGENDS SO MUCH, PLEASE HELP; I AM ADDICTED TO LEAGUE OF LEGENDS; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS LEAGUE OF LEGENDS; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS LEAGUE OF LEGENDS. Even when I go to sleep, it is just LEAGUE OF LEGENDS. I imagine the champions, skills, and outplays; just thinking about it now makes me want to play it. OMG, MGMMGNGM, I NEED TO GET ON LEAGUE OF LEGENDS RIGHT NOW. GOD I LOVE LEAGUE OF LEGENDS SO MUCH"
        )


    @commands.command(aliases=['vl'])
    async def valorant(self, ctx):
        await ctx.send(
          "VALORANT. I LOVE VALORANT SO MUCH, PLEASE HELP; I AM ADDICTED TO VALORANT; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS VALORANT; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS VALORANT. Even when I go to sleep, it is just VALORANT. I imagine the line ups, clutches, and aces; just thinking about it now makes me want to play it. OMG, MGMMGNGM, I NEED TO GET ON VALORANT RIGHT NOW. GOD I LOVE VALORANT SO MUCH"
        )


    @commands.command(aliases=['rr'])
    async def RR(self, ctx, thing, *, number):
        if thing == 'pig':
          await ctx.send(
            f"┈┈┏━╮╭━┓┈╭━━━╮\n┈┈┃┏┗┛┓  ┃╭┫  {number}  ┃\n┈┈╰┓▋▋┏╯┈╰━━━╯\n┈╭━┻╮╲┗━━━━╮╭╮┈\n┈╰━┳┻▅╯╲╲╲╲┃┈┈┈\n┈┈┈╰━┳┓┏┳┓┏╯┈┈┈\n┈┈┈┈┈┗┻┛┗┻┛┈┈┈┈"
          )
        elif thing == 'truck':
          await ctx.send(
            f"""────────── ▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n───── ▄▄██▌█ BEEP BEEP\n▄▄▄▌▐██▌█ {number}\n███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n▀(⊙)▀▀▀▀▀▀▀(⊙)(⊙)▀▀▀▀▀▀▀▀▀▀(⊙""")
        else:
          await ctx.send("Send one of the valid RR commands, see ;;legacy")


    @commands.command(aliases=['op'])
    async def one_piece(self, ctx):
        await ctx.send(
          "ONE PIECE. I LOVE ONE PIECE SO MUCH, PLEASE HELP; I AM ADDICTED TO ONE PIECE; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS ONE PIECE; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS ONE PIECE. Even when I go to sleep, it is just ONE PIECE. Just thinking about it now makes me want to watch it. OMG, MGMMGNGM, I NEED TO WATCH ONE PIECE RIGHT NOW. GOD I LOVE ONE PIECE SO MUCH ❤️"
        )


    @commands.command(aliases=['omgg', 'OMGG'])
    async def oh_my_goodness_gracious(self, ctx, *, phrase):
        await ctx.send(
          f"**{phrase}**. I LOVE **{phrase}** SO MUCH, PLEASE HELP; I AM ADDICTED TO **{phrase}**; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS **{phrase}**; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS **{phrase}**. Even when I go to sleep, it is just **{phrase}**. I imagine the **{phrase}**, with **{phrase}**, and **{phrase}**; just thinking about it now makes me need it. OMG, MGMMGNGM, I NEED TO GET ON **{phrase}** RIGHT NOW. GOD I LOVE **{phrase}** SO MUCH ❤️"
        )


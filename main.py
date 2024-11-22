import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
import time
import math
from askb import askb_of_the_day, num_rolls, roll, append_favorite, members

oh_no = False
delay = 2

current_time = time.time()

TOKEN = os.environ['TOKEN']

intents = discord.Intents.all()
intents.messages = True

client = commands.Bot(command_prefix=';;', intents=intents)


@client.event
async def on_ready():
  print(f'{client.user.name} has connected to Discord.')


@client.command(aliases=['info', 'inform'])
async def information(ctx):
  await ctx.send(embed=make_information())


@client.command()
async def commands(ctx):
  await ctx.send(embed=askb_commands())


@client.command(aliases=['exinfo', 'einfo'])
async def extra_information(ctx):
  await ctx.send(embed=extra_info())


# @client.command(aliases = ['askb', 'Bernardson'])
# async def bernardson(ctx):
#   if time_okay():
#     global current_time
#     current_time = time.time()
#     message = get_rollkb()
#     await ctx.send(message)

import jsonpickle


@client.command(aliases=['d', 'b', 'askbofday', 'askb'])
async def the_day(ctx):
  if not time_okay():
    return

  global current_time
  current_time = time.time()
  author = ctx.author
  if str(author.id) in members:
    previous_rolls = num_rolls(author)
  message = askb_of_the_day(author)
  print(ctx.author)
  await ctx.send(message)
  if num_rolls(author) == 1:
    message = "You have 1 roll now!"
  else:
    message = f"You have {num_rolls(author)} rolls now!"
    if num_rolls(author) == previous_rolls + 2:
      message = f"**WOW Bonus Roll**\nYou have {num_rolls(author)} rolls now!"
  await ctx.send(message)


@client.command(aliases=['r', 'roll'])
async def the_roll(ctx):
  if time_okay():
    global current_time
    current_time = time.time()
    author = ctx.author
    if num_rolls(author) > 0:
      the_roll = roll(author)
      gif = the_roll[0]
      message = gif.gif
      await ctx.send(message)
      message = f"ID: {gif.id}"
      if gif.tier == 'A':
        if gif.id < 1304:
          message += "\nYou got an **A** tier Bernardson!" + f"\nYou have {num_rolls(author)} rolls left."
        else:
          message += "\nYou got an **A** tier **KHALED**!" + f"\nYou have {num_rolls(author)} rolls left."
      else:
        if gif.id < 1304:
          message += f"\nYou got a **{gif.tier}** tier Bernardson!" + f"\nYou have {num_rolls(author)} rolls left."
        else:
          message += f"\nYou got an **{gif.tier}** tier **KHALED**!" + f"\nYou have {num_rolls(author)} rolls left."
      if the_roll[1]:
        message += "\n**S PITY!!!**"
      if the_roll[2]:
        message += "\n**A PITY!!!**"
      if num_rolls(author) == 1:
        message.replace("rolls", "roll")
      await ctx.send(message)
    else:
      message = "You don't have any rolls to use..."
      await ctx.send(message)


# Format for message is ;;s (tier) (page number)
@client.command(aliases=['show', 's'])
async def show_all(ctx, *, message):
  if time_okay():
    global current_time
    current_time = time.time()
    author_id = str(ctx.author.id)
    gif_list = members[author_id].gifs

    if "ALL" in message.upper():
      real_tier = "ALL"
    else:
      real_tier = message.upper()[0]
      if not (message[0].upper() == "S" or message[0].upper() == "A"
              or message[0].upper() == "B" or message[0].upper() == "C"):
        await ctx.send("Missing Tier Value...\n(Either S, A, B, C)")
        return
      tier = message[0].upper()
      if not (any(char.isdigit() for char in message)):
        await ctx.send(
          "Missing Page Number...\n(Make sure you have that amount of pages, see ;;s all)"
        )

        # Possible that digit code doesn't work with the way people set things up
        # Just return False so don't have to think about it
        return
      digit_message = [char for char in message if char.isdigit()]
      digit_message = int("".join(digit_message))
      check_gif_list = [gif for gif in gif_list if gif.tier == real_tier]
      if math.ceil(len(check_gif_list) / 5) < digit_message:
        page_count = math.ceil(
          len([num for num in gif_list if num.tier == tier]) / 5)
        await ctx.send(
          f"The Page Number is too high\n(Total Page amount is {page_count}.)")
        return

    if real_tier == 'S' or real_tier == 'A' or real_tier == 'B' or real_tier == 'C':

      do_display = False
      for num in gif_list:
        if num.tier == real_tier:
          do_display = True

      if do_display:
        gif_list = [gif for gif in gif_list if gif.tier == real_tier]
        digit_message = [char for char in message if char.isdigit()]
        digit_message = int("".join(digit_message))

        display_list = gif_list[(digit_message - 1) * 5:digit_message * 5]

        await ctx.send(f"This is Page {digit_message}:")
        for gif in display_list:
          await ctx.send(gif.gif)
          if gif.number != 1:
            await ctx.send(f"ID: {gif.id}\nYou have {gif.number} copies")
          else:
            await ctx.send(f"ID: {gif.id}")

      #   if len(display_list) < 5 and len(display_list) > 0:
      #     display_list = display_list[:len(gif_list)]
      #     for gif in display_list:
      #       await ctx.send(gif.gif)
      #       if gif.number == 1:
      #         await ctx.send(f"You have {gif.number} copy")
      #       else:
      #         await ctx.send(f"You have {gif.number} copies")
      #   elif len(display_list) > 5:
      #     display_list = display_list[:5]
      #     for gif in display_list:
      #       await ctx.send(gif.gif)
      #       if gif.number == 1:
      #         await ctx.send(f"You have {gif.number} copy")
      #       else:
      #         await ctx.send(f"You have {gif.number} copies")
      #   else:
      #     await ctx.send("You don't have any of that Tier...")
      # else:
      #   await ctx.send("You don't have any of that Tier...")

      return

    elif real_tier == "ALL":
      tier_list = ["S", "A", "B", "C"]
      message = ""
      for tier in tier_list:
        count = 0
        for gif in gif_list:
          if tier == gif.tier:
            count += 1
        page_count = math.ceil(
          len([num for num in gif_list if num.tier == tier]) / 5)
        message += f"#{tier}: {count}(Pages: {page_count})\n"

      message += f"A Pity: {members[author_id].A_pity}\n"
      message += f"S Pity: {members[author_id].S_pity}\n"
      await ctx.send(message)

    else:
      await ctx.send('Please use either "S","A","B","C","ALL" at the end.')


@client.command(aliases=['f', 'fav'])
async def favorite(ctx, message):
  inventory = members[str(ctx.author.id)]
  if message[0].isdigit():
    digit_message = [char for char in message if char.isdigit()]
    digit_message = int("".join(digit_message))
    if digit_message <= len(inventory.favorites):
      gif = inventory.favorites[digit_message - 1]
      await ctx.send(gif.gif)
    else:
      await ctx.send("Not in your Favorites...")
  else:
    if "ALL" in message.upper():
      await ctx.send("Sending GIFs to DMs...")
      for gif in inventory.favorites:
        await ctx.author.send(f"#{gif.id}:")
        await ctx.author.send(gif.gif)
    else:
      await ctx.send('Need a Number ID or "ALL"...')


@client.command(aliases=['savfav'])
async def show_favorite(ctx, message):
  author = ctx.author
  if not message.isnumeric():
    await ctx.send(
      "Not an ID Number, use the show command to find the id number")
    return
  number = int(message)
  do_favorite = False
  for gif in members[str(author.id)].gifs:
    if number == gif.id:
      do_favorite = True

  if do_favorite:
    append_favorite(author, number)
    await ctx.send(
      f"Succesfully saved as #{len(members[str(author.id)].favorites)}")
  else:
    await ctx.send("You don't have that GIF...")


def askb_commands():
  embed = discord.Embed(
    color=discord.Color.darker_gray(),
    title="**COMMANDS**",
    description=
    "The parentheses() are information, [] are a part of the command")
  embed.set_footer(text='Made by jporh')
  embed.add_field(
    name="**(askboftheday)\n;;askb**",
    value="Gives you a random gif of the day\nAdds 1 Roll per new day")
  embed.add_field(
    name="**(roll)\n;;roll**",
    value=
    "Gives you either an S, A, B, or C tier Bernardson Gif and puts it into your inventory"
  )
  embed.add_field(
    name="**(Show your gifs)\n;;show [tier] [page]**",
    value="Shows you a page of 5 gifs of a certain tier of gifs that you own")
  embed.add_field(name="**(Save gifs to favorite)\n;;savfav [id number]**",
                  value="Saves a gif into your favorite list")
  embed.add_field(
    name="**(show favorite gifs)\n;;fav [number]**",
    value="Shows you a specific gif that you favorited(see ;;savfav)")
  embed.add_field(
    name="**;;exinfo**",
    value=
    "Gives you more information on each of the commands(Some of it is very useful)"
  )
  return embed


def extra_info():
  embed = discord.Embed(
    color=discord.Color.darker_gray(),
    title="**Extra Info**",
    description="More and examples for ;;d, ;;r, ;;s, ;;f, ;;savfav")
  embed.set_image(
    url="https://media.tenor.com/JEupJ2TM_0IAAAAd/askb-bernardson.gif")
  embed.set_footer(text='Made by jporh')
  embed.add_field(
    name="**(askboftheday)\n\;;d**",
    value=
    "Every 7 days gain 2 Rolls\n Ex: Have 6 Rolls and then ;;d, now have 8 Rolls"
  )
  embed.add_field(
    name="**(roll)\n\;;r**",
    value=
    "Chances for S-Tier are at base about 1% and for A-Tier about 9%\n You are guaranteed a S-Tier every 30 rolls and an A-Tier every 10 rolls"
  )
  embed.add_field(
    name="**(Show your gifs)\n\;;s**",
    value=
    "Ex: \;;s B 2(This would show you page 2 of your B-Tiers)\n Also you can do \;;s all to see more general stats"
  )
  embed.add_field(
    name="**(Save gifs to favorite)\n\;;savfav**",
    value=
    "Ex: ;;savfav 1001\nThis would save the 1st gif\n Can only save gifs that you have"
  )
  embed.add_field(
    name="**(show favorite gifs)\n\;;f**",
    value=
    "You can do \;;f all to see all of your favorite gifs that will be sent to your DMs"
  )
  return embed


def make_information():
  embed = discord.Embed(color=discord.Color.darker_gray())

  # embed.set_image(url = '')
  embed.set_footer(text='Bot made by jporh')
  embed.add_field(name="**DONT SPAM**",
                  value=f"THE BOT WILL ONLY SEND EVERY {delay} seconds",
                  inline=False)
  embed.add_field(
    name='**What is this?**',
    value=
    "This is the Bernardson Bot!\nIt houses a gacha system where you roll to get GIFs of the coolest guy around, Bernardson\nEach day you get one roll for typing in a command (;;b, ;;d, or ;;askb)\nThen you can use these to roll for GIFs with the ;;r command\nEach gif has its own ID number and tier (this is the letter S, A, B, C)",
    inline=False)
  embed.add_field(
    name='What to do Next:',
    value=
    'There is a list of other commands as well, like favoriting the gifs to help find and send them easier; Type ";;commands" to learn more',
    inline=False)
  return embed


def command_info():
  embed = discord.Embed(color=discord.Color.darker_gray())

  embed.set_footer(text='jporh')

  embed.add_field(name='****',
                  value=";;au(mogus, sus, peensus, amogus)",
                  inline=False)
  embed.add_field(
    name="**Bernardson**",
    value=
    ";;askb[gives you a random askb gif]\n ;;askbofday[random gif of the day]")
  embed.add_field(name='**Bobble League**', value=";;bl", inline=False)
  embed.add_field(name='**Bing Chilling**', value=";;bc", inline=False)
  embed.add_field(name='**LOL**', value=";;lol", inline=False)
  embed.add_field(name='**Nate Reed**', value=";;nr 1 \n ;;nr 2", inline=False)
  embed.add_field(name='**Omega Strikers**', value=";;os", inline=False)
  embed.add_field(name='**OMGG**',
                  value=';;omgg (text of the thing)',
                  inline=False)
  embed.add_field(name='**One Piece**', value=";;op", inline=False)
  embed.add_field(name='**-RR**',
                  value=";;rr (pig, truck) (number lost)\n ex: ;;rr pig 35",
                  inline=False)
  embed.add_field(name='**Valorant**', value=";;vl", inline=False)

  return embed


@client.command(aliases=['au', 'mogus', 'amogus', 'peensus', 'sus'])
async def among_us(ctx):
  if time_okay():
    global current_time
    current_time = time.time()
    await ctx.send(
      "STOP POSTING ABOUT AMONG US! I'M TIRED OF SEEING IT! MY FRIENDS ON TIKTOK SEND ME MEMES, ON DISCORD IT'S FUCKING MEMES! I was in a server, right? and ALL OF THE CHANNELS were just among us stuff. I-I showed my champion underwear to my girlfriend and t-the logo I flipped it and I said \"hey babe, when the underwear is sus HAHA DING DING DING DING DING DING DING DI DI DING\" I fucking looked at a trashcan and said \"THAT'S A BIT SUSSY\" I looked at my penis I think of an astronauts helmet and I go \"PENIS? MORE LIKE PENSUS\" AAAAAAAAAAAAAAHGESFG"
    )


@client.command(aliases=['os'])
async def OmegaStrikers(ctx):
  if time_okay():
    global current_time
    current_time = time.time()
    await ctx.send(
      'OMEGA STRIKERS. I LOVE OMEGA STRIKERS SO MUCH, PLEASE HELP; I AM ADDICTED TO OMEGA STRIKERS; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS OMEGA STRIKERS; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS OMEGA STRIKERS. Even when I go to sleep, it is just OMEGA STRIKERS. I imagine the strategies, characters, and plays; just thinking about it now makes me want to play it. OMG, MGMMGNGM, I NEED TO GET ON OMEGA STRIKERS RIGHT NOW. GOD I LOVE OMEGA STRIKERS SO MUCH ❤️'
    )


@client.command(aliases=['bl', 'bobble'])
async def Bobble_League(ctx):
  if time_okay():
    global current_time
    current_time = time.time()
    await ctx.send(
      "BOBBLE LEAGUE. I LOVE BOBBLE LEAGUE SO MUCH, PLEASE HELP; I AM ADDICTED TO BOBBLE LEAGUE; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS BOBBLE LEAGUE; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS BOBBLE LEAGUE. Even when I go to sleep, it is just BOBBLE LEAGUE. I imagine the strategies, bounces, and plays; just thinking about it now makes me want to play it. OMG, MGMMGNGM, I NEED TO GET ON BOBBLE LEAGUE RIGHT NOW. GOD I LOVE BOBBLE LEAGUE SO MUCH ❤️ @Bubble"
    )


@client.command(aliases=['bc', 'bing-chilling'])
async def Bing_Chilling(ctx):
  if time_okay():
    global current_time
    current_time = time.time()
    await ctx.send(
      "Zǎoshang hǎo zhōngguó xiànzài wǒ yǒu BING CHILLING 🥶🍦 wǒ hěn xǐhuān BING CHILLING 🥶🍦 dànshì sùdù yǔ jīqíng 9 bǐ BING CHILLING 🥶🍦 sùdù yǔ jīqíng sùdù yǔ jīqíng 9 wǒ zuì xǐhuān suǒyǐ…xiànzài shì yīnyuè shíjiān zhǔnbèi 1 2 3 liǎng gè lǐbài yǐhòu sùdù yǔ jīqíng 9 ×3 bùyào wàngjì bùyào cu òguò jìdé qù diànyǐngyuàn kàn sùdù yǔ jīqíng 9 yīn wéi fēicháng hǎo diànyǐng dòngzuò fēicháng hǎo chàbùduō yīyàng BING CHILLING 🥶🍦zàijiàn 🥶🍦"
    )


@client.command(aliases=['lol'])
async def League_Of_Legends(ctx):
  if time_okay():
    global current_time
    current_time = time.time()
    await ctx.send(
      "LEAGUE OF LEGENDS. I LOVE LEAGUE OF LEGENDS SO MUCH, PLEASE HELP; I AM ADDICTED TO LEAGUE OF LEGENDS; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS LEAGUE OF LEGENDS; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS LEAGUE OF LEGENDS. Even when I go to sleep, it is just LEAGUE OF LEGENDS. I imagine the champions, skills, and outplays; just thinking about it now makes me want to play it. OMG, MGMMGNGM, I NEED TO GET ON LEAGUE OF LEGENDS RIGHT NOW. GOD I LOVE LEAGUE OF LEGENDS SO MUCH"
    )


@client.command(aliases=['vl'])
async def valorant(ctx):
  if time_okay():
    global current_time
    current_time = time.time()
    await ctx.send(
      "VALORANT. I LOVE VALORANT SO MUCH, PLEASE HELP; I AM ADDICTED TO VALORANT; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS VALORANT; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS VALORANT. Even when I go to sleep, it is just VALORANT. I imagine the line ups, clutches, and aces; just thinking about it now makes me want to play it. OMG, MGMMGNGM, I NEED TO GET ON VALORANT RIGHT NOW. GOD I LOVE VALORANT SO MUCH"
    )


@client.command(aliases=['rr'])
async def RR(ctx, thing, *, number):
  if time_okay():
    global current_time
    current_time = time.time()
    if thing == 'pig':
      await ctx.send(
        f"┈┈┏━╮╭━┓┈╭━━━╮\n┈┃┏┗┛┓┃╭┫  {number}  ┃\n┈┈╰┓▋▋┏╯╯╰━━━╯\n┈╭━┻╮╲┗━━━━╮╭╮┈\n┈╰━┳┻▅╯╲╲╲╲┃┈┈┈\n┈┈┈╰━┳┓┏┳┓┏╯┈┈┈\n┈┈┈┈┈┗┻┛┗┻┛┈┈┈┈"
      )
    elif thing == 'truck':
      await ctx.send(
        f"──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n───▄▄██▌█ BEEP BEEP\n▄▄▄▌▐██▌█ {number}\n███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n▀(⊙)▀▀▀▀▀▀▀(⊙)(⊙)▀▀▀▀▀▀▀▀▀▀(⊙"
      )
    else:
      await ctx.send("Send one of the valid RR commands, see ;;commands")


@client.command(aliases=['nr'])
async def nate_reed(ctx, number):
  if time_okay():
    global current_time
    current_time = time.time()

    if number == '1':
      await ctx.send(
        "NATE REED. I LOVE NATE REED SO MUCH, PLEASE HELP; I AM ADDICTED TO NATE REED; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS NATE REED; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS NATE REED. Even when I go to sleep, it is just NATE REED. I imagine the story posts, the pure energy, and all the screenshots; just thinking about him now makes me want to look at more of his stories. OMG, MGMMGNGM, I NEED TO GET ON NATE REED RIGHT NOW. GOD I LOVE NATE REED SO MUCH ❤️"
      )
    elif number == '2':
      await ctx.send(
        "I was only nine years old. I loved NATE REED so much, I had all the merchandise and movies. I'd pray to NATE REED every night before I go to bed, thanking for the life I've been given. \"NATE REED is love\", I would say, \"NATE REED is life\". My dad hears me and calls me a faggot. I knew he was just jealous for my devotion of NATE REED. I called him a cunt. He slaps me and sends me to go to sleep. I'm crying now and my face hurts. I lay in bed and it's really cold. A warmth is moving towards me. I feel something touch me. It's NATE REED. I'm so happy. He whispers in my ear, \"This is my gaming dungeon\". He grabs me with his powerful e-boy hands, and puts me on my hands and knees. I spread my ass-cheeks for NATE REED He penetrates my butthole. It hurts so much, but I do it for NATE REED. I can feel my butt tearing as my eyes start to water. I push against his force. I want to please NATE REED. He roars a mighty roar, as he fills my butt with his love. My dad walks in. NATE REED looks him straight in the eye, and says, \"I\'m on my dad\'s esports team\". NATE REED leaves through my window. NATE REED is love. NATE REED is life."
      )
    else:
      await ctx.send("Send one of the valid Nate Reed commands, see ;;commands"
                     )


@client.command(aliases=['op'])
async def one_piece(ctx):
  if time_okay():
    global current_time
    current_time = time.time()
    await ctx.send(
      "ONE PIECE. I LOVE ONE PIECE SO MUCH, PLEASE HELP; I AM ADDICTED TO ONE PIECE; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS ONE PIECE; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS ONE PIECE. Even when I go to sleep, it is just ONE PIECE. Just thinking about it now makes me want to watch it. OMG, MGMMGNGM, I NEED TO WATCH ONE PIECE RIGHT NOW. GOD I LOVE ONE PIECE SO MUCH ❤️"
    )


@client.command(aliases=['omgg', 'OMGG'])
async def oh_my_goodness_gracious(ctx, *, phrase):
  if time_okay():
    global current_time
    current_time = time.time()
    await ctx.send(
      f"{phrase}. I LOVE {phrase} SO MUCH, PLEASE HELP; I AM ADDICTED TO {phrase}; PLEASE, I NEED HELP; ALL I EVER THINK ABOUT IS {phrase}; ANY TIME I TRY TO DO HOMEWORK, ALL THAT IS IN MY MIND IS {phrase}. Even when I go to sleep, it is just {phrase}. I imagine the {phrase}, with {phrase}, and {phrase}; just thinking about it now makes me need it. OMG, MGMMGNGM, I NEED TO GET ON {phrase} RIGHT NOW. GOD I LOVE {phrase} SO MUCH ❤️"
    )


# def make_information():
#     embed = discord.Embed(
#         color = discord.Color.darker_gray()
#     )

#     # embed.set_image(url = '')
#     embed.set_footer(text= 'Bot made by jporh#4599')
#     embed.add_field(name = "**DONT SPAM**", value = f"THE BOT WILL ONLY SEND EVERY {delay} seconds", inline = False)
#     embed.add_field(name = '**What This is**', value = "This is a bot that sends copypastas for quick use.", inline= False)
#     embed.add_field(name = 'What to do Next:', value = "There is a list of commands, type ';;commands' to learn more", inline= False)
#     return embed

# def command_info():
#     embed = discord.Embed(
#         color = discord.Color.darker_gray()
#     )

#     embed.set_footer(text = 'jporh#4599')

#     embed.add_field(name = '**Among Us**', value = ";;au(mogus, sus, peensus, amogus)", inline= False)
#     embed.add_field(name = "**Bernardson**", value = ";;askb[gives you a random askb gif]\n ;;askbofday[random gif of the day]")
#     embed.add_field(name = '**Bobble League**', value = ";;bl", inline= False)
#     embed.add_field(name = '**Bing Chilling**', value = ";;bc", inline = False)
#     embed.add_field(name = '**LOL**', value = ";;lol", inline = False)
#     embed.add_field(name = '**Nate Reed**', value = ";;nr 1 \n ;;nr 2", inline = False)
#     embed.add_field(name = '**Omega Strikers**', value = ";;os", inline= False)
#     embed.add_field(name = '**OMGG**', value = ';;omgg (text of the thing)', inline = False)
#     embed.add_field(name = '**One Piece**', value = ";;op", inline = False)
#     embed.add_field(name = '**-RR**', value = ";;rr (pig, truck) (number lost)\n ex: ;;rr pig 35", inline = False)
#     embed.add_field(name = '**Valorant**', value = ";;vl", inline = False)

#     return embed


def time_okay():
  if time.time() >= current_time + delay:
    return True
  else:
    return False


def plus_One_all(oh_no):
  if oh_no:
    for member in members:
      members[member].rolls += 1
      print(members[member].rolls)
    with open('members.json', 'w') as output_file:
      output_file.write(jsonpickle.encode(members, indent=1))


plus_One_all(oh_no)
keep_alive()
client.run(TOKEN)

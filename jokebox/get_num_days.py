from dotenv import load_dotenv
import discord
import asyncio
import os

load_dotenv()
TOKEN = os.environ.get('TOKEN')
GUILD_ID = 633777849806880779
CHANNEL_ID = 1129160056387153990

PREFIX = ';;'


intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    guild = client.get_guild(GUILD_ID)
    channel = client.get_channel(CHANNEL_ID)

    count = 0

    print("about to count")
    async for message in channel.history(limit=None):
        if message.content.startswith(PREFIX):
            print(f"Messaged matched {message.content}")
            count += 1

    print(f'Found {count} command usages')

    await client.close()


client.run(TOKEN)

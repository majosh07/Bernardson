from dotenv import load_dotenv
import os
import discord
from discord.ext.commands import Bot
from gacha import Gacha
from database import Database
# import logging

# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

load_dotenv()
TOKEN = os.environ.get('TOKEN')
if TOKEN is None:
  raise ValueError("TOKEN not set correctly, check .env...")

intents = discord.Intents.default()
intents.message_content= True


class askBernardson(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
    async def setup_hook(self) -> None:
        await self.add_cog(Gacha(self, self.db))

    async def on_ready(self):
        print(f'{self.user} has connected to Discord.')



bot = askBernardson(command_prefix=';;', intents=intents)
# bot.run(TOKEN, log_handler=handler, root_logger=True)
bot.run(TOKEN)

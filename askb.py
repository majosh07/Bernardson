from discord.ext.commands import Bot
from gacha import Gacha


class askBernardson(Bot):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  async def setup_hook(self) -> None:
    await self.add_cog(Gacha(self))

  async def on_ready(self):
    print(f'{self.user} has connected to Discord.')




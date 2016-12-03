import discord
from discord.ext import commands
import urllib, json

class Mycog:
    """My custom cog that does stuff!"""

    def init(self, bot):
        self.bot = bot


    async def saypokes(self):
        """Says latest pokemon"""

        url = "http://www.hydrabot.info/pokemon.json"
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            await self.bot.say(data)
        await asyncio.sleep(10)

def setup(bot):
    n = Mycog(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.saypokes())
    bot.add_cog(Mycog(bot))
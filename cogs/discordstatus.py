import aiohttp
from discord.ext import commands

try:
    from bs4 import BeautifulSoup
    soupAvailable = True
except:
    soupAvailable = False


class DiscordStatus:
    """Get Discord status"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self):
        """Get Discord Status"""

        url = "https://status.discordapp.com/"
        async with aiohttp.ClientSession(loop=None).get(url) as response:
            soupObject = BeautifulSoup(await response.text(), 'html.parser')
            try:
                status = soupObject.find(class_='unresolved-incident impact-none').get_text()
                await self.bot.say(status)
            except:
                await self.bot.say("Discord: Everything is fine")


def setup(bot):
    if soupAvailable:
        bot.add_cog(DiscordStatus(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")

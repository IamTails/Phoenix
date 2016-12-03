from discord.ext import commands
import random
import discord
import asyncio

class Plants:
    """Grow your own plants! There are 40 of them!"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def grow(self, context):
        """Grow a plant! Costs 100$ to plant one!"""
        gardener = context.message.author.mention

        plant = [
            {'name': 'Dandelion', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/emqnQP2.jpg', 'cash' : 500},
            {'name': 'Poppy', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/S4hjyUX.jpg', 'cash' : 500},
            {'name': 'Daisy', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/lcFq4AB.jpg', 'cash' : 500},
            {'name': 'Chrysanthemum', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/5jLtqWL.jpg', 'cash' : 500},
            {'name': 'Pansy', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/f7TgD1b.jpg', 'cash' : 500},
            {'name': 'Lavender', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/g3OmOSK.jpg', 'cash' : 500},
            {'name': 'Lily', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/0hzy7lO.jpg', 'cash' : 500},
            {'name': 'Petunia', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/rJm8ISv.jpg', 'cash' : 500},
            {'name': 'Sunflower', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/AzgzQK9.jpg', 'cash' : 500},
            {'name': 'Daffodil', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/pnCCRsH.jpg', 'cash' : 500},
            {'name': 'Clover', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/0GSsABG.jpg', 'cash' : 500},
            {'name': 'Tulip', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/kodIFjE.jpg', 'cash' : 500},
            {'name': 'Rose', 'article' : 'a', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/sdTNiOH.jpg', 'cash' : 500},
            {'name': 'Aster', 'article' : 'an', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/1tN04Hl.jpg', 'cash' : 500},
            {'name': 'Aloe Vera', 'article' : 'an', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/WFAYIpx.jpg', 'cash' : 500},
            {'name': 'Orchid', 'article' : 'an', 'time': 300, 'rarity': 'common', 'link' : 'http://i.imgur.com/IQrQYDC.jpg', 'cash' : 500},
            {'name': 'Dragon Fruit Plant', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/pfngpDS.jpg', 'cash' : 1000},
            {'name': 'Mango Tree', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/ybR78Oc.jpg', 'cash' : 1000},
            {'name': 'Lychee Tree', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/w9LkfhX.jpg', 'cash' : 1000},
            {'name': 'Durian Tree', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/jh249fz.jpg', 'cash' : 1000},
            {'name': 'Fig Tree', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/YkhnpEV.jpg', 'cash' : 1000},
            {'name': 'Jack Fruit Tree', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/2D79TlA.jpg', 'cash' : 1000},
            {'name': 'Prickly Pear Plant', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/GrcGAGj.jpg', 'cash' : 1000},
            {'name': 'Pineapple Plant', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/VopYQtr.jpg', 'cash' : 1000},
            {'name': 'Citron Tree', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/zh7Dr23.jpg', 'cash' : 1000},
            {'name': 'Cherimoya Tree', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/H62gQK6.jpg', 'cash' : 1000},
            {'name': 'Mangosteen Tree', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/McNnMqa.jpg', 'cash' : 1000},
            {'name': 'Guava Tree', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/iy8WgPt.jpg', 'cash' : 1000},
            {'name': 'Orange Tree', 'article' : 'an', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/lwjEJTm.jpg', 'cash' : 1000},
            {'name': 'Apple Tree', 'article' : 'an', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/QI3UTR3.jpg', 'cash' : 1000},
            {'name': 'Sapodilla Tree', 'article' : 'a', 'time': 600, 'rarity': 'uncommon', 'link' : 'http://i.imgur.com/6BvO5Fu.jpg', 'cash' : 1000},
            {'name': 'Franklin Tree', 'article' : 'a', 'time': 1200, 'rarity': 'rare', 'link' : 'http://i.imgur.com/hoh17hp.jpg', 'cash' : 2500},
            {'name': 'Parrot\'s Beak', 'article' : 'a', 'time': 1200, 'rarity': 'rare', 'link' : 'http://i.imgur.com/lhSjfQY.jpg', 'cash' : 2500},
            {'name': 'Koki\'o', 'article' : 'a', 'time': 1200, 'rarity': 'rare', 'link' : 'http://i.imgur.com/Dhw9ync.jpg', 'cash' : 2500},
            {'name': 'Jade Vine', 'article' : 'a', 'time': 1200, 'rarity': 'rare', 'link' : 'http://i.imgur.com/h4fJo2R.jpg', 'cash' : 2500},
            {'name': 'Venus Fly Trap', 'article' : 'a', 'time': 1200, 'rarity': 'rare', 'link' : 'http://i.imgur.com/NoSdxXh.jpg', 'cash' : 2500},
            {'name': 'Chocolate Cosmos', 'article' : 'a', 'time': 1200, 'rarity': 'rare', 'link' : 'http://i.imgur.com/4ArSekX.jpg', 'cash' : 2500},
            {'name': 'Pizza Plant', 'article' : 'a', 'time': 1800, 'rarity': 'super rare', 'link' : 'http://i.imgur.com/ASZXr7C.png', 'cash' : 5000},
            {'name': 'Radiant Roxy Rose', 'article' : 'a', 'time': 1800, 'rarity': 'super rare', 'link' : 'http://i.imgur.com/aLe56mr.png', 'cash' : 5000},
            {'name': 'Pirahna Plant', 'article' : 'a', 'time': 1800, 'rarity': 'super rare', 'link' : 'http://i.imgur.com/c03i9W7.jpg', 'cash' : 5000},
            {'name': 'Pod Plant', 'article' : 'a', 'time': 1800, 'rarity': 'super rare', 'link' : 'http://i.imgur.com/ECAGMUM.jpg', 'cash' : 5000},
            {'name': 'Peashooter', 'article' : 'a', 'time': 1800, 'rarity': 'super rare', 'link' : 'http://imgur.com/a/IJBu2', 'cash' : 5000},
            {'name': 'Starlight Rose', 'article' : 'a', 'time': 2400, 'rarity': 'epic', 'link' : 'http://i.imgur.com/em8Kg5M.png', 'cash' : 7500},
            {'name': 'Pikmin', 'article' : 'a', 'time': 2400, 'rarity': 'epic', 'link' : 'http://i.imgur.com/cFSmaHH.png', 'cash' : 7500},
            {'name': 'Groot', 'article' : 'a', 'time': 2400, 'rarity': 'epic', 'link' : 'http://i.imgur.com/9f5QzaW.jpg', 'cash' : 7500},
            {'name': 'Triffid', 'article' : 'a', 'time': 2400, 'rarity': 'epic', 'link' : 'http://i.imgur.com/WZlwqUt.jpg', 'cash' : 7500},
            {'name': 'Athelas', 'article' : 'an', 'time': 2400, 'rarity': 'epic', 'link' : 'http://i.imgur.com/PNNMEjB.jpg', 'cash' : 7500},
            {'name': 'Money Tree', 'article' : 'a', 'time': 3600, 'rarity': 'legendary', 'link' : 'http://i.imgur.com/MIJQDLL.jpg', 'cash' : 10000},
            {'name': 'Truffula Tree', 'article' : 'a', 'time': 3600, 'rarity': 'legendary', 'link' : 'http://i.imgur.com/cFSmaHH.png', 'cash' : 10000},
            {'name': 'Whomping Willow', 'article' : 'a', 'time': 3600, 'rarity': 'legendary', 'link' : 'http://i.imgur.com/Ibwm2xY.jpg', 'cash' : 10000}
                ]

        used = random.choice(plant)

        bank = self.bot.get_cog('Economy').bank
        bank.withdraw_credits(context.message.author, 100)
        await self.bot.say('{0}, you have sown the seed for 100$! http://i.imgur.com/4uIktZQ.jpg'.format(gardener))
        await asyncio.sleep(used['time'])
        await self.bot.say('{0}, your plant needs water! Do you want to water it? (yes/no)'.format(gardener))
        answer = await self.bot.wait_for_message(timeout=300,
                                                 author=context.message.author)

        if answer is None:
            await self.bot.say('{0}, your plant has died...'.format(gardener))
        elif answer.content.lower().strip() == "yes":
            await self.bot.say('You have successfully watered the plant.')
            await asyncio.sleep(used['time'])
            await self.bot.say('{0}, the soil needs fertilizer! Do you want to fertilize it? (yes/no)'.format(gardener))
            answer = await self.bot.wait_for_message(timeout=300,
                                                     author=context.message.author)

            if answer is None:
                await self.bot.say('{0}, your plant has died...'.format(gardener))
            elif answer.content.lower().strip() == "yes":
                await self.bot.say('You have successfully fertilized the soil.')
                await asyncio.sleep(used['time'])
                await self.bot.say('{0}, you have grown {1} **{2}** [{3}] {4}'.format(gardener, used['article'], used['name'], used['rarity'], used['link']))
                bank.deposit_credits(context.message.author, used['cash'])
                await self.bot.say('You have recieved {0}$ for growing a {1} plant.'.format(used['cash'], used['rarity']))
            else:
                await self.bot.say('{0}, your plant has died...'.format(gardener))
        else:
            await self.bot.say('{0}, your plant has died...'.format(gardener))
def setup(bot):
    bot.add_cog(Plants(bot))

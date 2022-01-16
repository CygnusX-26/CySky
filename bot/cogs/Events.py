import discord
from discord.ext import commands
from aiohttp import ClientSession
import time
from datetime import date

today = date.today()

async def asyncGetInfo(call, session):
    async with session.get(call) as response:
        result = await response.json()
        return result


class Events(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.timer = None

    @commands.command()
    async def events(self, ctx):

        embed = discord.Embed(
            title = 'Events',
            description = f'> Your Timezone <t:{str(time.time()//1)[0:-2]}:F>',
            colour=discord.Colour.dark_gray()
        )

        async with ClientSession() as session:
            self.timer = await asyncGetInfo('https://api.slothpixel.me/api/skyblock/calendar?years=1', session)

        embed.set_thumbnail(url='https://images.emojiterra.com/twitter/512px/1f5d3.png')
        embed.add_field(name = '**Next Bank Interest**', value = self.getEventR('BANK_INTEREST'), inline=False)
        embed.add_field(name = '**The Spooky Festival is starting**', value = self.getEvent('SPOOKY_FESTIVAL'), inline=False)
        embed.add_field(name = "**Jerry's Workshop is starting**", value = self.getEvent('JERRYS_WORKSHOP'), inline=False)
        embed.add_field(name = '**The New Year Celebration is starting**', value = self.getEvent('NEW_YEAR_CELEBRATION'), inline=False)
        embed.add_field(name = '**Traveling Zoo is starting**', value = self.getEvent('TRAVELING_ZOO'), inline=False)
        embed.add_field(name = '**Election Booth Open is starting**', value = self.getEvent('ELECTION_BOOTH_OPENS'), inline=False)
        embed.add_field(name = '**Election over**', value = self.getEvent('ELECTION_OVER'), inline=False)
        embed.add_field(name = "**Next Jacob's Contest is starting**", value = '<t:' + str(self.getLatestJacob()) + ':R>', inline=False)
        embed.set_footer(text=f'Today ▹ <t:{str(time.time()//1)[0:-2]}:d>')
        await ctx.send(embed=embed)
    
    def getEvent(self, event):
        return '<t:' + str((self.timer['events'][event]['events'][-1]['start_timestamp'])//1000) + ':F>'

    def getEventR(self, event):
        return '<t:' + str((self.timer['events'][event]['events'][-1]['start_timestamp'])//1000) + ':R>'

    def getLatestJacob(self):
        oldMin = self.timer['events']['JACOBS_CONTEST']['events'][0]['starting_in']
        for i in self.timer['events']['JACOBS_CONTEST']['events']:
            if i['starting_in'] < oldMin:
                oldMin = i['starting_in']
                oldTime = i['start_timestamp']
        
        return oldTime//1000


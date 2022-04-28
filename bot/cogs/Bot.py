import discord
from discord.ext import commands


class bot(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('This bot is online!')
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"waiting for hypixel api :( in {len(self.bot.guilds)} servers"))

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        embed = discord.Embed(
            title=f'Help menu',
            description='> Page - 1/1',
            colour=discord.Colour.dark_grey()
        )
        embed.set_footer(
            text='Coded in python, powered by the Hypixel, Slothpixel, Senither, Maro, and Skycrypt APIs')
        embed.add_field(name='List of Commands', value='''
        > Verify your Minecraft account with &verify first!
        `help` ▹ displays this menu!
        `ah` ▹ displays auction info for a specified player.
        `bz` ▹ displays bazaar info for a specified item.
        `bztop` ▹ displays bazaar info for a specified item.
        `events`▹ displays upcoming events for the next skyblock year. 
        `latest` ▹ displays the latest skyblock update information.
        `networth` ▹ displays the specified user's current networth.
        `profile` ▹ displays the user's Skyblock profiles and their IDs.
        `weight` ▹ displays current Senither player weight.
        Invite the bot to your server [here](https://discord.com/api/oauth2/authorize?client_id=277588583693680640&permissions=277025508352&scope=bot)
        [This bot is open source!](https://github.com/CygnusX-26/CySky)
        ''', inline=False)
        await ctx.send(embed=embed)
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"waiting for hypixel api :( in {len(self.bot.guilds)} servers"))

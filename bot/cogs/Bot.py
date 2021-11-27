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
            activity=discord.Game("waiting for hypixel api :("))

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        embed = discord.Embed(
            title=f'Help menu',
            description='> Page - 1/1',
            colour=discord.Colour.dark_grey()
        )
        embed.set_footer(
            text='Coded in python, powered by the Hypixel, Slothpixel, Senither, and Skycrypt APIs')
        embed.add_field(name='List of Commands', value='''
        > Verify your Minecraft account with &verify first!
        `help` ▹ displays this menu!
        `ah` ▹ displays auction info for a specified player.
        `bz` ▹ displays bazaar info for a specified item.
        `bztop` ▹ displays bazaar info for a specified item.
        `latest` ▹ displays the latest skyblock update information.
        `profile` ▹ displays the user's Skyblock profiles and their IDs.
        `weight` ▹ displays current Senither player weight.
        ''', inline=False)
        await ctx.send(embed=embed)
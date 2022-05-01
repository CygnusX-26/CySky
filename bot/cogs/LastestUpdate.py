import discord
from discord.ext import commands
import requests
import json
from aiohttp import ClientSession
from username_to_uuid import UsernameToUUID
import os
from discord import app_commands

API_KEY = os.getenv("API_KEY")


def getInfo(call):
    r = requests.get(call)
    return r.json()


async def asyncGetInfo(call, session):
    async with session.get(call) as response:
        result = await response.json()
        return result


class LatestUpdate(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='latest', description='Shows the latest skyblock update')
    async def latestupdate(self, interaction: discord.Interaction) -> None:
        async with ClientSession() as session:
            update_data = await asyncGetInfo(f'https://api.hypixel.net/skyblock/news?key={API_KEY}', session)
        embed = discord.Embed(
            title=f"{update_data['items'][0]['title']}",
            description=f"{update_data['items'][0]['text']}",
            colour=discord.Colour.blurple()
        )
        link = update_data['items'][0]['link']
        embed.set_thumbnail(url='https://i.gifer.com/Vg7.gif')
        embed.add_field(
            name='\u200b', value=f'Link to the forum post [here]({link}).', inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(LatestUpdate(bot))
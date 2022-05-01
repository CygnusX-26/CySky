import discord
from discord.ext import commands
import requests
from aiohttp import ClientSession
import json
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


class Bazaar(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = 'bazaar', description = 'Checks the bazaar for a given item')
    @app_commands.describe(item = "The item to check")
    async def bazaarInfo(self, interaction: discord.Interaction, *, item:str) -> None:
        boolId = False
        async with ClientSession() as session:
            bazaar_data = await asyncGetInfo(f'https://api.hypixel.net/skyblock/bazaar?key={API_KEY}', session)
            item_data = await asyncGetInfo('https://api.hypixel.net/resources/skyblock/items', session)
        if item.isupper():  # checks if item id
            id = item
            boolId = True

        try:
            item2 = str.title(item)
            for i in range(len(item_data['items'])):
                value = item_data['items'][i]['name']
                if value.startswith('§'):
                    value = value[2:]
                if (value.lower() == item2.lower() or item_data['items'][i]['id'] == item):
                    if (not(boolId)):
                        id = item_data['items'][i]['id']
                        try:
                            tier = item_data['items'][i]['tier']
                        except:
                            tier = 'COMMON'
                        break
                    else:
                        item = item_data['items'][i]['name']
                        try:
                            tier = item_data['items'][i]['tier']
                        except:
                            tier = 'COMMON'
                        break
            embed = discord.Embed(
                title=f'Bazaar Info for:',
                colour=discord.Colour.light_gray()
            )
            sell_price = float(
                bazaar_data['products'][id]['sell_summary'][0]['pricePerUnit'])
            buy_price = float(
                bazaar_data['products'][id]['buy_summary'][0]['pricePerUnit'])

            embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/{id}')
            embed.add_field(name=f'{str.title(item)}', value=f"""
            `Rarity` ▹ {tier}
            `Bazaar Buy Price` ▹ {round(sell_price, 2):,}
            `Bazaar Sell Price`▹ {round(buy_price, 2):,}
            `Sell Volume` ▹ {bazaar_data['products'][id]['quick_status']['sellVolume']:,}
            `Buy Volume` ▹ {bazaar_data['products'][id]['quick_status']['buyVolume']:,}
            `Sell Orders` ▹ {bazaar_data['products'][id]['quick_status']['sellOrders']:,}
            `Buy Orders` ▹ {bazaar_data['products'][id]['quick_status']['buyOrders']:,}
            `Current Flip Value` ▹ {round(buy_price - sell_price, 2):,}
            `Current % Profit` ▹ {round((buy_price - sell_price)/sell_price, 2) * 100}%
            """, inline=True)
        except:
            embed = discord.Embed()
            embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
            embed.add_field(name='Error', value=f"""Uh oh! Looks like the item ID you were searching for couldn't be found... 
            Make sure you are inputting the correct item id, spelling corectly, or that the item exists on the bazaar! For further information and a list of item ids, you can click [here](https://api.slothpixel.me/api/skyblock/items).""", inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Bazaar(bot))
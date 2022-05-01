import discord
from discord.ext import commands
import requests
import json
from aiohttp import ClientSession
from discord import app_commands
from discord.app_commands import Choice
import os

API_KEY = os.getenv("API_KEY")


def getInfo(call):
    r = requests.get(call)
    return r.json()


async def asyncGetInfo(call, session):
    async with session.get(call) as response:
        result = await response.json()
        return result


class BazaarTop(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = 'bztop', description = 'Finds best flips on the bazaar')
    @app_commands.describe(type = "The type of flip to look for")
    @app_commands.choices(type = [Choice(name='margin', value='margin'), Choice(name='percent', value='percent'), Choice(name='demand', value='demand'), Choice(name='smart', value='smart')])
    async def bazaartop(self, interaction: discord.Interaction, type:str) -> None:
        if (type == 'margin' or type == 'm'):
            old = 0
            value = 0
            async with ClientSession() as session:
                bazaar_data = await asyncGetInfo(f'https://api.hypixel.net/skyblock/bazaar?key={API_KEY}', session)
                item_data = await asyncGetInfo('https://api.hypixel.net/resources/skyblock/items', session)
            bazaar_items = []
            for i in range(len(item_data['items'])):
                bazaar_items.append(item_data['items'][i]['id'])
            for i in range(len(bazaar_items)):
                try:
                    buy_price = float(
                        bazaar_data['products'][bazaar_items[i]]['buy_summary'][0]['pricePerUnit'])
                    sell_price = float(
                        bazaar_data['products'][bazaar_items[i]]['sell_summary'][0]['pricePerUnit'])
                    if buy_price - sell_price > old:
                        old = buy_price - sell_price
                        value = i
                        buy_pricef = buy_price
                        sell_pricef = sell_price
                except:
                    continue
            embed = discord.Embed(
                title='Best Profit Margin Bazaar Flip:',
                colour=discord.Colour.default()
            )
            embed.set_thumbnail(
                url=f'https://sky.shiiyu.moe/item/{bazaar_items[value]}')
            embed.add_field(name=f'{bazaar_items[value]}', value=f"""
            `Bazaar Buy Price` ▹ {round(sell_pricef, 2):,}
            `Bazaar Sell Price`▹ {round(buy_pricef, 2):,}
            `Sell Volume` ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['sellVolume']:,}
            `Buy Volume` ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['buyVolume']:,}
            `Sell Orders` ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['sellOrders']:,}
            `Buy Orders` ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['buyOrders']:,}
            __**`Current Flip Value`**__ ▹ {round(buy_pricef - sell_pricef, 2):,}
            `Current % Profit` ▹ {round((buy_pricef - sell_pricef)/sell_pricef, 2) * 100}%
            """, inline=True)
            embed.set_footer(
                text='⚠️Please note that some markets may be extremely volatile⚠️')
            await interaction.response.send_message(embed=embed)
        elif (type == 'percent' or type == 'p' or type == '%'):
            old = 0
            value = 0
            async with ClientSession() as session:
                bazaar_data = await asyncGetInfo(f'https://api.hypixel.net/skyblock/bazaar?key={API_KEY}', session)
                item_data = await asyncGetInfo('https://api.hypixel.net/resources/skyblock/items', session)
            bazaar_items = []
            for i in range(len(item_data['items'])):
                bazaar_items.append(item_data['items'][i]['id'])
            for i in range(len(bazaar_items)):
                try:
                    buy_price = float(
                        bazaar_data['products'][bazaar_items[i]]['buy_summary'][0]['pricePerUnit'])
                    sell_price = float(
                        bazaar_data['products'][bazaar_items[i]]['sell_summary'][0]['pricePerUnit'])
                    if (buy_price - sell_price)/sell_price > old:
                        old = (buy_price - sell_price)/sell_price
                        value = i
                        buy_pricef = buy_price
                        sell_pricef = sell_price
                except:
                    continue
            embed = discord.Embed(
                title='Best % Flip:',
                colour=discord.Colour.default()
            )
            embed.set_thumbnail(
                url=f'https://sky.shiiyu.moe/item/{bazaar_items[value]}')
            embed.add_field(name=f'{bazaar_items[value]}', value=f"""
            `Bazaar Buy Price` ▹ {round(sell_pricef, 2):,}
            `Bazaar Sell Price`▹ {round(buy_pricef, 2):,}
            `Sell Volume` ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['sellVolume']:,}
            `Buy Volume` ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['buyVolume']:,}
            `Sell Orders` ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['sellOrders']:,}
            `Buy Orders` ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['buyOrders']:,}
            `Current Flip Value` ▹ {round(buy_pricef - sell_pricef, 2):,}
            __**`Current % Profit`**__ ▹ {round((buy_pricef - sell_pricef)/sell_pricef, 2) * 100}%
            """, inline=True)
            embed.set_footer(
                text='⚠️Please note that some markets may be extremely volatile⚠️')
            await interaction.response.send_message(embed=embed)
        elif (type == 'demand' or type == 'd'):
            old = 0
            value = 0
            async with ClientSession() as session:
                bazaar_data = await asyncGetInfo(f'https://api.hypixel.net/skyblock/bazaar?key={API_KEY}', session)
                item_data = await asyncGetInfo('https://api.hypixel.net/resources/skyblock/items', session)
            bazaar_items = []
            for i in range(len(item_data['items'])):
                bazaar_items.append(item_data['items'][i]['id'])
            for i in range(len(bazaar_items)):
                try:
                    buy_price = float(
                        bazaar_data['products'][bazaar_items[i]]['buy_summary'][0]['pricePerUnit'])
                    sell_price = float(
                        bazaar_data['products'][bazaar_items[i]]['sell_summary'][0]['pricePerUnit'])
                    if bazaar_data['products'][bazaar_items[i]]['quick_status']['buyVolume'] + bazaar_data['products'][bazaar_items[i]]['quick_status']['sellVolume'] > old:
                        old = bazaar_data['products'][bazaar_items[i]]['quick_status']['buyVolume'] + \
                            bazaar_data['products'][bazaar_items[i]
                                                    ]['quick_status']['sellVolume']
                        value = i
                        buy_pricef = buy_price
                        sell_pricef = sell_price
                except:
                    continue
            embed = discord.Embed(
                title='Highest Demand',
                colour=discord.Colour.default()
            )
            embed.set_thumbnail(
                url=f'https://sky.shiiyu.moe/item/{bazaar_items[value]}')
            embed.add_field(name=f'{bazaar_items[value]}', value=f"""
            `Bazaar Buy Price` ▹ {round(sell_pricef, 2):,}
            `Bazaar Sell Price`▹ {round(buy_pricef, 2):,}
            __**`Sell Volume`**__ ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['sellVolume']:,}
            __**`Buy Volume`**__ ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['buyVolume']:,}
            `Sell Orders` ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['sellOrders']:,}
            `Buy Orders` ▹ {bazaar_data['products'][bazaar_items[value]]['quick_status']['buyOrders']:,}
            `Current Flip Value` ▹ {round(buy_pricef - sell_pricef, 2):,}
            `Current % Profit` ▹ {round((buy_pricef - sell_pricef)/sell_pricef, 2) * 100}%
            """, inline=True)
            embed.set_footer(
                text='⚠️Please note that some markets may be extremely volatile⚠️')
            await interaction.response.send_message(embed=embed)
        elif (type == 'smart' or type == 's'):
            old = 0
            value = 0
            async with ClientSession() as session:
                bazaar_data = await asyncGetInfo(f'https://api.hypixel.net/skyblock/bazaar?key={API_KEY}', session)
                item_data = await asyncGetInfo('https://api.hypixel.net/resources/skyblock/items', session)
            bazaar_items = []
            smart_list = []
            for i in range(len(item_data['items'])):
                bazaar_items.append(item_data['items'][i]['id'])
            for i in range(len(bazaar_items)):
                try:
                    buy_orders = bazaar_data['products'][bazaar_items[i]
                                                         ]['quick_status']['buyOrders']
                    sell_orders = bazaar_data['products'][bazaar_items[i]
                                                          ]['quick_status']['sellOrders']
                    buy_price = float(
                        bazaar_data['products'][bazaar_items[i]]['buy_summary'][0]['pricePerUnit'])
                    sell_price = float(
                        bazaar_data['products'][bazaar_items[i]]['sell_summary'][0]['pricePerUnit'])
                    if buy_orders + sell_orders > 700:
                        smart_list.append(
                            bazaar_data['products'][bazaar_items[i]]['quick_status']['productId'])
                except:
                    continue
            for i in range(len(smart_list)):
                try:
                    buy_price = float(
                        bazaar_data['products'][smart_list[i]]['buy_summary'][0]['pricePerUnit'])
                    sell_price = float(
                        bazaar_data['products'][smart_list[i]]['sell_summary'][0]['pricePerUnit'])
                    if (buy_price - sell_price)/sell_price > old:
                        old = (buy_price - sell_price)/sell_price
                        value = i
                        buy_pricef = buy_price
                        sell_pricef = sell_price
                except:
                    continue
            embed = discord.Embed(
                title='Current Smartest Flip',
                colour=discord.Colour.default()
            )
            embed.set_thumbnail(
                url=f'https://sky.shiiyu.moe/item/{smart_list[value]}')
            embed.add_field(name=f'{smart_list[value]}', value=f"""
            `Bazaar Buy Price` ▹ {round(sell_pricef, 2):,}
            `Bazaar Sell Price`▹ {round(buy_pricef, 2):,}
            __**`Sell Volume`**__ ▹ {bazaar_data['products'][smart_list[value]]['quick_status']['sellVolume']:,}
            __**`Buy Volume`**__ ▹ {bazaar_data['products'][smart_list[value]]['quick_status']['buyVolume']:,}
            `Sell Orders` ▹ {bazaar_data['products'][smart_list[value]]['quick_status']['sellOrders']:,}
            `Buy Orders` ▹ {bazaar_data['products'][smart_list[value]]['quick_status']['buyOrders']:,}
            `Current Flip Value` ▹ {round(buy_pricef - sell_pricef, 2):,}
            `Current % Profit` ▹ {round((buy_pricef - sell_pricef)/sell_pricef, 2) * 100}%
            """, inline=True)
            embed.set_footer(
                text='⚠️Please note that some markets may be extremely volatile⚠️')
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed()
            embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
            embed.add_field(name='Error', value=f"""
            Please specify a valid value for bazaar top!
            `margin`
            `percent`
            `demand`
            `smart`
            """, inline=True)
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(BazaarTop(bot))
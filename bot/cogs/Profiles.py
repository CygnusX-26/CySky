import discord
from discord.ext import commands
import requests
import json
import os
from aiohttp import ClientSession
from username_to_uuid import UsernameToUUID
import sqlite3

conn = sqlite3.connect('bot/data/accounts.db')

c = conn.cursor()

API_KEY = os.getenv("API_KEY")


def getInfo(call):
    r = requests.get(call)
    return r.json()


async def asyncGetInfo(call, session):
    async with session.get(call) as response:
        result = await response.json()
        return result


def getUser(id, mcname):
    c.execute(
        f"SELECT * FROM accounts WHERE id = {id} AND mcname = ?", (mcname,))
    return c.fetchone()


class Profiles(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['p'])
    async def profile(self, ctx, player=None):
        if (player == None):
            c.execute(f"SELECT * FROM accounts")
            check = c.fetchall()
            user = ctx.message.author.id
            if len(check) == 0:
                return
            for i in range(len(check)):
                if user in check[i]:
                    player = getUser(user, check[i][1])[1]
            if player == None:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(name='Error `Unverified`', value=f"""Uh oh! Looks like the discord account you are using has not been verified. 
                Link your minecraft account with &verify [accountname]""", inline=True)
                await ctx.send(embed=embed)
                return

        converter = UsernameToUUID(f'{player}')
        uuid = converter.get_uuid()

        embed2 = discord.Embed(
            title=f'Profiles for {player}',
            description='Loading...',
            colour=discord.Colour.dark_gray()
        )
        message = await ctx.send(embed=embed2)

        try:
            async with ClientSession() as session:
                profile_data = await asyncGetInfo(f'https://hypixel-skyblock-facade.cygnusx.repl.co/v1/profiles/{uuid}?key={API_KEY}', session)

            status = profile_data['status']

            # Error Handler
            if status == 200:
                pass
            elif status == 400:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(
                    name='Error', value=f"""The request is missing an authentication method, you must either provide a valid **key query paramater**, or an **Authentication header**.""", inline=True)
                await message.edit(embed=embed)
                return
            elif status == 403:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(
                    name='Error', value=f"""The provided Hypixel API token is invalid, or does not exists.""", inline=True)
                await message.edit(embed=embed)
                return
            elif status == 404:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(
                    name='Error', value=f"""There is either no player with the given UUID, or the player has no SkyBlock profiles.""", inline=True)
                await message.edit(embed=embed)
                return
            elif status == 429:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(name='Error', value=f"""The Hypixel API rate-limited was reached, if you see this in your resposnes you should slow down requests, or start caching response to prevent having to make as many requests in the future.""", inline=True)
                await message.edit(embed=embed)
                return
            elif status == 500:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(
                    name='Error', value=f"""An internal error occurred in the API, or the Hypixel API responded with an unknown error code.""", inline=True)
                await message.edit(embed=embed)
                return
            elif status == 502:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(name='Error', value=f"""Hypixels API is experiencing some technical issues and may not be available, if you get this error code just re-send your request at a later time, hopefully Hypixels API will work again by then.""", inline=True)
                await message.edit(embed=embed)
                return
            elif status == 503:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(
                    name='Error', value=f"""Hypixels API is in maintenance mode, you can't really do much about this, just try re-send your request when the API is back online.""", inline=True)
                await message.edit(embed=embed)
                return

            data = profile_data['data']
            embed = discord.Embed(
                title=f"List of {player}'s Profiles",
                description=f'> **{player}** has a total of **{len(data)}** profiles!',
                colour=discord.Colour.dark_grey()
            )
            embed.set_thumbnail(url=f'https://mc-heads.net/head/{player}')
            embed.set_footer(text=f"https://sky.shiiyu.moe/stats/{player}.", icon_url='https://storage.cloudconvert.com/tasks/955dc6fd-4951-4478-8cf0-9844480a60b5/crypt.jpg?AWSAccessKeyId=cloudconvert-production&Expires=1637720970&Signature=jDJTh6IvRy3qu%2BQhluD6FYby3x4%3D&response-content-disposition=inline%3B%20filename%3D%22crypt.jpg%22&response-content-type=image%2Fjpeg')
            for i in range(len(data)):
                embed.add_field(name=f"{data[i]['name']}", value=f"""
                `id:`
                {data[i]['id']}
                `Weight`
                {round(data[i]['weight'] + data[i]['weight_overflow'], 2):,}
                """)
            await message.edit(embed=embed)

        except:
            embed = discord.Embed()
            embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
            embed.add_field(name='Error', value=f"""Uh oh! Looks like the player you were searching for couldn't be found... 
            Check your spelling! For further information and more detailed info, you can click [here](https://sky.shiiyu.moe/api/v2/coins/{player}).""", inline=True)
            await message.edit(embed=embed)

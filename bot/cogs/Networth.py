import discord
from discord.ext import commands
import requests
import json
import os
import sqlite3
from pprint import pprint
from aiohttp import ClientSession
from username_to_uuid import UsernameToUUID

conn = sqlite3.connect('accounts.db')

c = conn.cursor()

API_KEY = os.getenv("API_KEY")

def getInfo(call):
    r = requests.get(call)
    return r.json()

async def asyncPostInfo(call, data, session):
    async with session.post(call, json=data) as response:
        result = await response.json()
        return result

async def asyncGetInfo(call, session):
    async with session.get(call) as response:
        result = await response.json()
        return result


def getUser(id, mcname):
    c.execute(
        f"SELECT * FROM accounts WHERE id = {id} AND mcname = ?", (mcname,))
    return c.fetchone()


class Networth(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['nw'])
    async def networth(self, ctx, player=None):
        oldSave = -1
        count = -1
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
        
        embed2 = discord.Embed(
            title=f"{player}'s total networth",
            description='Loading...',
            colour=discord.Colour.dark_gray()
        )
        message = await ctx.send(embed=embed2)

        converter = UsernameToUUID(f'{player}')
        uuid = converter.get_uuid()

        async with ClientSession() as session:
            data = await asyncGetInfo(f'https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}', session)
            try:
                for i in data['profiles']:
                    lastSave = i['members'][uuid]['last_save'] 
                    count += 1
                    if lastSave > oldSave:
                        oldSave = lastSave
                        fcount = count
            except:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(name='Error `User not found!`', value="Couldn't find the requested user.", inline=True)
                await message.edit(embed=embed)
                return

            profile = data['profiles'][fcount]['members'][uuid]
            categories = await asyncPostInfo("https://skyblock.acebot.xyz/api/networth/categories", {"data": profile}, session)
        if categories['status'] == 404:
            embed = discord.Embed()
            embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
            embed.add_field(name='Error `API Disabled`', value=f"{categories['cause']}", inline=True)
            await message.edit(embed=embed)
            return
        networth = categories['data']['networth']
        purse = categories['data']['purse']
        sacks = categories['data']['sacks']

        embed = discord.Embed(
            title=f"{player}'s total networth ",
            description=f'> **{round(networth + purse + sacks, 2):,}**',
            colour=discord.Colour.dark_gray() 
        )
        await message.edit(embed=embed)

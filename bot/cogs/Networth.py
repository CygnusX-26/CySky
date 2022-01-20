import discord
from discord.ext import commands
import requests
import json
import os
import sqlite3
from aiohttp import ClientSession
from username_to_uuid import UsernameToUUID
from datetime import date

today = date.today()


conn = sqlite3.connect('bot/data/accounts.db')

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
            categories = await asyncPostInfo("https://maro.skybrokers.xyz/api/networth/categories", {"data": profile}, session)
        if categories['status'] == 404:
            embed = discord.Embed()
            embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
            embed.add_field(name='Error `API Disabled`', value=f"{categories['cause']}", inline=True)
            await message.edit(embed=embed)
            return
        networth = categories['data']['networth']
        purse = categories['data']['purse']
        sacks = categories['data']['sacks']
        bank = round(float(("%.17f" % data['profiles'][fcount]['banking']['balance']).rstrip('0').rstrip('.')))

        embed = discord.Embed(
            title=f"{player}'s total networth ",
            description=f'> **{round(networth + purse + sacks + bank):,}**',
            colour=discord.Colour.dark_gray() 
        )

        embed.set_footer(text=f"Profile: {data['profiles'][fcount]['cute_name']} {today}")
        embed.set_thumbnail(url=f'https://mc-heads.net/head/{player}')
        try:
            embed.add_field(name = "Purse Value", value = f"`{round(purse):,}`", inline = False)
            embed.add_field(name = "Bank Value", value = f"`{round(bank):,}`", inline = True)
            embed.add_field(name = f"Storage Value ▹ {round(categories['data']['categories']['storage']['total']):,}", value=f"""
            > Highest value item
            {categories['data']['categories']['storage']['top_items'][0]['name']} ▹ `{categories['data']['categories']['storage']['top_items'][0]['price']:,}`
            """, inline = False)
        except:
            pass
        
        try:
            embed.add_field(name = f"Enderchest Value ▹ {round(categories['data']['categories']['enderchest']['total']):,}", value=f"""
            > Highest value item
            {categories['data']['categories']['enderchest']['top_items'][0]['name']} ▹ `{categories['data']['categories']['enderchest']['top_items'][0]['price']:,}`
            """, inline = False)
        except:
            pass

        try:
            embed.add_field(name = f"Inventory Value ▹ {round(categories['data']['categories']['inventory']['total']):,}", value=f"""
            > Highest value item
            {categories['data']['categories']['inventory']['top_items'][0]['name']} ▹ `{categories['data']['categories']['inventory']['top_items'][0]['price']:,}`
            """, inline = False)
        except:
            pass
        
        try:
            embed.add_field(name = f"Armor Value ▹ {round(categories['data']['categories']['armor']['total']):,}", value=f"""
            > Highest value item
            {categories['data']['categories']['armor']['top_items'][0]['name']} ▹ `{categories['data']['categories']['armor']['top_items'][0]['price']:,}`
            """, inline = False)
        except:
            pass
        
        try:
            embed.add_field(name = f"Wardrobe Value ▹ {round(categories['data']['categories']['wardrobe_inventory']['total']):,}", value=f"""
            > Highest value item
            {categories['data']['categories']['wardrobe_inventory']['top_items'][0]['name']} ▹ `{categories['data']['categories']['wardrobe_inventory']['top_items'][0]['price']:,}`
            """, inline = False)
        except:
            pass

        try:
            embed.add_field(name = f"Pets Value ▹ {round(categories['data']['categories']['pets']['total']):,}", value=f"""
            > Highest value item
            {categories['data']['categories']['pets']['top_items'][0]['name']} ▹ `{categories['data']['categories']['pets']['top_items'][0]['price']:,}`
            """, inline = False)
        except:
            pass

        try:
            embed.add_field(name = f"Talismans Value ▹ {round(categories['data']['categories']['talismans']['total']):,}", value=f"""
            > Highest value item
            {categories['data']['categories']['talismans']['top_items'][0]['name']} ▹ `{categories['data']['categories']['talismans']['top_items'][0]['price']:,}`
            """, inline = False)
        except:
            pass

        await message.edit(embed=embed)

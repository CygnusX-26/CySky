import discord
from discord.ext import commands
import requests
import json
from username_to_uuid import UsernameToUUID
import os
from aiohttp import ClientSession
import sqlite3

conn = sqlite3.connect('accounts.db')

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


class Auction(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['ah'])
    async def auction(self, ctx, player=None):
        # verification check
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
        fields = False
        embed2 = discord.Embed(
            title=f'Auction Info for {player}',
            description='Loading...',
            colour=discord.Colour.dark_gray()
        )
        message = await ctx.send(embed=embed2)

        try:
            converter = UsernameToUUID(player)
            uuid = converter.get_uuid()
            auction_data = getInfo('https://api.hypixel.net/skyblock/auctions')
            pages = int(auction_data['totalPages'])
            embed = discord.Embed(
                title=f'Auction Info for {player}',
                colour=discord.Colour.dark_gray()
            )

            async with ClientSession() as session:
                for j in range(pages):
                    auction_data = await asyncGetInfo(f'https://api.hypixel.net/skyblock/auctions?page={j}', session)
                    for i in range(len(auction_data['auctions'])):
                        if auction_data['auctions'][i]['auctioneer'] == uuid:
                            embed.add_field(name=f"__{auction_data['auctions'][i]['item_name']}__", value=f"""
                            `Rarity` ▹ {auction_data['auctions'][i]['tier']}
                            `Starting Bid` ▹ {auction_data['auctions'][i]['starting_bid']:,}
                            `Highest Bid` ▹ {auction_data['auctions'][i]['highest_bid_amount']:,}
                            """, inline=False)
                            fields = True

        except:
            embed = discord.Embed()
            embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
            embed.add_field(name='Error', value=f"""Uh oh! Looks like the player you were searching for couldn't be found... 
            Check your spelling! For further information and a list of player auctions, you can click [here](https://api.hypixel.net/skyblock/auctions_ended).""", inline=True)
        if fields:
            await message.edit(embed=embed)
        else:
            embed.add_field(
                name=f'No ongoing auctions for {player}', value=f"For further information you can view a list of all auctions [here](https://api.hypixel.net/skyblock/auctions_ended).", inline=True)
            await message.edit(embed=embed)

import discord
from discord.ext import commands
import requests
import json
from username_to_uuid import UsernameToUUID
import os
from aiohttp import ClientSession
import sqlite3
from discord import app_commands

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



class Auction(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "auction", description= "Checks auction info for a given player")
    @app_commands.describe(player = "The player to check auction info for, can be none if verified")
    async def auction(self, interaction: discord.Interaction, player:str=None) -> None:
        # verification check
        if (player == None):
            c.execute(f"SELECT * FROM accounts")
            check = c.fetchall()
            user = interaction.user.id
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
                await interaction.response.send_message(embed=embed)
                return
        fields = False
        await interaction.response.defer()
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
            await interaction.followup.send(embed=embed)
        else:
            embed.add_field(name=f'No ongoing auctions for {player}', value=f"For further information you can view a list of all auctions [here](https://api.hypixel.net/skyblock/auctions_ended).", inline=True)
            await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Auction(bot))

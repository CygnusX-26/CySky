import discord
from discord.ext import commands
import requests
from aiohttp import ClientSession
import os
from username_to_uuid import UsernameToUUID
import sqlite3
from discord import app_commands

from datetime import date

today = date.today()

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

# methods for sql


def getUser(id, mcname):
    c.execute(
        f"SELECT * FROM accounts WHERE id = {id} AND mcname = ?", (mcname,))
    return c.fetchone()


def insertUser(id, mcname):
    with conn:
        c.execute(f"INSERT INTO accounts VALUES ({id}, ?)", (mcname,))


def removeUser(id):
    with conn:
        c.execute(f"DELETE from accounts WHERE id = {id}")


class Verify(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='verify', description='Links your minecraft account to your discord account')
    @app_commands.describe(username = "The minecraft account you want to link to your discord account")
    async def verify(self, interaction: discord.Interaction, username:str=None):
        if username == None:
            embed = discord.Embed()
            embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
            embed.add_field(name='Error `couldnt resolve username`', value=f"""Uh oh! The player you were searching for couldn't be found... 
            Check your spelling! For further information and a list of players, you can click [here](https://namemc.com/).""", inline=True)
            await interaction.response.send_message(embed=embed)
            return
        await interaction.response.defer()
        try:

            converter = UsernameToUUID(f'{username}')
            uuid = converter.get_uuid()
            async with ClientSession() as session:
                profile_data = await asyncGetInfo(f'https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}', session)
            social = profile_data['player']['socialMedia']['links']['DISCORD']
            print(social)
            if (not(social == (interaction.user.name + "#" + interaction.user.discriminator))):
                raise ValueError('A very specific bad thing happened.')
        except:
            embed = discord.Embed()
            embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
            embed.add_field(name='Error `Unlinked accounts`', value=f"""Uh oh! The player you were searching for couldn't be found or doesn't have their hypixel account linked to your discord account! 
            Give the API a while to update after linking.""", inline=True)
            await interaction.followup.send(embed=embed)
            return

        c.execute(f"SELECT * FROM accounts")
        check = c.fetchall()
        user = interaction.user.id
        if len(check) == 0:
            insertUser(user, username)
            embed = discord.Embed(
            title='Success!',
            colour=discord.Color.default()
            )
            embed.add_field(
            name='`Verified!`', value=f"""{interaction.user.mention} has been successfully linked to {username}""", inline=True)
            embed.set_footer(
            text=f'Verified: {today}', icon_url='https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/20/Powered_Redstone_Repeater_Delay_3_%28S%29_BE2.png/revision/latest?cb=20210329195117')
            await interaction.followup.send(embed=embed)
            return
        for i in range(len(check)):
            if user in check[i]:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(name='Error `Already Verified`', value=f"""Uh oh! Looks like the discord account you are using has already been verified. 
                Check your spelling or unverify yourself with &unverify""", inline=True)
                await interaction.followup.send(embed=embed)
                return
        insertUser(user, username)
        embed = discord.Embed(
            title='Success!',
            colour=discord.Color.default()
        )
        embed.add_field(
            name='`Verified!`', value=f"""{interaction.user.mention} has been successfully linked to {username}""", inline=True)
        embed.set_footer(
            text=f'Verified: {today}', icon_url='https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/20/Powered_Redstone_Repeater_Delay_3_%28S%29_BE2.png/revision/latest?cb=20210329195117')
        await interaction.followup.send(embed=embed)

    @app_commands.command(name='unverify', description='Unlinks your minecraft account from your discord account')
    @app_commands.describe(username = "The minecraft account you want to unlink from your discord account")
    async def unverify(self, interaction: discord.Interaction, username:str=None):
        c.execute(f"SELECT * FROM accounts")
        check = c.fetchall()
        user = interaction.user.id
        await interaction.response.defer()
        if username == None:
            for i in range(len(check)):
                if user in check[i]:
                    embed = discord.Embed()
                    embed.add_field(name='Success! `Unverified!`',
                                    value=f"""Successfully unverified {interaction.user.mention}""", inline=True)
                    removeUser(user)
                    await interaction.followup.send(embed=embed)
                    return
        if len(check) == 0:
            return
        for i in range(len(check)):
            if user in check[i] and username in check[i]:
                embed = discord.Embed()
                embed.add_field(name='Success! `Unverified!`',
                                value=f"""Successfully unverified {username}""", inline=True)
                removeUser(user)
                await interaction.followup.send(embed=embed)
                return
        embed = discord.Embed()
        embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
        embed.add_field(name='Error `Unlinked`',
                        value=f"""Your discord account isn't linked with this Minecraft account!""", inline=True)
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Verify(bot))
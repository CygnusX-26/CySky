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


class Weight(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['we'])
    async def weight(self, ctx, playerName=None, profile=None):
        dungeons = False
        slayer = False
        skill = False

        # Verification Check
        if (playerName == None):
            c.execute(f"SELECT * FROM accounts")
            check = c.fetchall()
            user = ctx.message.author.id
            if len(check) == 0:
                return
            for i in range(len(check)):
                if user in check[i]:
                    playerName = getUser(user, check[i][1])[1]
            if playerName == None:
                embed = discord.Embed()
                embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
                embed.add_field(name='Error `Unverified`', value=f"""Uh oh! Looks like the discord account you are using has not been verified. 
                Link your minecraft account with s/verify [accountname], give the API a bit before trying again""", inline=True)
                await ctx.send(embed=embed)
                return

        embed2 = discord.Embed(
            title=f'Weight for {playerName}',
            description='Calculating...',
            colour=discord.Colour.dark_gray()
        )
        message = await ctx.send(embed=embed2)

        converter = UsernameToUUID(f'{playerName}')
        uuid = converter.get_uuid()

        # try:
        async with ClientSession() as session:
            if profile == None:
                profile_data = await asyncGetInfo(f'https://hypixel-api.senither.com/v1/profiles/{uuid}/weight?key={API_KEY}', session)
            else:
                profile_data = await asyncGetInfo(f'https://hypixel-api.senither.com/v1/profiles/{uuid}/{profile}?key={API_KEY}', session)

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
        profile_name = data['name']
        skills = data['skills']
        if not(skills == None):
            skill = True
        if skills['apiEnabled'] == False:
            embed = discord.Embed()
            embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
            embed.add_field(name='Error `API DISABLED`', value=f"""Uh oh! Looks like the player or profile you were searching for doesn't have their API turned on... 
            For further information, you can click [here](https://sky.shiiyu.moe/api/v2/profile/{playerName}).""", inline=True)
            await message.edit(embed=embed)
            return
        slayers = data['slayers']
        if not(slayers == None):
            slayer = True
        classes = data['dungeons']
        if not(classes == None):
            catacombs = classes['types']['catacombs']
            dungeons_classes = data['dungeons']['classes']
            dungeons = True

        embed = discord.Embed(
            title=f'Weight for {playerName} on {profile_name}',
            description=f"""> Total weight for **{playerName}** on **{profile_name}** is **{round(data['weight'], 2)}** (**+ {round(data['weight_overflow'], 2)}** Overflow)
            > Total Weight With Overflow: **{round(data['weight'] + data['weight_overflow'], 2)}**""",
            colour=discord.Colour.dark_grey()
        )
        embed.set_footer(text=f'{profile_name}')
        embed.set_thumbnail(url=f'https://mc-heads.net/head/{playerName}')
        if skill:
            embed.add_field(name=f"Skills: {round(skills['weight'], 2)} (+ {round(skills['weight_overflow'], 2)} Overflow)", value=f"""
            <:taming:912112891073822770> `Taming` {round(skills['taming']['level'], 2)} ▹ Weight: {round(skills['taming']['weight'], 2)} ▹ Overflow: {round(skills['taming']['weight_overflow'], 2)}
            <:farming:912111478025379871> `Farming` {round(skills['farming']['level'], 2)} ▹ Weight: {round(skills['farming']['weight'], 2)} ▹ Overflow: {round(skills['farming']['weight_overflow'], 2)}
            <:mining:912112891157696562> `Mining` {round(skills['mining']['level'], 2)} ▹ Weight: {round(skills['mining']['weight'], 2)} ▹ Overflow: {round(skills['mining']['weight_overflow'], 2)}
            <:combat:912112890977337395> `Combat` {round(skills['combat']['level'], 2)} ▹ Weight: {round(skills['combat']['weight'], 2)} ▹ Overflow: {round(skills['combat']['weight_overflow'], 2)}
            <:foraging:912112891182850159> `Foraging` {round(skills['foraging']['level'], 2)} ▹ Weight: {round(skills['foraging']['weight'], 2)} ▹ Overflow: {round(skills['foraging']['weight_overflow'], 2)}
            <:fishing:912112891086389288> `Fishing` {round(skills['fishing']['level'], 2)} ▹ Weight: {round(skills['fishing']['weight'], 2)} ▹ Overflow: {round(skills['fishing']['weight_overflow'], 2)}
            <:enchanting:912112891119951882> `Enchanting` {round(skills['enchanting']['level'], 2)} ▹ Weight: {round(skills['enchanting']['weight'], 2)} ▹ Overflow: {round(skills['enchanting']['weight_overflow'], 2)}
            <:alchemy:912112891140927518> `Alchemy` {round(skills['alchemy']['level'], 2)} ▹ Weight: {round(skills['alchemy']['weight'], 2)} ▹ Overflow: {round(skills['alchemy']['weight_overflow'], 2)}
            """, inline=False)
        else:
            embed.add_field(name=f"Skills: {0} (+ {round(skills['weight_overflow'], 2)} Overflow)", value=f"""
            <:taming:912112891073822770> `Taming` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:farming:912111478025379871> `Farming` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:mining:912112891157696562> `Mining` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:combat:912112890977337395> `Combat` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:foraging:912112891182850159> `Foraging` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:fishing:912112891086389288> `Fishing` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:enchanting:912112891119951882> `Enchanting` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:alchemy:912112891140927518> `Alchemy` {0} ▹ Weight: {0} ▹ Overflow: {0}
            """, inline=False)

        if slayer:
            embed.add_field(name=f"Slayers: {round(slayers['weight'], 2)} (+ {round(slayers['weight_overflow'], 2)} Overflow)", value=f"""
            <:revenant:912115179372806164> `Revenant` {round(slayers['bosses']['revenant']['level'], 2)} ▹ Weight: {round(slayers['bosses']['revenant']['weight'], 2)} ▹ Overflow: {round(slayers['bosses']['revenant']['weight_overflow'], 2)}
            <:tara:912115179377029140> `Tarantula` {round(slayers['bosses']['tarantula']['level'], 2)} ▹ Weight: {round(slayers['bosses']['tarantula']['weight'], 2)} ▹ Overflow: {round(slayers['bosses']['tarantula']['weight_overflow'], 2)}
            <:sven:912115179343474718> `Sven` {round(slayers['bosses']['sven']['level'], 2)} ▹ Weight: {round(slayers['bosses']['sven']['weight'], 2)} ▹ Overflow: {round(slayers['bosses']['sven']['weight_overflow'], 2)}
            <:enderman:912115179712577576> `Enderman` {round(slayers['bosses']['enderman']['level'], 2)} ▹ Weight: {round(slayers['bosses']['enderman']['weight'], 2)} ▹ Overflow: {round(slayers['bosses']['enderman']['weight_overflow'], 2)}
            """, inline=False)
        else:
            embed.add_field(name=f"Slayers: {0} (+ {0} Overflow)", value=f"""
            <:revenant:912115179372806164> `Revenant` {0} ▹ Weight: {round(slayers['bosses']['revenant']['weight'], 2)} ▹ Overflow: {0}
            <:tara:912115179377029140> `Tarantula` {0} ▹ Weight: {round(slayers['bosses']['tarantula']['weight'], 2)} ▹ Overflow: {0}
            <:sven:912115179343474718> `Sven` {0} ▹ Weight: {round(slayers['bosses']['sven']['weight'], 2)} ▹ Overflow: {0}
            <:enderman:912115179712577576> `Enderman` {0} ▹ Weight: {round(slayers['bosses']['enderman']['weight'], 2)} ▹ Overflow: {0}
            """, inline=False)

        if dungeons:
            embed.add_field(name=f'Dungeons: {round(catacombs["weight"] + classes["weight"])} (+ {round(catacombs["weight_overflow"] + classes["weight_overflow"])} Overflow)', value=f"""
            <:catacombs:912115179062452256> `Catacombs` {round(catacombs["level"], 2)} ▹ Weight: {round(catacombs["weight"], 2)} ▹ Overflow: {round(catacombs["weight_overflow"], 2)}
            <:healer:912115179385413642> `Healer` {round(dungeons_classes['healer']['level'], 2)} ▹ Weight: {round(dungeons_classes['healer']['weight'], 2)} ▹ Overflow: {round(dungeons_classes['healer']['weight_overflow'], 2)}
            <:mage:912115179347640360> `Mage` {round(dungeons_classes['mage']['level'], 2)} ▹ Weight: {round(dungeons_classes['mage']['weight'], 2)} ▹ Overflow: {round(dungeons_classes['mage']['weight_overflow'], 2)}
            <:berserker:912115179003732099> `Berserker` {round(dungeons_classes['berserker']['level'], 2)} ▹ Weight: {round(dungeons_classes['berserker']['weight'], 2)} ▹ Overflow: {round(dungeons_classes['berserker']['weight_overflow'], 2)}
            <:tank:912115179372810270> `Tank` {round(dungeons_classes['tank']['level'], 2)} ▹ Weight: {round(dungeons_classes['tank']['weight'], 2)} ▹ Overflow: {round(dungeons_classes['tank']['weight_overflow'], 2)}
            <:archer:912115179431559248> `Archer` {round(dungeons_classes['archer']['level'], 2)} ▹ Weight: {round(dungeons_classes['archer']['weight'], 2)} ▹ Overflow: {round(dungeons_classes['archer']['weight_overflow'], 2)}
            """, inline=False)
        else:
            embed.add_field(name=f'Dungeons: {0} (+ {0} Overflow)', value=f"""
            <:catacombs:912115179062452256> `Catacombs` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:healer:912115179385413642> `Healer` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:mage:912115179347640360> `Mage` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:berserker:912115179003732099> `Berserker` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:tank:912115179372810270> `Tank` {0} ▹ Weight: {0} ▹ Overflow: {0}
            <:archer:912115179431559248> `Archer` {0} ▹ Weight: {0} ▹ Overflow: {0}
            """, inline=False)

        await message.edit(embed=embed)
        # except:
        #     embed = discord.Embed()
        #     embed.set_thumbnail(url=f'https://sky.shiiyu.moe/item/BARRIER')
        #     embed.add_field(name='Error', value=f"""Uh oh! Looks like the player or profile you were searching for couldn't be found...
        #     Check your spelling! For further information, you can click [here](https://sky.shiiyu.moe/api/v2/profile/{playerName}).""", inline=True)
        #     await message.edit(embed=embed)

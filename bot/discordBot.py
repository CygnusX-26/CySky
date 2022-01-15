import discord
import os
from discord.ext import commands
from cogs.Verify import Verify
from cogs.Profiles import Profiles
from cogs.Weight import Weight
from cogs.BazaarTop import BazaarTop
from cogs.Auction import Auction
from cogs.Bazaar import Bazaar
from cogs.Bot import bot
from cogs.LastestUpdate import LatestUpdate
from cogs.Networth import Networth
import sqlite3
from os.path import join, dirname, abspath

db_path = join(dirname(dirname(abspath(__file__))), 'bot/data/accounts.db')

conn = sqlite3.connect(db_path)

c = conn.cursor()

intents = discord.Intents.all()
client = commands.Bot(command_prefix= os.getenv("DISCORD_BOT_PREFIX"), intents=intents)
client.remove_command('help')


# creates a new user table if one doesn't currently exist
try:
    c.execute("""CREATE TABLE accounts (
            id integer,
            mcname text
            )""")

except:
    pass


client.add_cog(bot(client))
client.add_cog(Bazaar(client))
client.add_cog(BazaarTop(client))
client.add_cog(Auction(client))
client.add_cog(LatestUpdate(client))
client.add_cog(Weight(client))
client.add_cog(Profiles(client))
client.add_cog(Verify(client))
client.add_cog(Networth(client))

client.run(os.getenv("DISCORD_BOT_TOKEN"))

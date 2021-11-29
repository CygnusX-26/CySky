import discord
import os
from discord.ext import commands
from bot.cogs.Verify import Verify
from bot.cogs.Profiles import Profiles
from bot.cogs.Weight import Weight
from bot.cogs.BazaarTop import BazaarTop
from bot.cogs.Auction import Auction
from bot.cogs.Bazaar import Bazaar
from bot.cogs.Bot import bot
from bot.cogs.LastestUpdate import LatestUpdate
import sqlite3

conn = sqlite3.connect('accounts.db')

c = conn.cursor()

intents = discord.Intents.all()
client = commands.Bot(command_prefix='s/', intents=intents)
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

client.run(os.getenv("DISCORD_BOT_TOKEN"))

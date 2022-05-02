import asyncio
import aiohttp
import discord
import os
from discord.ext import commands
import sqlite3
from os.path import join, dirname, abspath

db_path = join(dirname(dirname(abspath(__file__))), 'bot/data/accounts.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

class SkyBlockBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv("DISCORD_BOT_PREFIX")),
            description='SkyBlock Bot',
            intents=discord.Intents.default(),
            application_id = 277588583693680640)
    
    async def load_extensions(self):
        for filename in os.listdir("bot/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def setup_hook(self):
        await self.load_extensions()
        await bot.tree.sync()
        

# creates a new user table if one doesn't currently exist
try:
    c.execute("""CREATE TABLE accounts (
            id integer,
            mcname text
            )""")

except:
    pass

bot = SkyBlockBot()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

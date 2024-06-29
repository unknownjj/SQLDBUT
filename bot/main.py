import sys
import os
import logging
import discord
from discord.ext import commands
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

logger.info("Starting bot initialization")
logger.info(f"Python path: {sys.path}")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Parent directory added: {parent_dir}")

# Now try to import
try:
    from config import DISCORD_TOKEN
    from database.db_operations import init_db as db_init
    logger.info("Imports successful")
except ImportError as e:
    logger.error(f"Import error: {e}")
    sys.exit(1)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self):
        logger.info("Setting up bot...")
        await self.load_extension('bot.cogs.calls')
        await self.load_extension('bot.cogs.watchlist')
        await self.load_extension('bot.cogs.admin')
        logger.info("All cogs loaded")

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Connected to {len(self.guilds)} guilds')
        
        # Initialize database
        db_init()
        
        # Sync commands
        logger.info("Syncing commands...")
        await self.tree.sync()
        logger.info("Commands synced")

        # Log all registered commands
        commands = await self.tree.fetch_commands()
        logger.info(f"Registered commands: {[command.name for command in commands]}")

async def main():
    bot = MyBot()
    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
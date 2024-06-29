import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import discord
from discord import app_commands
from discord.ext import commands
from bot.utils.api import get_token_info
from bot.utils.embeds import create_watchlist_embed
from database.db_operations import add_to_watchlist, remove_from_watchlist, get_watchlist

class Watchlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def watch(self, interaction: discord.Interaction, address: str):
        token_info = get_token_info(address)
        if not token_info:
            await interaction.response.send_message("Invalid token address.")
            return
        
        result = add_to_watchlist(interaction.user.id, token_info)
        if result:
            await interaction.response.send_message(f"Added {token_info['name']} to your watchlist.")
        else:
            await interaction.response.send_message("Failed to add token to watchlist. You may have reached the limit of 10 tokens.")

    @app_commands.command()
    async def remove_watch(self, interaction: discord.Interaction, symbol: str):
        result = remove_from_watchlist(interaction.user.id, symbol)
        if result:
            await interaction.response.send_message(f"Removed {symbol} from your watchlist.")
        else:
            await interaction.response.send_message("Failed to remove token from watchlist. It may not be in your watchlist.")

    @app_commands.command()
    async def watchlist(self, interaction: discord.Interaction):
        watchlist = get_watchlist(interaction.user.id)
        if watchlist:
            embed = create_watchlist_embed(watchlist, interaction.user.name)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Your watchlist is empty.")

    @app_commands.command()
    async def creep(self, interaction: discord.Interaction, member: discord.Member):
        watchlist = get_watchlist(member.id)
        if watchlist:
            embed = create_watchlist_embed(watchlist, member.name)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{member.name}'s watchlist is empty.")

async def setup(bot):
    await bot.add_cog(Watchlist(bot))
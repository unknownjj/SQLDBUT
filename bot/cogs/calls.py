import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import discord
from discord import app_commands
from discord.ext import commands
from bot.utils.api import get_token_info
from bot.utils.embeds import create_call_embed, create_leaderboard_embed
from database.db_operations import get_or_create_user, open_call, close_call, get_user_calls, get_leaderboard, toggle_duplicate_messages, add_to_watchlist, remove_from_watchlist, get_watchlist, export_calls, import_calls, export_watchlist, import_watchlist
from config import DUPLICATE_CHANNEL_ID

class Calls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Calls cog initialized")

    async def cog_load(self):
        logger.info("Calls cog loaded")

    @app_commands.command()
    async def call(self, interaction: discord.Interaction, address: str):
        token_info = get_token_info(address)
        if not token_info:
            await interaction.response.send_message("Invalid token address.")
            return
        
        call = open_call(interaction.user.id, token_info)
        if call:
            embed = create_call_embed(call, "Call Opened")
            await interaction.response.send_message(embed=embed)
            
            user = get_or_create_user(interaction.user.id)
            if user.duplicate_messages:
                duplicate_channel = self.bot.get_channel(DUPLICATE_CHANNEL_ID)
                if duplicate_channel:
                    await duplicate_channel.send(embed=embed)
        else:
            await interaction.response.send_message("Failed to open call. This token may already have an open call.")

    @app_commands.command()
    async def close_call(self, interaction: discord.Interaction, address: str):
        call = close_call(interaction.user.id, address)
        if call:
            embed = create_call_embed(call, "Call Closed")
            await interaction.response.send_message(embed=embed)
            
            user = get_or_create_user(interaction.user.id)
            if user.duplicate_messages:
                duplicate_channel = self.bot.get_channel(DUPLICATE_CHANNEL_ID)
                if duplicate_channel:
                    await duplicate_channel.send(embed=embed)
        else:
            await interaction.response.send_message("Failed to close call. You may not have an open call for this token.")

    @app_commands.command()
    async def my_calls(self, interaction: discord.Interaction):
        calls = get_user_calls(interaction.user.id)
        if calls:
            embeds = [create_call_embed(call, f"Call #{i+1}") for i, call in enumerate(calls)]
            await interaction.response.send_message(embeds=embeds)
        else:
            await interaction.response.send_message("You don't have any calls yet.")

    @app_commands.command()
    async def leaderboard(self, interaction: discord.Interaction):
        leaderboard_data = get_leaderboard()
        if leaderboard_data:
            embed = create_leaderboard_embed(leaderboard_data)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("No data available for the leaderboard yet.")

    @app_commands.command()
    async def toggle_duplicate_messages(self, interaction: discord.Interaction):
        new_status = toggle_duplicate_messages(interaction.user.id)
        await interaction.response.send_message(f"Duplicate messages have been {'enabled' if new_status else 'disabled'}.")

    @app_commands.command()
    async def check_calls(self, interaction: discord.Interaction, member: discord.Member):
        calls = get_user_calls(member.id)
        if calls:
            embeds = [create_call_embed(call, f"Call #{i+1}") for i, call in enumerate(calls)]
            await interaction.response.send_message(embeds=embeds)
        else:
            await interaction.response.send_message(f"{member.name} doesn't have any calls yet.")

# ... existing code ...

async def setup(bot):
    await bot.add_cog(Calls(bot))
    logger.info("Calls cog added to bot")


import logging


import discord
from discord import app_commands
from discord.ext import commands
from config import OWNER_ID
from database.db_operations import export_calls, import_calls, export_watchlist, import_watchlist

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, interaction: discord.Interaction):
        return interaction.user.id == OWNER_ID

    @app_commands.command()
    async def export_calls(self, interaction: discord.Interaction):
        data = export_calls()
        await interaction.user.send(file=discord.File(data, filename="calls_export.csv"))
        await interaction.response.send_message("Calls data exported to DM.", ephemeral=True)

    @app_commands.command()
    async def import_calls(self, interaction: discord.Interaction):
        await interaction.response.send_message("Please send the CSV file to import.", ephemeral=True)
        
        def check(m):
            return m.author.id == interaction.user.id and m.channel.type == discord.ChannelType.private

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=300.0)
            if msg.attachments:
                file_content = await msg.attachments[0].read()
                import_calls(file_content)
                await interaction.followup.send("Calls data imported successfully.", ephemeral=True)
            else:
                await interaction.followup.send("No file received. Import cancelled.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Import timed out. Please try again.", ephemeral=True)

    @app_commands.command()
    async def export_watchlist(self, interaction: discord.Interaction):
        data = export_watchlist()
        await interaction.user.send(file=discord.File(data, filename="watchlist_export.csv"))
        await interaction.response.send_message("Watchlist data exported to DM.", ephemeral=True)

    @app_commands.command()
    async def import_watchlist(self, interaction: discord.Interaction):
        await interaction.response.send_message("Please send the CSV file to import.", ephemeral=True)
        
        def check(m):
            return m.author.id == interaction.user.id and m.channel.type == discord.ChannelType.private

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=300.0)
            if msg.attachments:
                file_content = await msg.attachments[0].read()
                import_watchlist(file_content)
                await interaction.followup.send("Watchlist data imported successfully.", ephemeral=True)
            else:
                await interaction.followup.send("No file received. Import cancelled.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("Import timed out. Please try again.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
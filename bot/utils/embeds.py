import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import discord

def create_call_embed(call, title):
    embed = discord.Embed(title=title, color=discord.Color.blue())
    embed.add_field(name="Token", value=f"[{call.token.name} ({call.token.chain})](https://dexscreener.com/{call.token.chain}/{call.token.address})", inline=False)
    embed.add_field(name="Address", value=f"`{call.token.address}`", inline=False)
    embed.add_field(name="Entry Price", value=f"${call.entry_price:.4f}", inline=True)
    embed.add_field(name="Entry FDV", value=f"${call.entry_fdv:,.0f}", inline=True)
    if call.close_price:
        embed.add_field(name="Close Price", value=f"${call.close_price:.4f}", inline=True)
        embed.add_field(name="Close FDV", value=f"${call.close_fdv:,.0f}", inline=True)
        multiple = call.close_fdv / call.entry_fdv
        embed.add_field(name="Multiple", value=f"{multiple:.2f}x", inline=True)
    embed.set_footer(text=f"Called by {call.user.discord_id}")
    return embed

def create_watchlist_embed(watchlist, username):
    embed = discord.Embed(title=f"{username}'s Watchlist", color=discord.Color.green())
    for item in watchlist:
        token_info = get_token_info(item.token.address)
        if token_info:
            embed.add_field(
                name=f"{item.token.name} ({item.token.chain})",
                value=f"[{item.token.symbol}](https://dexscreener.com/{item.token.chain}/{item.token.address})\n"
                      f"Price: ${token_info['price']:.4f}\n"
                      f"FDV: ${token_info['fdv']:,.0f}\n"
                      f"24h Volume: ${token_info['volume24h']:,.0f}\n"
                      f"24h Change: {token_info['priceChange24h']:.2f}%",
                inline=False
            )
    return embed

def create_leaderboard_embed(leaderboard):
    embed = discord.Embed(title="Leaderboard", color=discord.Color.gold())
    for rank, (discord_id, avg_performance, total_calls) in enumerate(leaderboard, start=1):
        embed.add_field(
            name=f"#{rank} {discord_id}",
            value=f"Average Performance: {avg_performance:.2f}x\n"
                  f"Total Calls: {total_calls}",
            inline=False
        )
    return embed
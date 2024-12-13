#!/usr/bin/env python3

import os
import json
import asyncio
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser("~/priceTrackBot/.env"))
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is not set or could not be loaded.")

# Load configuration file
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../data/config.json")

try:
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("Config file not found. Please ensure ../data/config.json exists.")

# Extract settings from config
UPDATE_INTERVAL = config.get("update_interval", 14400)  # Default to 4 hours if not set
DEFAULT_UPDATES_CHANNEL = config.get("default_updates_channel", "price-tracking")
COMMAND_PREFIX = config.get("command_prefix", "pt!")

# Track the start time for uptime calculation
start_time = time.time()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user} (ID: {bot.user.id})")
    bot.loop.create_task(auto_refresh())

@bot.command()
async def uptime(ctx):
    """Command to display the bot's uptime"""
    uptime_seconds = time.time() - start_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    await ctx.send(f"Bot uptime: {hours}h {minutes}m {seconds}s")

async def auto_refresh():
    """Automatically refresh the item list at the configured interval."""
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(UPDATE_INTERVAL)  # Use update interval from config
        channel = discord.utils.get(bot.get_all_channels(), name=DEFAULT_UPDATES_CHANNEL)
        if channel:
            await channel.send("Refreshing prices...")
            cog = bot.get_cog("ItemManager")
            if cog:
                await cog.refresh_list(channel)
        else:
            print(f"Warning: Channel '{DEFAULT_UPDATES_CHANNEL}' not found. Skipping update.")

# Main entry point for the bot
async def main():
    """Main entry point for the bot."""

    try:
        # Load cogs (extensions)
        await bot.load_extension("commands.item_manager")
        await bot.load_extension("commands.config_manager")
        await bot.load_extension("events.on_message")

        # Run the bot
        await bot.start(TOKEN)

    except KeyboardInterrupt:
        print("Bot has been stopped with CTRL + C.")
    except asyncio.CancelledError:
        print("Bot's task was cancelled.")

    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())  # Run the async main function

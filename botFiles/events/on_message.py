#!/usr/bin/env python3

import time
from discord.ext import commands

# Track uptime
start_time = time.time()

class OnMessage(commands.Cog):
    """Handles bot mentions and related events."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        print(f"Message received: {message.content}")
        # Ignore messages from the bot itself
        if message.author == bot.user:
            return

        # Check if the bot is mentioned
        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            uptime = time.time() - start_time
            uptime_formatted = f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m {int(uptime % 60)}s"
            await message.channel.send(f"Hello, {message.author.mention}! I’ve been online for {uptime_formatted}.")

        # Ensure other commands are processed
        await self.bot.process_commands(message)

# Required setup function (must be async)
async def setup(bot):
    await bot.add_cog(OnMessage(bot))  # This must be awaited


import json
from discord.ext import commands

# Path to the configuration file
CONFIG_FILE = "../data/config.json"

class ConfigManager(commands.Cog):
    """Handles bot configuration."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="config")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        """Interactive configuration command."""
        # Load existing configuration
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        # Step 1: Channel for updates
        await ctx.send("Please mention the channel where updates should be sent (e.g., #updates):")
        
        def check_channel(message):
            return message.channel == ctx.channel and message.author == ctx.author

        channel_msg = await self.bot.wait_for("message", check=check_channel)
        if channel_msg.channel_mentions:
            channel = channel_msg.channel_mentions[0]
            config["default_updates_channel"] = channel.name
            await ctx.send(f"✅ Updates will be sent to {channel.mention}.")
        else:
            await ctx.send("❌ No valid channel mentioned. Keeping the existing setting.")

        # Step 2: Default currency
        await ctx.send("Please enter the default currency (e.g., USD, EUR):")
        currency_msg = await self.bot.wait_for("message", check=check_channel)
        config["default_currency"] = currency_msg.content.upper()
        await ctx.send(f"✅ Default currency set to {currency_msg.content.upper()}.")

        # Step 3: Update interval
        await ctx.send("Please enter the update interval in seconds (e.g., 14400 for 4 hours):")
        interval_msg = await self.bot.wait_for("message", check=check_channel)
        try:
            interval = int(interval_msg.content)
            if interval > 0:
                config["update_interval"] = interval
                await ctx.send(f"✅ Update interval set to {interval} seconds.")
            else:
                raise ValueError
        except ValueError:
            await ctx.send("❌ Invalid interval. Keeping the existing setting.")

        # Save the updated configuration
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        await ctx.send("⚙️ Configuration updated successfully!")

    @config.error
    async def config_error(self, ctx, error):
        """Handle errors for the config command."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have the required permissions to use this command.")
        else:
            await ctx.send(f"❌ An error occurred: {str(error)}")


# Required setup function
async def setup(bot):
    await bot.add_cog(ConfigManager(bot))

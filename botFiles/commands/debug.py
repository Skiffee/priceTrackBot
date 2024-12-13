from discord.ext import commands

class Debug(commands.Cog):
    """Debug commands for the bot."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hw")
    async def hello_world(self, ctx):
        """Respond with 'Hello World'."""
        await ctx.send("Hello World!")

def setup(bot):
    bot.add_cog(Debug(bot))

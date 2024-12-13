import json
import discord
from discord.ext import commands
from utils.fetch_price import fetch_price

ITEMS_FILE = "../data/items.json"  # Path to the JSON file


class ItemManager(commands.Cog):
    """Manages items for price tracking."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add")
    async def add_item(self, ctx, category, alias, url, alert_price: float, website):
        """Add an item to the tracking list."""
        try:
            # Fetch current price
            selector = ".price"  # Update with the correct CSS selector for the target website
            current_price = fetch_price(url, selector)

            # Create the item
            item = {
                "category": category,
                "alias": alias,
                "url": url,
                "current_price": current_price,
                "alert_price": alert_price,
                "website": website,
                "user_id": ctx.author.id  # Store the user ID for alerts
            }

            # Save the item to JSON
            items = self.load_items()
            items.append(item)
            self.save_items(items)

            await ctx.send(f"✅ Item '{alias}' added successfully! Current price: ${current_price:.2f}")
        except Exception as e:
            await ctx.send(f"❌ Failed to add item: {str(e)}")

    @commands.command(name="refresh")
    async def refresh_list(self, ctx):
        """Manually refresh the list of items."""
        try:
            items = self.load_items()
            updated_items = []
            alerts = []

            for item in items:
                # Fetch updated price
                selector = ".price"  # Update as needed
                new_price = fetch_price(item["url"], selector)
                item["current_price"] = new_price

                # Check alert condition
                if new_price <= item["alert_price"]:
                    alerts.append((item["alias"], item["user_id"], new_price))

                updated_items.append(item)

            # Save the updated items
            self.save_items(updated_items)

            # Build embed for updated list
            embed = self.build_embed(updated_items)
            await ctx.send(embed=embed)

            # Send alerts
            for alias, user_id, price in alerts:
                user = await self.bot.fetch_user(user_id)
                if user:
                    await user.send(f"🚨 Price Alert: '{alias}' is now ${price:.2f}!")

        except Exception as e:
            await ctx.send(f"❌ Failed to refresh list: {str(e)}")

    @commands.command(name="list")
    async def list_items(self, ctx):
        """Display the current list of items."""
        items = self.load_items()
        embed = self.build_embed(items)
        await ctx.send(embed=embed)

    def load_items(self):
        """Load items from the JSON file."""
        try:
            with open(ITEMS_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_items(self, items):
        """Save items to the JSON file."""
        with open(ITEMS_FILE, "w") as f:
            json.dump(items, f, indent=4)

    def build_embed(self, items):
        """Build an embed to display the list of items."""
        embed = discord.Embed(title="Tracked Items", color=0x00FF00)
        for item in items:
            embed.add_field(
                name=item["alias"],
                value=(
                    f"[Link]({item['url']}) | **${item['current_price']:.2f}**\n"
                    f"Website: {item['website']}\n"
                    f"Category: {item['category']}\n"
                    f"Alert Price: ${item['alert_price']:.2f}"
                ),
                inline=False
            )
        return embed


async def setup(bot):
    await bot.add_cog(ItemManager(bot))

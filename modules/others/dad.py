import disnake
from disnake.ext import commands
from typing import TYPE_CHECKING, cast, Any
if TYPE_CHECKING:
    from myfunctions.motor import MotorDbManager

class DadJokes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dad(self, ctx: commands.Context[Any]):
        motor = cast(
            "MotorDbManager",
            self.client.get_cog("MotorDbManager")
        )
        toggles = motor.get_collection_for_server("toggles", ctx.guild.id)

        dad_jokes = await toggles.find_one({"title": "Dad Jokes"})

        if not dad_jokes:
            new = False
            await toggles.insert_one({"title": "Dad Jokes", "enabled": new})
        else:
            new = not dad_jokes["enabled"]
            await toggles.replace_one({"title": "Dad Jokes"}, {"enabled": new})

        if new:
            await ctx.send(f"Dad jokes have been enabled")
        else:
            await ctx.send(f"Dad jokes have been disabled")


def setup(client: commands.Bot):
    client.add_cog(DadJokes(client))

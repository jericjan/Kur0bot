from typing import TYPE_CHECKING, Any, Optional, Union, cast, TypedDict

import disnake
from disnake.ext import commands

if TYPE_CHECKING:
    from myfunctions.motor import MotorDbManager

class UserStat:
    def __init__(self, client: commands.Bot, guild_id: Union[str, int], author_id: int):
        motor = cast(
            "MotorDbManager", 
            client.get_cog("MotorDbManager")
        )
        self.stats_coll = motor.get_collection_for_server("stats", guild_id)
        self.author_id = author_id

    async def increment(self, stat_name: str, inc_amount: int):
        await self.stats_coll.update_one(
            {"user_id": self.author_id},
            {"$inc": {f"stats.{stat_name}": inc_amount}},
            upsert=True,
        )

class StatContents(TypedDict):
    user_id: int
    stats: dict[str, Any]

class Stats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    def get_user(self, guild_id: Union[str, int], author_id: int):
        return UserStat(self.client, guild_id, author_id)

    @commands.command()
    async def stats(self, ctx: commands.Context[Any], user: Optional[Union[disnake.User, disnake.Member]] = None):
        if user is None:
            user = ctx.author

        motor = cast(
            "MotorDbManager", 
            self.client.get_cog("MotorDbManager")
        )
        stats_coll = motor.get_collection_for_server(
            "stats", ctx.guild.id if ctx.guild else ctx.author.id
        )
        user_doc = cast(
            StatContents, 
            await stats_coll.find_one({"user_id": user.id})
        )

        if not user_doc:
            await ctx.send("No stats for this user atm. Sorry bud :(")
            return

        user_stats: dict[str, Any] = user_doc["stats"]

        final = ""

        def recurse(x: Union[str, dict[Any, Any]], depth: int):
            nonlocal final

            if not isinstance(x, dict):
                if x in user_stats:
                    final += f"{'  '*depth}- {x}\n"
                    recurse(user_stats[x], depth + 1)
                else:
                    final = final.rstrip()
                    final += f": **{x}**\n"
            else:
                for key in x.keys():
                    final += f"{'  '*depth}- {key}\n"
                    recurse(x[key], depth + 1)

            #    final += f"{' '*(depth+1)}- {user_stats[x]}\n"

        for key in user_stats.keys():
            recurse(key, 0)
        # await ctx.send(json.dumps(user_doc['stats'], indent=4))
        # await ctx.send(final)

        em = disnake.Embed(
            title=f"Stats for {user.display_name}:",
            description=final,
        )
        await ctx.send(embed=em)


def setup(client: commands.Bot):
    client.add_cog(Stats(client))

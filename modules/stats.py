from typing import TYPE_CHECKING, Any, Optional, cast

import disnake
from disnake.ext import commands

if TYPE_CHECKING:
    from myfunctions.motor import MotorDbManager, StatContents
class UserStat:
    def __init__(self, client: commands.Bot, guild_id: str | int, author_id: int):
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



class Stats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    def get_user(self, guild_id: str | int, author_id: int):
        return UserStat(self.client, guild_id, author_id)

    @commands.command()
    async def stats(self, ctx: commands.Context[Any], user: Optional[disnake.User | disnake.Member] = None, filter: Optional[str] = ""):
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
            "StatContents", 
            await stats_coll.find_one({"user_id": user.id})
        )

        if not user_doc:
            await ctx.send("No stats for this user atm. Sorry bud :(")
            return

        user_stats: dict[str, Any] = user_doc["stats"]

        final = ""

        def recurse(x: str | dict[Any, Any], depth: int = 0, history: str = ""):
            nonlocal final

            if not isinstance(x, dict):
                if x in user_stats:
                    if filter and (filter not in history.lower() and filter not in x.lower()):
                        return
                    final += f"{'  '*depth}- {x}\n"
                    recurse(user_stats[x], depth + 1, history + f"{x}.")
                else:
                    final = final.rstrip()
                    final += f": **{x}**\n"
            else:
                for key in x.keys():
                    print(history, key)
                    if filter and (filter not in history.lower() and filter not in key.lower()):
                        return                    
                    final += f"{'  '*depth}- {key}\n"
                    recurse(x[key], depth + 1, history + f"{x}.")

            #    final += f"{' '*(depth+1)}- {user_stats[x]}\n"

        for key in user_stats.keys():
            recurse(key)
        # await ctx.send(json.dumps(user_doc['stats'], indent=4))
        # await ctx.send(final)

        em = disnake.Embed(
            title=f"Stats for {user.display_name}:",
            description=final if final else "No stats found for search query.",
        )
        await ctx.send(embed=em)


def setup(client: commands.Bot):
    client.add_cog(Stats(client))

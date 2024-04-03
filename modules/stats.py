import json

import disnake
from disnake.ext import commands


class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx, user: disnake.User = None):
        if not user:
            user = ctx.author

        motor = self.client.get_cog("MotorDbManager")
        stats_coll = motor.get_collection_for_server("stats", ctx.guild.id)
        user_doc = await stats_coll.find_one({"user_id": user.id})

        if not user_doc:
            await ctx.send("No stats for this user atm. Sorry bud :(")
            return

        user_stats = user_doc["stats"]

        final = ""

        def recurse(x, depth):
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


def setup(client):
    client.add_cog(Stats(client))

import os
from typing import Any

from disnake.ext import commands


class Karaoke(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def queue(self, ctx: commands.Context[Any]):
        guild_id = ctx.guild.id
        if os.path.exists(f"modules/others/karaoke_queue/{guild_id}.json"):
            with open(f"modules/others/karaoke_queue/{guild_id}.json") as f:
                singers_list = f.read()
            await ctx.send(f"Peeps in queue are:\n {singers_list}")
        else:
            await ctx.send("Empty. Add someone to the queue with 'k.addqueue <name>'")

    @commands.command()
    async def addqueue(self, ctx: commands.Context[Any], *names):
        guild_id = ctx.guild.id
        names = [x + "\n" for x in list(names)]
        with open(f"modules/others/karaoke_queue/{guild_id}.json", "a") as f:
            f.writelines(names)
        with open(f"modules/others/karaoke_queue/{guild_id}.json") as f:
            singers_list = f.read()
        await ctx.send(f"Peeps in queue are:\n {singers_list}")

    @commands.command()
    async def insertqueue(self, ctx: commands.Context[Any], singer, new_singer):
        guild_id = ctx.guild.id
        with open(f"modules/others/karaoke_queue/{guild_id}.json") as f:
            singers_list = f.readlines()
        singers_list = [x.strip() for x in singers_list]
        index = singers_list.index(singer)
        singers_list.insert(index + 1, new_singer)
        singers_list = [x + "\n" for x in singers_list]
        with open(f"modules/others/karaoke_queue/{guild_id}.json", "w") as f:
            f.writelines(singers_list)
        with open(f"modules/others/karaoke_queue/{guild_id}.json") as f:
            singers_list = f.read()
        await ctx.send(f"Peeps in queue are:\n {singers_list}")

    @commands.command()
    async def removequeue(self, ctx: commands.Context[Any], singer):
        guild_id = ctx.guild.id
        with open(f"modules/others/karaoke_queue/{guild_id}.json") as f:
            singers_list = f.readlines()
        singers_list = [x.strip() for x in singers_list]
        index = singers_list.index(singer)
        singers_list.pop(index)
        singers_list = [x + "\n" for x in singers_list]
        with open(f"modules/others/karaoke_queue/{guild_id}.json", "w") as f:
            f.writelines(singers_list)
        with open(f"modules/others/karaoke_queue/{guild_id}.json") as f:
            singers_list = f.read()
        await ctx.send(f"Peeps in queue are:\n {singers_list}")

    @commands.command()
    async def clearqueue(self, ctx: commands.Context[Any]):
        guild_id = ctx.guild.id
        open(f"modules/others/karaoke_queue/{guild_id}.json", "w").close()
        await ctx.send("Queue cleared!")


def setup(client: commands.Bot):
    client.add_cog(Karaoke(client))

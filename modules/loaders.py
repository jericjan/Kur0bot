import importlib
import sys

from disnake.ext import commands
from typing import Any

class Loaders(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.start_time = self.client.start_time
        self.log = self.client.log


    @commands.command(name="reload", aliases=["refresh"])
    @commands.is_owner()
    async def p_reload(self, ctx: commands.Context[Any], name):
        try:
            self.client.reload_extension(name)
        except commands.ExtensionNotLoaded:
            try:
                importlib.reload(sys.modules[name])
            except KeyError:
                await ctx.send("Could not find module")
                return
        await ctx.message.delete()
        await ctx.send(f"{name} reloaded!", delete_after=3.0)

    @commands.slash_command(name="reload")
    @commands.is_owner()
    async def s_reload(self, inter, name: str):
        """
        Reloads a module

        Parameters
        ----------
        name: The module to reload
        """
        self.client.reload_extension(name)
        await inter.response.send_message(f"{name} reloaded!", ephemeral=True)

    @commands.command(name="load")
    @commands.is_owner()
    async def p_load(self, ctx: commands.Context[Any], name):
        self.client.load_extension(name)
        await ctx.send(f"{name} loaded!")

    @commands.slash_command(name="load")
    @commands.is_owner()
    async def s_load(self, inter, name: str):
        """
        Loads a module

        Parameters
        ----------
        name: The module to load
        """
        self.client.load_extension(name)
        await inter.response.send_message(f"{name} loaded!", ephemeral=True)

    @commands.command(name="unload")
    @commands.is_owner()
    async def p_unload(self, ctx: commands.Context[Any], name):
        self.client.unload_extension(name)
        await ctx.send(f"{name} unloaded!")

    @commands.slash_command(name="unload")
    @commands.is_owner()
    async def s_unload(self, inter, name: str):
        """
        Unloads a module

        Parameters
        ----------
        name: The module to unload
        """
        self.client.unload_extension(name)
        await inter.response.send_message(f"{name} unloaded!", ephemeral=True)


def setup(client: commands.Bot):
    client.add_cog(Loaders(client))

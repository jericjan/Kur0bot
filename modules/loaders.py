import importlib
import sys
from typing import Any, TYPE_CHECKING

import disnake
from disnake.ext import commands
from main import MyBot

if TYPE_CHECKING:
    from main import MyBot

class Loaders(commands.Cog):
    def __init__(self, client: "MyBot"):
        self.client = client
        self.start_time = self.client.start_time
        self.log = self.client.log


    @commands.command(name="reload", aliases=["refresh"])
    @commands.is_owner()
    async def p_reload(self, ctx: commands.Context[Any], name: str):
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
    async def s_reload(self, inter: disnake.ApplicationCommandInteraction[Any], name: str):
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
    async def p_load(self, ctx: commands.Context[Any], name: str):
        self.client.load_extension(name)
        await ctx.send(f"{name} loaded!")

    @commands.slash_command(name="load")
    @commands.is_owner()
    async def s_load(self, inter: disnake.ApplicationCommandInteraction[Any], name: str):
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
    async def p_unload(self, ctx: commands.Context[Any], name: str):
        self.client.unload_extension(name)
        await ctx.send(f"{name} unloaded!")

    @commands.slash_command(name="unload")
    @commands.is_owner()
    async def s_unload(self, inter: disnake.ApplicationCommandInteraction[Any], name: str):
        """
        Unloads a module

        Parameters
        ----------
        name: The module to unload
        """
        self.client.unload_extension(name)
        await inter.response.send_message(f"{name} unloaded!", ephemeral=True)


def setup(client: "MyBot"):
    client.add_cog(Loaders(client))

from disnake.ext import commands
import modules.events
import importlib


class Loaders(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.start_time = self.client.start_time
        self.log = self.client.log

    # def reload_module(self, name):
    # if name == "events":
    # try:
    # self.client.get_cog("Events").cog_unload()
    # self.client.remove_cog("Events")
    # except:
    # print("epic failure")
    # importlib.reload(modules.events)
    # self.client.add_cog(modules.events.Events( self.client, self.start_time, self.log))
    # else:
    # self.client.reload_extension(name)

    @commands.command(name="reload", aliases=["refresh"])
    @commands.is_owner()
    async def p_reload(self, ctx, name):
        self.client.reload_extension(name)
        await ctx.send(f"{name} reloaded!")

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
    async def p_load(self, ctx, name):
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
    async def p_unload(self, ctx, name):
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


def setup(client):
    client.add_cog(Loaders(client))

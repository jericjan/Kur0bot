from disnake.ext import commands
import disnake


class Cog_Name_Here(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Cog_Name_Here(client))

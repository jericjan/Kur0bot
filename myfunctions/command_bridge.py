import disnake
from disnake.ext import commands


class Bridger(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def send_msg(self, thing, msg):
        if isinstance(thing, disnake.ext.commands.Context):
            await thing.send(msg)
        elif isinstance(thing, disnake.ApplicationCommandInteraction):
            await thing.response.send_message(msg)
        else:
            raise Exception(
                "Invalid thing provided! Must be Context or ApplicationCommandInteraction"
            )


def setup(client):
    client.add_cog(Bridger(client))

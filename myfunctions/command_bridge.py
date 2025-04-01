from typing import Any, Union

import disnake
from disnake.ext import commands


class Bridger(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    async def send_msg(self, thing: Union[commands.Context[Any], disnake.ApplicationCommandInteraction[Any]], msg: str):
        if isinstance(thing, commands.Context):
            await thing.send(msg)
        elif isinstance(thing, disnake.ApplicationCommandInteraction): # type: ignore
            await thing.response.send_message(msg)
        else:
            raise Exception(
                "Invalid thing provided! Must be Context or ApplicationCommandInteraction"
            )


def setup(client: commands.Bot):
    client.add_cog(Bridger(client))

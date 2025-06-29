from importlib.metadata import version
from typing import Any, cast

import g4f  # type: ignore
import nest_asyncio  # type: ignore (remind me why i added this?)
from disnake.ext import commands
from g4f.client import Client  # type: ignore
import g4f.Provider  # type: ignore
from g4f.client.types import ChatCompletion  # type: ignore

class OpenAI(commands.Cog):
    def __init__(self, client: commands.Bot):
        print(f"g4f version is {version('g4f')}")
        self.client = client
        nest_asyncio.apply()  # type: ignore

    def prompt(self, msg: str) -> str:
        client = Client()
        response = cast(
            ChatCompletion,
            client.chat.completions.create(  # pyright: ignore[reportUnknownMemberType, reportAssignmentType]
                model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                provider=g4f.Provider.DeepInfraChat,
                messages=[{"role": "user", "content": msg}],
            )
        )
        res = response.choices[0].message.content
        return res if res else "No response."

    @commands.command()
    async def gpt(self, ctx: commands.Context[Any], *, msg: str):

        def split_long_string(long_string: str, chunk_size: int =2000):
            return [
                long_string[i : i + chunk_size]
                for i in range(0, len(long_string), chunk_size)
            ]

        async with ctx.channel.typing():
            gpt_msg = self.prompt(msg)
            splitted = split_long_string(gpt_msg)
            for split in splitted:
                await ctx.send(split)

def setup(client: commands.Bot):
    client.add_cog(OpenAI(client))

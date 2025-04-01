import aiohttp
import filetype
from disnake.ext import commands


class FileTypeChecker(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    async def is_image(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                file_bytes = await response.content.read(1024)
                return filetype.is_image(file_bytes)


def setup(client: commands.Bot):
    client.add_cog(FileTypeChecker(client))

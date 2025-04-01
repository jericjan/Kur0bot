import io
import os
from typing import Any, Optional, Union
from urllib.parse import quote

import aiohttp
import disnake
import humanize
from disnake.ext import commands

def delete_file(filename: str):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(f"Could not delete {filename}. File not Found.")


async def send_file(ctx: commands.Context[Any], message: disnake.Message, filename: str, custom_name: Optional[str] = None):
    if custom_name:
        clean_name = custom_name
    else:
        clean_name = filename.replace(",", "")

    def bytes_to_mebibytes(data: Union[list[int], int]):
        if isinstance(data, list):
            return [bytes * 1024 * 1024 for bytes in data]
        else:
            return data * 1024 * 1024

    boost_size_limits: list[int] = bytes_to_mebibytes([25, 25, 50, 100])  # type: ignore
    if ctx.guild is not None:
        boosts = ctx.guild.premium_tier
        try:
            limit = boost_size_limits[boosts]
        except:
            print("Couldn't find boosts")
            limit: int = bytes_to_mebibytes(25)  # type: ignore
    else:
        limit: int = bytes_to_mebibytes(25)  # type: ignore
    if isinstance(filename, io.BytesIO):
        filesize = filename.getbuffer().nbytes
    else:
        filesize = os.path.getsize(filename)
    if filesize <= limit:
        await message.edit(content="Sending...")
        try:
            await ctx.send(file=disnake.File(filename, filename=clean_name))
        except Exception as e:
            await ctx.send(f"Failed to send: {e}")
    else:
        os.rename(filename, f"temp/{filename}")
        url_enc_filename = quote(filename)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://checkip.amazonaws.com") as resp:
                ip = await resp.text()
                ip = ip.strip()
        msg = (
            "File too large, broski <:towashrug:853606191711649812>\n"
            f"The file: {humanize.naturalsize(filesize, binary=True)}\n"
            f"Server upload limit: {humanize.naturalsize(limit, binary=True)}\n"
            f"You can access the file here but it will only be up for 12 hours:\n"
            f"http://{ip}:{os.getenv('PORT')}/temp/{url_enc_filename}"
        )
        await ctx.send(msg)
    await message.delete()

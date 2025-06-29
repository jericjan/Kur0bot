import io
import re
from typing import Any, Optional

import aiohttp
import requests
from aiolimiter import AsyncLimiter
from disnake.ext import commands
from PIL import Image

from myfunctions import file_handler, msg_link_grabber, subprocess_runner
from myfunctions.async_wrapper import async_wrap

limiter = AsyncLimiter(1, 1)


class Resize(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @async_wrap
    def resize_core(self, link: str, width: int, height: int):
        response = requests.get(link)  # threaded
        byteio = io.BytesIO(response.content)
        im = Image.open(byteio)
        newsize = (int(width), int(height))
        im = im.resize(newsize)
        byteio.close()
        byteio2 = io.BytesIO()
        byteio2.seek(0)
        im.save(byteio2, format="PNG")
        byteio2.seek(0)
        return byteio2

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def resize(self, ctx: commands.Context[Any], width: int, height: int, link: Optional[str]=None, algorithm: Optional[str]=None):
        link = await msg_link_grabber.grab_link(ctx, link)
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as r:
                content_type = r.headers["Content-Type"]
        file_type, file_ext = content_type.split("/")
        if file_type == "video" or file_ext == "gif":
            message = await ctx.send("Resizing video...")
            filename = link.split("/")[-1].split("?")[0]
            regex = re.findall(r".+(?=\.)", filename)
            if regex:
                filename = regex[0]
            filename = f"{filename}.{file_ext}"
            filepath = f"videos/resize/{filename}"
            coms = [
                "ffmpeg",
                "-i",
                link,
                "-vf",
                f"scale={width}:{height},setsar=1",
            ]
            if algorithm:
                algo_list = [
                    "fast_bilinear",
                    "bilinear",
                    "bicubic",
                    "experimental",
                    "neighbor",
                    "area",
                    "bicublin",
                    "gauss",
                    "sinc",
                    "lanczos",
                    "spline",
                    "accurate_rnd",
                    "full_chroma_int",
                    "full_chroma_inp",
                    "bitexact",
                ]
                if algorithm in algo_list:
                    coms.extend(["-sws_flags", algorithm])
                else:
                    await ctx.send(
                        "You sent an invalid algorithm!\nCheck https://ffmpeg.org/ffmpeg-scaler.html for the list"
                    )
                    return
            coms.append(filepath)
            await subprocess_runner.run_subprocess(coms)
            await file_handler.send_file(ctx, message, filepath, filename)
            file_handler.delete_file(filepath)
        elif file_type == "image":
            message = await ctx.send("Resizing...")
            bruh = await self.resize_core(link, width, height)
            bruh.seek(0)
            filename = link.split("/")[-1].split("?")[0]
            await file_handler.send_file(ctx, message, bruh, filename)
            bruh.close()


def setup(client: commands.Bot):
    client.add_cog(Resize(client))

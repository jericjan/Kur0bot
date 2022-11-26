from disnake.ext import commands


import asyncio
import aiohttp
from PIL import Image
import io
import requests
import functools
from aiolimiter import AsyncLimiter
import re
from myfunctions import msg_link_grabber, file_handler, subprocess_runner
import os

limiter = AsyncLimiter(1, 1)


class Resize(commands.Cog):
    def __init__(self, client):
        self.client = client

    def run_in_executor(f):
        @functools.wraps(f)
        async def inner(*args, **kwargs):
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: f(*args, **kwargs))

        return inner

    def bar(self, link, width, height):
        response = requests.get(link)
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

    @run_in_executor
    def foo(self, link, width, height):  # Your wrapper for async use
        out = self.bar(link, width, height)
        return out

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def resize(self, ctx, width, height, link=None, algorithm=None):
        link = await msg_link_grabber.grab_link(ctx, link)
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as r:
                content_type = r.headers["Content-Type"]
        file_type, file_ext = content_type.split("/")
        if file_type == "video" or file_ext == "gif":
            message = await ctx.send("Resizing video...")
            filename = link.split("/")[-1]
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
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            await file_handler.send_file(ctx, message, filepath, filename)
            file_handler.delete_file(filepath)
        elif file_type == "image":
            message = await ctx.send("Resizing...")
            bruh = await self.foo(link, width, height)
            bruh.seek(0)
            filename = link.split("/")[-1]
            await file_handler.send_file(ctx, message, bruh, filename)
            bruh.close()

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def rs(self, ctx, link=None):
        async def res_vid(msg, in_video, out_video, name=None):
            coms = [
                "ffmpeg",
                "-i",
                in_video,
                "-vf",
                "scale=1600:720,setsar=1",
                "-vcodec",
                "h264",
                out_video,
            ]
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            if name is None:
                await file_handler.send_file(ctx, msg, out_video)
            else:
                await file_handler.send_file(ctx, msg, out_video, name)
            file_handler.delete_file(out_video)
            if os.path.exists(in_video):
                file_handler.delete_file(in_video)

        link = await msg_link_grabber.grab_link(ctx, link)
        if "youtube.com" in link or "youtu.be" in link:
            message = await ctx.send("Downloading and resizing YT video...")
            coms = ["yt-dlp", "-f", "b", "--no-warnings", "-P", "videos/resize/", link]
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            coms = ["yt-dlp", "-f", "b", "--get-filename", "--no-warnings", link]
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            filename = stdout.decode("utf-8").rstrip("\n")
            filename = filename.split(".")
            file_ext = filename.pop(-1)
            filename = ".".join(filename)
            filename1 = f"{filename}.{file_ext}"
            filename2 = f"{filename}_2.{file_ext}"
            filepath = f"videos/resize/{filename1}"
            filepath2 = f"videos/resize/{filename2}"
            stdout = stdout.decode("utf-8")
            await res_vid(message, filepath, filepath2, filename1)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as r:
                    content_type = r.headers["Content-Type"]
            file_type, file_ext = content_type.split("/")
            if file_type == "image":
                message = await ctx.send("Resizing...")
                bruh = await self.foo(link, 1600, 720)
                bruh.seek(0)
                filename = link.split("/")[-1]
                await file_handler.send_file(ctx, message, bruh, filename)
                bruh.close()
            elif file_type == "video":
                message = await ctx.send("Resizing video...")
                filename = link.split("/")[-1]
                regex = re.findall(r".+(?=\.)", filename)
                if regex:
                    filename = regex[0]
                filename = f"{filename}.{file_ext}"
                filepath = f"videos/resize/{filename}"
                await res_vid(message, link, filepath, filename)


def setup(client):
    client.add_cog(Resize(client))

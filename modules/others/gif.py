from disnake.ext import commands
import re
import asyncio
import subprocess
from tqdm import tqdm
from aiolimiter import AsyncLimiter
from datetime import datetime, timedelta
import io
import os
import uuid
import glob
import shutil
import time
import shlex
from myfunctions import msg_link_grabber, subprocess_runner, file_handler
from typing import Any

limiter = AsyncLimiter(1, 1)


class Gif(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.pbar_list = []

    async def updatebar(self, msg):
        try:

            async with limiter:
                await asyncio.wait_for(msg.edit(content=self.pbar_list[-1]), timeout=1)
        except Exception as e:
            if str(e).startswith("404 Not Found"):
                pass
            else:
                pass
            pass

    @commands.command(aliases=["vid2gif", "gifify"])
    @commands.bot_has_permissions(manage_messages=True)
    async def gif(self, ctx: commands.Context[Any], link=None):
        link = await msg_link_grabber.grab_link(ctx, link)
        print(link)

        filename = link.split("/")[-1]
        new_filename = "".join(filename.split(".")[:-1]) + ".gif"
        if re.search(r".+\.mp4|.+\.mkv|.+\.mov|.+\.webm", filename) is not None:
            coms = [
                "ffmpeg",
                "-i",
                link,
                "-y",
                new_filename,
            ]
            message = await ctx.send("Converting to GIF...")
            process = await asyncio.create_subprocess_exec(  # reads stdout live
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            full_line = ""
            pbar = tqdm(total=100)
            while process.returncode is None:

                line = await process.stdout.read(500)
                if not line:
                    break
                linedec = line.decode("utf-8")
                full_line += linedec
                print(linedec)
                if (
                    re.search(r"(?<=Duration: )\d{2}:\d{2}:\d{2}.\d{2}", full_line)
                    is not None
                ):
                    duration_str = re.findall(
                        r"(?<=Duration: )\d{2}:\d{2}:\d{2}.\d{2}", full_line
                    )[-1]
                    strpcurr = datetime.strptime(duration_str, "%H:%M:%S.%f")
                    duration = timedelta(
                        hours=strpcurr.hour,
                        minutes=strpcurr.minute,
                        seconds=strpcurr.second,
                        microseconds=strpcurr.microsecond,
                    )
                if (
                    re.search(r"(?<=time=)\d{2}:\d{2}:\d{2}.\d{2}", full_line)
                    is not None
                ):
                    if (
                        re.findall(r"(?<=time=)\d{2}:\d{2}:\d{2}.\d{2}", full_line)[-1]
                        != "00:00:00.00"
                    ):
                        currtime_str = re.findall(
                            r"(?<=time=)\d{2}:\d{2}:\d{2}.\d{2}", full_line
                        )[-1]
                        strpcurr = datetime.strptime(currtime_str, "%H:%M:%S.%f")
                        currtime = timedelta(
                            hours=strpcurr.hour,
                            minutes=strpcurr.minute,
                            seconds=strpcurr.second,
                            microseconds=strpcurr.microsecond,
                        )
                        try:
                            percentage = (
                                currtime.total_seconds() / duration.total_seconds()
                            ) * 100

                            output = io.StringIO()
                            pbar = tqdm(total=100, file=output, ascii=False)
                            pbar.update(float(f"{percentage:.3f}"))
                            pbar.close()
                            final = output.getvalue()
                            output.close()
                            final1 = final.splitlines()[-1]
                            aaa = re.findall(
                                r"(?<=\d\%)\|.+\| (?=\d+|\d+.\d+/\d+|\d+.\d+)", final1
                            )[0]
                            self.pbar_list.append(
                                f"Converting to GIF...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"
                            )
                            asyncio.ensure_future(self.updatebar(message))
                        except:
                            if not filename.endswith("gif"):
                                await message.edit(
                                    content="Uh, I couldn't find the duration of vod. idk man."
                                )
        else:
            await ctx.send(
                "I don't support this filetype yet ig. Ping kur0 or smth. <:towashrug:853606191711649812> "
            )
        await file_handler.send_file(ctx, message, new_filename)
        file_handler.delete_file(new_filename)

    @commands.command(aliases=["vid2gif2", "gifify2"])
    @commands.bot_has_permissions(manage_messages=True)
    async def gif2(self, ctx: commands.Context[Any], link=None, quality=None):
        uuid_id = uuid.uuid4()
        if link:
            if (
                link.isdigit()
            ):  # if link is digits 1-100. usually for when replying to message or sending vid directly.
                if int(link) in range(1, 101):
                    quality = link
                    if ctx.message.attachments:  # message has images
                        print("is attachment")
                        link = ctx.message.attachments[0].url
                    elif ctx.message.reference is not None:  # message is replying
                        print("is reply")
                        id = ctx.message.reference.message_id
                        msg = await ctx.channel.fetch_message(id)
                        if msg.attachments:  # if replied has image
                            link = msg.attachments[0].url
                        elif msg.embeds:  # if replied has link
                            link = msg.embeds[0].url
                else:
                    await ctx.send(
                        "If you were trying to specify a quality. It's not valid."
                    )
            elif quality == None:
                quality = 70
        else:
            quality = 70

        link = await msg_link_grabber.grab_link(ctx, link)
        print(link)

        filename = link.split("/")[-1]
        new_filename = "".join(filename.split(".")[:-1]) + ".gif"
        if new_filename.startswith("-"):
            new_filename = new_filename[1:]
        print(f"filename is: {filename}, quality is: {quality}")
        if re.search(r".+\.mp4|.+\.mkv|.+\.mov|.+\.webm", filename) is not None:
            frames_folder = f"frames_{uuid_id}"
            os.mkdir(f"{frames_folder}/")
            frames_path = f"{frames_folder}/frame%04d.png"

            coms = ["ffmpeg", "-i", link, frames_path]
            message = await ctx.send("Extracting frames... This might take a bit.")
            print("FFMPEGGGG")
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)

            gif_ski_frames_path = f"{frames_folder}/frame*.png"
            gif_ski_frames_path = glob.glob(gif_ski_frames_path)
            coms = [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                "-show_entries",
                "stream=r_frame_rate",
                link,
            ]
            await message.edit(content="Getting framerate...")
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            result_string = stdout.decode("utf-8").split()[0].split("/")
            fps = float(result_string[0]) / float(result_string[1])
            await message.edit(content="Making gif...")
            edit_start = time.time()
            coms = [
                "gifski_/gifski",
                "--fps",
                str(fps),
                "--quality",
                str(quality),
                "--width",
                "640",
                "--output",
                new_filename,
            ]

            coms = coms + gif_ski_frames_path
            print(shlex.join(coms))
            process = await asyncio.create_subprocess_exec(  # reads stdout live
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            full_line = ""
            while process.returncode is None:
                line = await process.stdout.read(500)

                if not line:
                    break
                linedec = line.decode("utf-8")
                print(linedec)
                full_line += linedec
                split_full_line = full_line.split("\r")
                time_since_edit = time.time() - edit_start
                if time_since_edit > 1:
                    await message.edit(content=f"Making gif...\n{split_full_line[-1]}")
                    edit_start = time.time()
                else:
                    pass

            print("GIFSKI")
            await file_handler.send_file(ctx, message, new_filename)
            file_handler.delete_file(new_filename)
            shutil.rmtree(f"{frames_folder}/")
        elif re.search(r".+\.jpg|.+\.png|.+\.webp", filename) is not None:
            pre_message = await ctx.send(
                "You... want to turn an image into a gif? Uh ok then."
            )
            frames_folder = f"frames_{uuid_id}"
            os.mkdir(f"{frames_folder}/")
            frames_path1 = f"{frames_folder}/frame1.png"
            frames_path2 = f"{frames_folder}/frame2.png"

            coms = ["ffmpeg", "-i", link, frames_path1]
            coms2 = ["ffmpeg", "-i", link, frames_path2]
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms2)
            print("FFMPEGGGG")

            gif_ski_frames_path = f"{frames_folder}/frame*.png"
            gif_ski_frames_path = glob.glob(gif_ski_frames_path)
            coms = [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                "-show_entries",
                "stream=r_frame_rate",
                link,
            ]
            message = await ctx.send("Making gif...")
            coms = [
                "gifski_/gifski",
                "--output",
                new_filename,
            ]

            coms = coms + gif_ski_frames_path
            print("GIFSKI")
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            await file_handler.send_file(ctx, message, new_filename)
            file_handler.delete_file(new_filename)
            shutil.rmtree(f"{frames_folder}/")
            await pre_message.delete()
        else:
            await ctx.send(
                "I don't support this filetype yet ig. Ping kur0 or smth. <:towashrug:853606191711649812> "
            )


def setup(client: commands.Bot):
    client.add_cog(Gif(client))

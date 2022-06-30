from disnake.ext import commands
import disnake
import asyncio
import os
import subprocess
import re
from tqdm import tqdm
import io
from aiolimiter import AsyncLimiter
from datetime import datetime, timedelta
import myfunctions.msg_link_grabber as msg_link_grabber
from shlex import join as shjoin

limiter = AsyncLimiter(1, 1)


class lowQual(commands.Cog):
    def __init__(self, client):
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

    @commands.command(aliases=["shitify", "pixelize"])
    async def lowqual(self, ctx, link=None):
        link = await msg_link_grabber.grab_link(ctx, link)
        print(link)

        is_tenor = False
        if "tenor.com" in link:
            is_tenor = True
            if ctx.message.reference is not None:  # message is replying
                vid_url = ctx.message.reference.resolved.embeds[0].video.url
                print(vid_url)
            elif ctx.message.embeds:
                vid_url = ctx.message.embeds[0].video.url
            else:
                await ctx.send(
                    "Hmm... Can't find the gif. An embed fail perhaps? <a:trollplant:934777423881445436>"
                )
                return

            filename = link.split("/")[-1]
            filename = f"{''.join(filename)}.gif"
            link = vid_url
        else:
            filename = link.split("/")[-1]
        if re.search(r".+\.mp4|.+\.mkv|.+\.mov|.+\.webm|.+\.gif", filename) is not None:
            # remuxes so it works with troll long videos, magic.
            muxname = re.sub(r"(.+(?=\..+))", r"\g<1>_mux", filename)
            if is_tenor:
                coms = [
                    "ffmpeg-git/ffmpeg",
                    "-i",
                    link,
                    muxname,
                ]
            else:
                coms = [
                    "ffmpeg-git/ffmpeg",
                    "-i",
                    link,
                    "-c:v",
                    "copy",
                    "-c:a",
                    "copy",
                    muxname,
                ]
            print(shjoin(coms))
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            print(f"stdout:\n\033[;32m{stdout.decode('utf-8')}\033[0m")
            print(f"stderr:\n\033[;31m{stderr.decode('utf-8')}\033[0m")
            tempname = re.sub(r"(.+(?=\..+))", r"\g<1>01", filename)
            coms = [
                "ffmpeg",
                "-i",
                muxname,
                "-vf",
                "scale=-2:20:flags=neighbor",
                "-b:v",
                "15000",
                "-b:a",
                "10000",
                "-y",
                tempname,
            ]
            print(shjoin(coms))
            message = await ctx.send("Downscaling...")
            process = await asyncio.create_subprocess_exec(
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
                if (
                    re.search(r"(?<=Duration: )\d{2,}:\d{2}:\d{2}.\d{2}", full_line)
                    is not None
                ):
                    duration_str = re.findall(
                        r"(?<=Duration: )\d{2,}:\d{2}:\d{2}.\d{2}", full_line
                    )[-1]
                    strpcurr = datetime.strptime(duration_str, "%H:%M:%S.%f")
                    duration = timedelta(
                        hours=strpcurr.hour,
                        minutes=strpcurr.minute,
                        seconds=strpcurr.second,
                        microseconds=strpcurr.microsecond,
                    )
                if (
                    re.search(r"(?<=time=)\d{2,}:\d{2}:\d{2}.\d{2}", full_line)
                    is not None
                ):
                    if (
                        re.findall(r"(?<=time=)\d{2,}:\d{2}:\d{2}.\d{2}", full_line)[-1]
                        != "00:00:00.00"
                    ):
                        currtime_str = re.findall(
                            r"(?<=time=)\d{2,}:\d{2}:\d{2}.\d{2}", full_line
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
                                f"Downscaling...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"
                            )
                            asyncio.ensure_future(self.updatebar(message))
                        except Exception as e:
                            if not filename.endswith("gif"):
                                await message.edit(
                                    content=f"Uh, I couldn't find the duration of vod. idk man.\nException: {e}"
                                )
            all_lines = await process.stdout.read()
            print(f"output:\n\033[;32m{all_lines.decode('utf-8')}\033[0m")
            os.remove(muxname)
            coms = [
                "ffmpeg",
                "-i",
                tempname,
                "-vf",
                "scale=-2:144:flags=neighbor",
                "-c:a",
                "copy",
                "-y",
                filename,
            ]
            print(shjoin(coms))
            await message.edit(content="Upscaling...")
            process = await asyncio.create_subprocess_exec(
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
                if (
                    re.search(r"(?<=Duration: )\d{2,}:\d{2}:\d{2}.\d{2}", full_line)
                    is not None
                ):
                    duration_str = re.findall(
                        r"(?<=Duration: )\d{2,}:\d{2}:\d{2}.\d{2}", full_line
                    )[-1]
                    strpcurr = datetime.strptime(duration_str, "%H:%M:%S.%f")
                    duration = timedelta(
                        hours=strpcurr.hour,
                        minutes=strpcurr.minute,
                        seconds=strpcurr.second,
                        microseconds=strpcurr.microsecond,
                    )
                if (
                    re.search(r"(?<=time=)\d{2,}:\d{2}:\d{2}.\d{2}", full_line)
                    is not None
                ):
                    if (
                        re.findall(r"(?<=time=)\d{2,}:\d{2}:\d{2}.\d{2}", full_line)[-1]
                        != "00:00:00.00"
                    ):
                        currtime_str = re.findall(
                            r"(?<=time=)\d{2,}:\d{2}:\d{2}.\d{2}", full_line
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
                                f"Upscaling...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"
                            )
                            asyncio.ensure_future(self.updatebar(message))
                        except:
                            if not filename.endswith("gif"):
                                await message.edit(
                                    content="Uh, I couldn't find the duration of vod. idk man."
                                )
            all_lines = await process.stdout.read()
            print(f"output:\n\033[;32m{all_lines.decode('utf-8')}\033[0m")
            os.remove(tempname)

        elif re.search(r".+\.jpg|.+\.jpeg|.+\.png|.+\.webp", filename) is not None:
            filename = filename.split("?")[0]
            tempname = re.sub(r"(.+(?=\..+))", r"\g<1>01", filename)
            coms = [
                "ffmpeg",
                "-i",
                link,
                "-vf",
                "scale=-2:20",
                "-b:v",
                "15000",
                tempname,
            ]
            message = await ctx.send("Downscaling...")
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await process.communicate()

            coms = [
                "ffmpeg",
                "-i",
                tempname,
                "-vf",
                "scale=-2:1080:flags=neighbor",
                filename,
            ]
            await message.edit(content="Upscaling...")
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await process.communicate()
            os.remove(tempname)
        else:
            await ctx.send(
                "I don't support this filetype yet ig. Ping kur0 or smth. <:towashrug:853606191711649812> "
            )
            return
        await ctx.send(file=disnake.File(filename))
        await message.delete()
        os.remove(filename)


def setup(client):
    client.add_cog(lowQual(client))

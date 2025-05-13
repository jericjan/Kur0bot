import asyncio
import io
import re
import subprocess
from datetime import datetime, timedelta
from shlex import join as shjoin
from typing import Any, Optional

from aiolimiter import AsyncLimiter
import disnake
from disnake.ext import commands
from tqdm import tqdm

from myfunctions import file_handler, msg_link_grabber, subprocess_runner

limiter = AsyncLimiter(1, 1)


class lowQual(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.pbar_list: list[str] = []

    async def updatebar(self, msg: disnake.Message):
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
    @commands.bot_has_permissions(manage_messages=True)
    async def lowqual(self, ctx: commands.Context[Any], link: Optional[str] = None):
        link = await msg_link_grabber.grab_link(ctx, link)
        print(link)

        is_tenor = False
        if "tenor.com" in link:
            is_tenor = True
            fail_msg = "Hmm... Can't find the gif. An embed fail perhaps? <a:trollplant:934777423881445436>"
            if ctx.message.reference is not None:  # message is replying
                if isinstance(ctx.message.reference.resolved, disnake.Message):
                    vid_url = ctx.message.reference.resolved.embeds[0].video.url
                    print(vid_url)
                else:
                    await ctx.send("You replied to smth but I couldn't find it. Damn.")
                    return
            elif ctx.message.embeds:
                vid_url = ctx.message.embeds[0].video.url
            else:
                await ctx.send(fail_msg)
                return

            if vid_url is None:
                await ctx.send(fail_msg)
                return    

            filename = link.split("/")[-1]
            filename = f"{''.join(filename)}.gif"
            link = vid_url
        else:
            filename = link.split("/")[-1]
        if (
            re.search(
                r".+\.mp4|.+\.mkv|.+\.mov|.+\.webm|.+\.gif|.+\.mp3|.+\.wav", filename
            )
            is not None
        ):
            filename = filename.split("?")[0]
            # remuxes so it works with troll long videos, magic.
            muxname = re.sub(r"(.+(?=\..+))", r"\g<1>_mux", filename)
            if is_tenor:
                coms: list[str] = [
                    "ffmpeg",
                    "-i",
                    link,
                    muxname,
                ]
            else:
                coms = [
                    "ffmpeg",
                    "-i",
                    link,
                    "-c:v",
                    "copy",
                    "-c:a",
                    "copy",
                    muxname,
                ]
            _out, _stdout, _stderr = await subprocess_runner.run_subprocess(coms)
            tempname = re.sub(r"(.+(?=\..+))", r"\g<1>01", filename)
            coms = [
                "ffmpeg",
                "-i",
                muxname,
                "-vf",
                # "scale=-2:20:flags=neighbor",
                "scale=-2:20",
                "-b:v",
                "15000",
                "-b:a",
                "10000",
                "-y",
                tempname,
            ]
            print(shjoin(coms))
            message = await ctx.send("Downscaling...")
            process = await asyncio.create_subprocess_exec(  # reads stdout live
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            full_line = ""
            pbar = tqdm(total=100)
            duration = None
            while process.returncode is None:
                if process.stdout is None:
                    break

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
                            if duration is None:
                                continue
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
                            if not filename.endswith("gif"):  # TODO: not sure why i had this check here
                                await message.edit(
                                    content=f"Uh, I couldn't find the duration of vod. idk man.\nException: {e}"
                                )
            # all_lines = await process.stdout.read()
            # print(f"output:\n\033[;32m{all_lines.decode('utf-8')}\033[0m")
            file_handler.delete_file(muxname)
            coms = [
                "ffmpeg",
                "-i",
                tempname,
                "-vf",
                # "scale=-2:144:flags=neighbor",
                "scale=-2:144",
                "-c:a",
                "copy",
                "-y",
                filename,
            ]
            print(shjoin(coms))
            await message.edit(content="Upscaling...")
            process = await asyncio.create_subprocess_exec(  # reads stdout live
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            full_line = ""
            pbar = tqdm(total=100)
            duration = None
            while process.returncode is None:
                if process.stdout is None:
                    break
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
                            if duration is None:
                                continue
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
            # all_lines = await process.stdout.read()
            # print(f"output:\n\033[;32m{all_lines.decode('utf-8')}\033[0m")
            file_handler.delete_file(tempname)

        elif re.search(r".+\.jpg|.+\.jpeg|.+\.png|.+\.webp", filename) is not None:
            filename = filename.split("?")[0]
            tempname = re.sub(r"(.+(?=\..+))", r"\g<1>01", filename)
            message = await ctx.send("Downscaling...")
            _out, _stdout, _stderr = await subprocess_runner.run_subprocess([
                "ffmpeg",
                "-i",
                link,
                "-vf",
                "scale=-2:20",
                "-b:v",
                "15000",
                tempname,
            ])

            await message.edit(content="Upscaling...")
            _out, _stdout, _stderr = await subprocess_runner.run_subprocess([
                "ffmpeg",
                "-i",
                tempname,
                "-vf",
                # "scale=-2:1080:flags=neighbor",
                "scale=-2:1080",
                filename,
            ])
            file_handler.delete_file(tempname)
        else:
            await ctx.send(
                "I don't support this filetype yet ig. Ping kur0 or smth. <:towashrug:853606191711649812> "
            )
            return
        await file_handler.send_file(ctx, message, filename)
        file_handler.delete_file(filename)


def setup(client: commands.Bot):
    client.add_cog(lowQual(client))

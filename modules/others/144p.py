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
import json

limiter = AsyncLimiter(1, 1)


class lowQual(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pbar_list = []

    async def updatebar(self, msg):
        # print("Updating bar...")
        try:

            async with limiter:
                await asyncio.wait_for(msg.edit(content=self.pbar_list[-1]), timeout=1)
                # print("\033[92m SUCCESS! \033[0m")
        except Exception as e:
            if str(e).startswith("404 Not Found"):
                pass
            else:
                # print(f"\033[91m timeout!\n{e} \033[0m")
                pass
            pass

    @commands.command(aliases=["shitify", "pixelize"])
    async def lowqual(self, ctx, link=None):

        if link == None:
            print(ctx.message.attachments)  # a list
            print(ctx.message.reference)
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

        if link == None:  # check again
            await ctx.send("Bruh, there's nothing there. what am i supposed to do?")
            return

        # print(f"link is {link}")
        if "tenor.com" in link:

          if ctx.message.embeds:  
            vid_url = ctx.message.embeds[0].video.url
          else:
            await ctx.send('Hmm... Can\'t find the gif. An embed fail perhaps? <a:trollplant:934777423881445436>')  
            return

          filename = link.split("/")[-1]
          filename  = f"{''.join(filename)}.gif"
         # await ctx.send(f"filename is {filename}")
          link = vid_url
        else:    
          filename = link.split("/")[-1]
        if re.search(r".+\.mp4|.+\.mkv|.+\.mov|.+\.webm|.+\.gif", filename) is not None:
            tempname = re.sub(r"(.+(?=\..+))", r"\g<1>01", filename)
            coms = [
                "ffmpeg",
                "-i",
                link,
                "-vf",
                "scale=-2:20:flags=neighbor",
                "-b:v",
                "15000",
                "-b:a",
                "10000",
                "-y",
                tempname,
            ]
            message = await ctx.send("Downscaling...")
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            # stdout, stderr = await process.communicate()
            full_line = ""
            pbar = tqdm(total=100)
            while process.returncode is None:

                line = await process.stdout.read(500)
                if not line:
                    break
                # print(line.decode('utf-8'))
                linedec = line.decode("utf-8")
                full_line += linedec
                # print(linedec)
                if (
                    re.search(r"(?<=Duration: )\d{2}:\d{2}:\d{2}.\d{2}", full_line)
                    is not None
                ):
                    duration_str = re.findall(
                        r"(?<=Duration: )\d{2}:\d{2}:\d{2}.\d{2}", full_line
                    )[-1]
                    # print(f"Duration is {duration_str}")
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
                    # print(linedec)
                    if (
                        re.findall(r"(?<=time=)\d{2}:\d{2}:\d{2}.\d{2}", full_line)[-1]
                        != "00:00:00.00"
                    ):
                        currtime_str = re.findall(
                            r"(?<=time=)\d{2}:\d{2}:\d{2}.\d{2}", full_line
                        )[-1]
                        # print(f"Current time is {currtime_str}")
                        strpcurr = datetime.strptime(currtime_str, "%H:%M:%S.%f")
                        currtime = timedelta(
                            hours=strpcurr.hour,
                            minutes=strpcurr.minute,
                            seconds=strpcurr.second,
                            microseconds=strpcurr.microsecond,
                        )
                        # print(linedec)
                        try:
                            percentage = (
                                currtime.total_seconds() / duration.total_seconds()
                            ) * 100
                            # print(f"{percentage}% complete...")

                            output = io.StringIO()
                            pbar = tqdm(total=100, file=output, ascii=False)
                            pbar.update(float(f"{percentage:.3f}"))
                            pbar.close()
                            final = output.getvalue()
                            output.close()
                            final1 = final.splitlines()[-1]
                            # print(final1)
                            aaa = re.findall(
                                r"(?<=\d\%)\|.+\| (?=\d+|\d+.\d+/\d+|\d+.\d+)", final1
                            )[0]
                            self.pbar_list.append(
                                f"Downscaling...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"
                            )
                            asyncio.ensure_future(self.updatebar(message))
                        except:
                          if not filename.endswith('gif'):
                            await message.edit(
                                content=f"Uh, I couldn't find the duration of vod. idk man."
                            )

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
                # print(line.decode('utf-8'))
                linedec = line.decode("utf-8")
                full_line += linedec
                # print(linedec)
                if (
                    re.search(r"(?<=Duration: )\d{2}:\d{2}:\d{2}.\d{2}", full_line)
                    is not None
                ):
                    duration_str = re.findall(
                        r"(?<=Duration: )\d{2}:\d{2}:\d{2}.\d{2}", full_line
                    )[-1]
                    # print(f"Duration is {duration_str}")
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
                    # print(linedec)
                    if (
                        re.findall(r"(?<=time=)\d{2}:\d{2}:\d{2}.\d{2}", full_line)[-1]
                        != "00:00:00.00"
                    ):
                        currtime_str = re.findall(
                            r"(?<=time=)\d{2}:\d{2}:\d{2}.\d{2}", full_line
                        )[-1]
                        # print(f"Current time is {currtime_str}")
                        strpcurr = datetime.strptime(currtime_str, "%H:%M:%S.%f")
                        currtime = timedelta(
                            hours=strpcurr.hour,
                            minutes=strpcurr.minute,
                            seconds=strpcurr.second,
                            microseconds=strpcurr.microsecond,
                        )
                        # print(linedec)
                        try:
                            percentage = (
                                currtime.total_seconds() / duration.total_seconds()
                            ) * 100
                            # print(f"{percentage}% complete...")

                            output = io.StringIO()
                            pbar = tqdm(total=100, file=output, ascii=False)
                            pbar.update(float(f"{percentage:.3f}"))
                            pbar.close()
                            final = output.getvalue()
                            output.close()
                            final1 = final.splitlines()[-1]
                            # print(final1)
                            aaa = re.findall(
                                r"(?<=\d\%)\|.+\| (?=\d+|\d+.\d+/\d+|\d+.\d+)", final1
                            )[0]
                            self.pbar_list.append(
                                f"Upscaling...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"
                            )
                            asyncio.ensure_future(self.updatebar(message))
                        except:
                          if not filename.endswith('gif'):
                            await message.edit(
                                content=f"Uh, I couldn't find the duration of vod. idk man."
                            )
            os.remove(tempname)
            
        elif re.search(r".+\.jpg|.+\.jpeg|.+\.png", filename) is not None:
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
            # await ctx.send(f"{round(percentage, 2)}% complete...\n`{aaa}`")
        else:
            await ctx.send(
                "I don't support this filetype yet ig. Ping kur0 or smth. <:towashrug:853606191711649812> "
            )
        await ctx.send(file=disnake.File(filename))
        await message.delete()
        os.remove(filename)


def setup(client):
    client.add_cog(lowQual(client))

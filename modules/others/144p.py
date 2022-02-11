from disnake.ext import commands
import disnake
import asyncio
import os
import subprocess
import re
from tqdm import tqdm
import io

from datetime import datetime, timedelta


class lowQual(commands.Cog):
    def __init__(self, client):
        self.client = client

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

        print(f"link is {link}")
        filename = link.split("/")[-1]
        coms = ["ffmpeg", "-i", link, "-vf", "scale=-2:20", "-b:v", "15000", filename]
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
                print(f"Duration is {duration_str}")
                strpcurr = datetime.strptime(duration_str, "%H:%M:%S.%f")
                duration = timedelta(
                    hours=strpcurr.hour,
                    minutes=strpcurr.minute,
                    seconds=strpcurr.second,
                    microseconds=strpcurr.microsecond,
                )
            if re.search(r"(?<=time=)\d{2}:\d{2}:\d{2}.\d{2}", full_line) is not None:
                # print(linedec)
                if (
                    re.findall(r"(?<=time=)\d{2}:\d{2}:\d{2}.\d{2}", full_line)[-1]
                    != "00:00:00.00"
                ):
                    currtime_str = re.findall(
                        r"(?<=time=)\d{2}:\d{2}:\d{2}.\d{2}", full_line
                    )[-1]
                    print(f"Current time is {currtime_str}")
                    strpcurr = datetime.strptime(currtime_str, "%H:%M:%S.%f")
                    currtime = timedelta(
                        hours=strpcurr.hour,
                        minutes=strpcurr.minute,
                        seconds=strpcurr.second,
                        microseconds=strpcurr.microsecond,
                    )
                    # print(linedec)
                    percentage = (
                        currtime.total_seconds() / duration.total_seconds()
                    ) * 100
                    print(f"{percentage}% complete...")
                    pbar

                    output = io.StringIO()
                    pbar = tqdm(total=100, file=output, ascii=False)
                    pbar.update(float(f"{percentage:.3f}"))
                    pbar.close()
                    final = output.getvalue()
                    output.close()
                    final1 = final.splitlines()[-1]
                    print(final1)
                    aaa = re.findall(
                        r"(?<=\d\%)\|.+\| (?=\d+|\d+.\d+/\d+|\d+.\d+)", final1
                    )[0]
                    await message.edit(
                        content=f"{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"
                    )
                    # await ctx.send(f"{round(percentage, 2)}% complete...\n`{aaa}`")

        await ctx.send(file=disnake.File(filename))
        await message.delete()
        os.remove(filename)


def setup(client):
    client.add_cog(lowQual(client))

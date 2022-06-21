from disnake.ext import commands
import re
import asyncio
import subprocess
from tqdm import tqdm
from aiolimiter import AsyncLimiter
from datetime import datetime, timedelta
import io
import os
import disnake
import uuid
import glob
import shutil
import time
import shlex 

limiter = AsyncLimiter(1, 1)


class Gif(commands.Cog):
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

    @commands.command(aliases=["vid2gif", "gifify"])
    async def gif(self, ctx, link=None):
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
                print(linedec)
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
        await ctx.send(file=disnake.File(new_filename))
        await message.delete()
        os.remove(new_filename)

    @commands.command(aliases=["vid2gif2", "gifify2"])
    async def gif2(self, ctx, link=None, quality=None):
        uuid_id = uuid.uuid4()
        if link:
            if link.isdigit():  # if link is digits 1-100. usually for when replying to message or sending vid directly.
                if int(link) in range(1,101):
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
                    await ctx.send("If you were trying to specify a quality. It's not valid.")
            elif quality == None:
                quality = 70
        else:
            quality = 70
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

        filename = link.split("/")[-1]
        new_filename = "".join(filename.split(".")[:-1]) + ".gif"
        if new_filename.startswith("-"):
            new_filename = new_filename[1:]
        print(f"filename is: {filename}, quality is: {quality}")
        if re.search(r".+\.mp4|.+\.mkv|.+\.mov|.+\.webm", filename) is not None:
            # r = requests.get(link)
            # vid = io.BytesIO(r.content)
            # vid.seek(0)
            frames_folder = f"frames_{uuid_id}"
            os.mkdir(f"{frames_folder}/")
            frames_path = f"{frames_folder}/frame%04d.png"

            coms = ["ffmpeg", "-i", link, frames_path]
            message = await ctx.send("Extracting frames... This might take a bit.")
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await process.communicate()
            print("FFMPEGGGG")
            print(stdout.decode("utf-8"))
            if stderr is not None:
                await ctx.send(stderr.decode("utf-8"))
            gif_ski_frames_path = f"{frames_folder}/frame*.png"
            gif_ski_frames_path = glob.glob(gif_ski_frames_path)
            # gif_ski_frames_path = ' '.join(gif_ski_frames_path)
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
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await process.communicate()
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
            # print(shlex.join(coms))
            print(shlex.join(coms))
            process = await asyncio.create_subprocess_exec(
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

            await message.edit(content="Sending...")
            try:
                await ctx.send(file=disnake.File(new_filename))
            except disnake.HTTPException as e:
                if e.status == 413:
                    await ctx.send("Too large for server. Sending somewhere else..")
                    coms = [
                        "curl",
                        "--upload-file",
                        new_filename,
                        f"https://transfer.sh/{new_filename}",
                    ]
                    process = await asyncio.create_subprocess_exec(
                        *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )
                    stdout, stderr = await process.communicate()
                    link = stdout.decode("utf-8").splitlines()[-1]
                    await ctx.send(link)
            os.remove(new_filename)
            shutil.rmtree(f"{frames_folder}/")
        elif re.search(r".+\.jpg|.+\.png|.+\.webp", filename) is not None:         
            pre_message = await ctx.send("You... want to turn an image into a gif? Uh ok then.")
            frames_folder = f"frames_{uuid_id}"
            os.mkdir(f"{frames_folder}/")
            frames_path1 = f"{frames_folder}/frame1.png"
            frames_path2 = f"{frames_folder}/frame2.png"

            coms = ["ffmpeg", "-i", link, frames_path1]
            coms2 = ["ffmpeg", "-i", link, frames_path2]
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await process.communicate()
            process = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await process.communicate()            
            print("FFMPEGGGG")
            print(stdout.decode("utf-8"))
            if stderr is not None:
                await ctx.send(stderr.decode("utf-8"))
            gif_ski_frames_path = f"{frames_folder}/frame*.png"
            gif_ski_frames_path = glob.glob(gif_ski_frames_path)
            # gif_ski_frames_path = ' '.join(gif_ski_frames_path)
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
            # print(shlex.join(coms))
            print(shlex.join(coms))
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            

            print("GIFSKI")
            stdout, stderr = await process.communicate()
            print(stdout.decode('utf-8'))
            await message.edit(content="Sending...")
            try:
                await ctx.send(file=disnake.File(new_filename))
            except disnake.HTTPException as e:
                if e.status == 413:
                    await ctx.send("Too large for server. Sending somewhere else..")
                    coms = [
                        "curl",
                        "--upload-file",
                        new_filename,
                        f"https://transfer.sh/{new_filename}",
                    ]
                    process = await asyncio.create_subprocess_exec(
                        *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )
                    stdout, stderr = await process.communicate()
                    link = stdout.decode("utf-8").splitlines()[-1]
                    await ctx.send(link)
            os.remove(new_filename)
            shutil.rmtree(f"{frames_folder}/")       
            await message.delete()
            await pre_message.delete()
        else:
            await ctx.send(
                "I don't support this filetype yet ig. Ping kur0 or smth. <:towashrug:853606191711649812> "
            )

def setup(client):
    client.add_cog(Gif(client))

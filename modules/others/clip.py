from discord.ext import commands
import discord
import asyncio
import re
from datetime import datetime, timedelta, timezone
from shlex import join as shjoin
import math
import os
import subprocess


class Clip(commands.Cog):
    # def __init__(self, client):
    #     self.client = client

    @commands.command()
    async def fastclip(self, ctx, link, start, end, filename):

        if (
            re.match("\d{2}:\d{2}:\d{2}", start) != None
            and re.match("\d{2}:\d{2}:\d{2}", end) != None
        ):
            print("good timestamps!")
        else:
            print("bad timestamps!")
            await ctx.send("Timestamps are wrong. Please provide it in HH:MM:SS")
            return

        message = await ctx.send("Fetching url...")
        coms = ["yt-dlp", "-g", "-f", "best", "--youtube-skip-dash-manifest", link]
        print(shjoin(coms))
        startsplit = start.split(":")
        shour = startsplit[0]
        sminute = startsplit[1]
        ssecond = startsplit[2]
        date_time = datetime.strptime(start, "%H:%M:%S")
        a_timedelta = date_time - datetime(1900, 1, 1)
        seconds = a_timedelta.total_seconds()
        print(seconds)
        if seconds < 30:
            print("less than 30 seconds!")
            result1 = timedelta(
                hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
            )
        else:
            print("it is at least 30 seconds.")
            result1 = timedelta(
                hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
            ) - timedelta(seconds=30)

        endsplit = end.split(":")
        ehour = endsplit[0]
        eminute = endsplit[1]
        esecond = endsplit[2]
        if seconds < 30:
            result2 = timedelta(
                hours=int(ehour), minutes=int(eminute), seconds=int(esecond)
            )
        else:
            result2 = (
                timedelta(hours=int(ehour), minutes=int(eminute), seconds=int(esecond))
                - timedelta(
                    hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
                )
                + timedelta(seconds=30)
            )
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await out.communicate()
        print(stdout)
        print(stderr)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
        aud = dirlinks[1]
        if seconds < 30:
            coms = [
                "ffmpeg",
                "-i",
                vid,
                "-t",
                str(result2),
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                f"{filename}_temp0.mp4",
            ]
        else:
            coms = [
                "ffmpeg",
                "-noaccurate_seek",
                "-ss",
                str(result1),
                "-i",
                vid,
                "-t",
                str(result2),
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                f"{filename}_temp0.mp4",
            ]
        print(shjoin(coms))
        await message.edit(content="Downloading... This will take a while...")
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        # while process.returncode is None:
        #     line = await process.stdout.readline()
        #     if not line:
        #             break
        #     await ctx.send(line.decode('utf-8'))

        stdout, stderr = await process.communicate()
        print(stdout)
        print(stderr.decode("utf-8"))
        # os.rename(filename+".mkv",filename+".mp4")

        def max_le(seq, val):
            """
            Same as max_lt(), but items in seq equal to val apply as well.

            >>> max_le([2, 3, 7, 11], 10)
            7
            >>> max_le((1, 3, 6, 11), 6)
            6
            """

            idx = len(seq) - 1
            while idx >= 0:
                if seq[idx] <= val:
                    return seq[idx]
                idx -= 1

            return None

        def min_gt(seq, val):
            """
            Return smallest item in seq for which item > val applies.
            None is returned if seq was empty or all items in seq were <= val.

            >>> min_gt([1, 3, 6, 7], 4)
            6
            >>> min_gt([2, 4, 7, 11], 5)
            7
            """

            for v in seq:
                if v > val:
                    return v
            return None

        def round_down(n, decimals=0):
            multiplier = 10 ** decimals
            return math.floor(n * multiplier) / multiplier

        coms = [
            "ffprobe",
            "-v",
            "error",
            "-skip_frame",
            "nokey",
            "-show_entries",
            "frame=pkt_pts_time",
            "-select_streams",
            "v",
            "-of",
            "csv=p=0",
            f"{filename}_temp0.mp4",
        ]
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(stderr)
        print(stdout.decode("utf-8"))
        timelist_str = stdout.decode("utf-8").strip().split("\n")
        print(timelist_str)
        timelist_float = [float(i) for i in timelist_str]
        timelist_float.sort()
        print(timelist_float)

        # remuxes so keyframes work, magic.
        coms = [
            "ffmpeg-git/ffmpeg",
            "-i",
            f"{filename}_temp0.mp4",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            f"{filename}_temp.mp4",
        ]
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(stdout.decode("utf-8"))

        round_number = 1
        round_frames = False

        if seconds < 30:
            if round_frames == True:
                keyframe = round_down(max_le(timelist_float, seconds), round_number)
            else:
                prev_keyframe = max_le(timelist_float, seconds)
                if prev_keyframe == timelist_float[-1]:  # if prev_keyframe is last
                    coms = [
                        "ffprobe",
                        "-v",
                        "error",
                        "-show_entries",
                        "format=duration",
                        "-of",
                        "default=noprint_wrappers=1:nokey=1",
                        f"{filename}_temp0.mp4",
                    ]  # get duration
                    process = await asyncio.create_subprocess_exec(
                        *coms,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    stdout, stderr = await process.communicate()
                    print(stderr)
                    next_keyframe = float(stdout.decode("utf-8"))
                else:
                    next_keyframe = min_gt(timelist_float, seconds)
                print(f"after {prev_keyframe}")
                print(f"before {next_keyframe}")
                if next_keyframe == None:
                    print("no next keyframe!")
                    keyframe = prev_keyframe
                else:
                    keyframe = (prev_keyframe + next_keyframe) / 2
            print(f"keyframe is {keyframe:.6f}")
            if round_down(seconds - prev_keyframe, round_number) == 0:
                await ctx.send(
                    "<:callipog:850365252637032479> Poggers. No need to clip to nearest keyframe."
                )
            else:
                await ctx.send(
                    f"Clipping {round_down(seconds - prev_keyframe, round_number)} seconds earlier to nearest keyframe..."
                )

        else:
            if round_frames == True:
                keyframe = round_down(max_le(timelist_float, 30), round_number)
            else:
                prev_keyframe = max_le(timelist_float, 30)
                next_keyframe = min_gt(timelist_float, 30)
                if next_keyframe == None:
                    print("no next keyframe!")
                    keyframe = prev_keyframe
                else:
                    keyframe = (prev_keyframe + next_keyframe) / 2
            print(f"keyframe is {keyframe}")
            if round_down(30 - prev_keyframe, round_number) == 0:
                await ctx.send(
                    "<:callipog:850365252637032479> Poggers. No need to clip to nearest keyframe."
                )
            else:
                await ctx.send(
                    f"Clipping {round_down(30 - prev_keyframe, round_number)} seconds earlier to nearest keyframe..."
                )

        coms = [
            "ffmpeg",
            "-noaccurate_seek",
            "-ss",
            "{:.6f}".format(keyframe),
            "-i",
            f"{filename}_temp.mp4",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-avoid_negative_ts",
            "make_zero",
            f"{filename}.mp4",
        ]
        print(shjoin(coms))
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(stdout)
        print(stderr.decode("utf-8"))

        coms = [
            "ffprobe",
            "-v",
            "error",
            "-skip_frame",
            "nokey",
            "-show_entries",
            "frame=pkt_pts_time",
            "-select_streams",
            "v",
            "-of",
            "csv=p=0",
            f"{filename}.mp4",
        ]
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(stderr)
        print("final keyframes:")
        print(stdout.decode("utf-8"))

        try:

            await ctx.send(file=discord.File(f"{filename}.mp4"))
        except Exception:
            await message.edit(content="I failed.")
        await ctx.send(ctx.message.author.mention)
        os.remove(f"{filename}.mp4")
        os.remove(f"{filename}_temp0.mp4")
        os.remove(f"{filename}_temp.mp4")
        await message.delete()

    @commands.command()
    async def idclip(self, ctx, link, start, end, filename, id, id2):

        if (
            re.match("\d{2}:\d{2}:\d{2}", start) != None
            and re.match("\d{2}:\d{2}:\d{2}", end) != None
        ):
            print("good timestamps!")
        else:
            print("bad timestamps!")
            await ctx.send("Timestamps are wrong. Please provide it in HH:MM:SS")
            return

        message = await ctx.send("Fetching url...")
        coms = ["yt-dlp", "-g", "-f", f"{id}+{id2}", link]
        print(shjoin(coms))
        startsplit = start.split(":")
        shour = startsplit[0]
        sminute = startsplit[1]
        ssecond = startsplit[2]
        date_time = datetime.strptime(start, "%H:%M:%S")
        a_timedelta = date_time - datetime(1900, 1, 1)
        seconds = a_timedelta.total_seconds()
        print(seconds)
        if seconds < 30:
            print("less than 30 seconds!")
            result1 = timedelta(
                hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
            )
        else:
            print("it is at least 30 seconds.")
            result1 = timedelta(
                hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
            ) - timedelta(seconds=30)

        endsplit = end.split(":")
        ehour = endsplit[0]
        eminute = endsplit[1]
        esecond = endsplit[2]
        if seconds < 30:
            result2 = timedelta(
                hours=int(ehour), minutes=int(eminute), seconds=int(esecond)
            )
        else:
            result2 = (
                timedelta(hours=int(ehour), minutes=int(eminute), seconds=int(esecond))
                - timedelta(
                    hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
                )
                + timedelta(seconds=30)
            )
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await out.communicate()
        print(stdout)
        print(stderr)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
        aud = dirlinks[1]
        if seconds < 30:
            coms = [
                "ffmpeg",
                "-i",
                vid,
                "-t",
                str(result2),
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                f"{filename}_temp.mp4",
            ]
        else:
            coms = [
                "ffmpeg",
                "-noaccurate_seek",
                "-ss",
                str(result1),
                "-i",
                vid,
                "-t",
                str(result2),
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                f"{filename}_temp.mp4",
            ]
        print(shjoin(coms))
        await message.edit(content="Downloading... This will take a while...")
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        while process.returncode is None:
            line = await process.stdout.readline()
            if not line:
                break
            # await message.edit(content=line.decode('utf-8'))
            await ctx.send(line.decode("utf-8"))
            # await asyncio.sleep(1)

        # stdout, stderr = await process.communicate()
        print(stdout)
        print(stderr.decode("utf-8"))
        # os.rename(filename+".mkv",filename+".mp4")

        def max_le(seq, val):
            """
            Same as max_lt(), but items in seq equal to val apply as well.

            >>> max_le([2, 3, 7, 11], 10)
            7
            >>> max_le((1, 3, 6, 11), 6)
            6
            """

            idx = len(seq) - 1
            while idx >= 0:
                if seq[idx] <= val:
                    return seq[idx]
                idx -= 1

            return None

        def min_gt(seq, val):
            """
            Return smallest item in seq for which item > val applies.
            None is returned if seq was empty or all items in seq were <= val.

            >>> min_gt([1, 3, 6, 7], 4)
            6
            >>> min_gt([2, 4, 7, 11], 5)
            7
            """

            for v in seq:
                if v > val:
                    return v
            return None

        def round_down(n, decimals=0):
            multiplier = 10 ** decimals
            return math.floor(n * multiplier) / multiplier

        coms = [
            "ffprobe",
            "-v",
            "error",
            "-skip_frame",
            "nokey",
            "-show_entries",
            "frame=pkt_pts_time",
            "-select_streams",
            "v",
            "-of",
            "csv=p=0",
            f"{filename}_temp.mp4",
        ]
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(stderr)
        print(stdout.decode("utf-8"))
        timelist_str = stdout.decode("utf-8").strip().split("\n")
        print(timelist_str)
        timelist_float = [float(i) for i in timelist_str]
        print(timelist_float)

        round_number = 1
        round_frames = False

        if seconds < 30:
            if round_frames == True:
                keyframe = round_down(max_le(timelist_float, seconds), round_number)
            else:
                prev_keyframe = max_le(timelist_float, seconds)
                next_keyframe = min_gt(timelist_float, seconds)
                print(f"after {prev_keyframe}")
                print(f"before {next_keyframe}")
                if next_keyframe == None:
                    print("no next keyframe!")
                    keyframe = prev_keyframe
                else:
                    keyframe = (prev_keyframe + next_keyframe) / 2
            print(f"keyframe is {keyframe:.6f}")
            await ctx.send(
                f"Clipping {round_down(seconds - prev_keyframe, round_number)} seconds earlier to nearest keyframe..."
            )

        else:
            if round_frames == True:
                keyframe = round_down(max_le(timelist_float, 30), round_number)
            else:
                prev_keyframe = max_le(timelist_float, 30)
                next_keyframe = min_gt(timelist_float, 30)
                keyframe = (prev_keyframe + next_keyframe) / 2
            print(f"keyframe is {keyframe}")
            await ctx.send(
                f"Clipping {round_down(30 - prev_keyframe, round_number)} seconds earlier to nearest keyframe..."
            )

        coms = [
            "ffmpeg",
            "-noaccurate_seek",
            "-ss",
            "{:.6f}".format(keyframe),
            "-i",
            f"{filename}_temp.mp4",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-avoid_negative_ts",
            "make_zero",
            f"{filename}.mp4",
        ]
        print(shjoin(coms))
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(stdout)
        print(stderr.decode("utf-8"))

        coms = [
            "ffprobe",
            "-v",
            "error",
            "-skip_frame",
            "nokey",
            "-show_entries",
            "frame=pkt_pts_time",
            "-select_streams",
            "v",
            "-of",
            "csv=p=0",
            f"{filename}.mp4",
        ]
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(stderr)
        print("final keyframes:")
        print(stdout.decode("utf-8"))

        try:

            await ctx.send(file=discord.File(f"{filename}.mp4"))
        except Exception as e:
            await message.edit(content="I failed.")
            await ctx.send(e)
            print(f"Could not send video\n{e}")
        await ctx.send(ctx.message.author.mention)
        os.remove(f"{filename}.mp4")
        os.remove(f"{filename}_temp.mp4")
        await message.delete()

    @commands.command()
    async def clipaudio(self, ctx, link, start, end, filename, filetype=None):
        if filetype not in ["mp3", "wav", "ogg"]:
            await ctx.send(
                "Missing or no filetype provided. I can do mp3, wav, and ogg."
            )
            return

        if (
            re.match("\d{2}:\d{2}:\d{2}", start) != None
            and re.match("\d{2}:\d{2}:\d{2}", end) != None
        ):
            print("good timestamps!")
        else:
            print("bad timestamps!")
            await ctx.send("Timestamps are wrong. Please provide it in HH:MM:SS")
            return

        message = await ctx.send("Fetching url...")
        coms = ["yt-dlp", "-g", "-f", "251", link]
        print(shjoin(coms))
        startsplit = start.split(":")
        shour = startsplit[0]
        sminute = startsplit[1]
        ssecond = startsplit[2]
        date_time = datetime.strptime(start, "%H:%M:%S")
        a_timedelta = date_time - datetime(1900, 1, 1)
        seconds = a_timedelta.total_seconds()
        print(seconds)
        if seconds < 30:
            print("less than 30 seconds!")
            result1 = timedelta(
                hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
            )
        else:
            print("it is at least 30 seconds.")
            result1 = timedelta(
                hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
            ) - timedelta(seconds=30)

        endsplit = end.split(":")
        ehour = endsplit[0]
        eminute = endsplit[1]
        esecond = endsplit[2]
        result2 = timedelta(
            hours=int(ehour), minutes=int(eminute), seconds=int(esecond)
        ) - timedelta(hours=int(shour), minutes=int(sminute), seconds=int(ssecond))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await out.communicate()
        print(stdout)
        print(stderr)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
        aud = dirlinks[1]
        if seconds < 30:
            coms = [
                "ffmpeg",
                "-i",
                vid,
                "-ss",
                str(result1),
                "-t",
                str(result2),
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                f"{filename}.ogg",
            ]
        else:
            coms = [
                "ffmpeg",
                "-ss",
                str(result1),
                "-i",
                vid,
                "-ss",
                "30",
                "-t",
                str(result2),
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                f"{filename}.ogg",
            ]
        print(shjoin(coms))
        await message.edit(content="Downloading... This will take a while...")
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(stdout)
        print(stderr.decode("utf-8"))

        if filetype == "ogg":
            pass
        elif filetype == "mp3":
            coms = [
                "ffmpeg",
                "-i",
                f"{filename}.ogg",
                "-codec:a",
                "libmp3lame",
                "-q:a",
                "0",
                f"{filename}.mp3",
            ]
            print(shjoin(coms))
            await message.edit(content="Using libmp3lame to convert to VBR 0 MP3...")
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            print(stdout)
            print(stderr.decode("utf-8"))
        elif filetype == "wav":
            coms = ["ffmpeg", "-i", f"{filename}.ogg", f"{filename}.wav"]
            print(shjoin(coms))
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            print(stdout)
            print(stderr.decode("utf-8"))

        # os.rename(filename+".mkv",filename+".mp4")
        try:
            await ctx.send(file=discord.File(f"{filename}.{filetype.lower()}"))
        except Exception:
            await message.edit(content="I failed.")
        await ctx.send(ctx.message.author.mention)
        os.remove(f"{filename}.ogg")
        os.remove(f"{filename}.{filetype.lower()}")
        await message.delete()

    @commands.command()
    async def clip(self, ctx, link, start, end, filename):

        if (
            re.match("\d{2}:\d{2}:\d{2}", start) != None
            and re.match("\d{2}:\d{2}:\d{2}", end) != None
        ):
            print("good timestamps!")
        else:
            print("bad timestamps!")
            await ctx.send("Timestamps are wrong. Please provide it in HH:MM:SS")
            return

        if os.path.isfile(f"{filename}.mkv"):
            os.remove(f"{filename}.mkv")
        if os.path.isfile(f"{filename}.mp4"):
            os.remove(f"{filename}.mp4")
        message = await ctx.send("Fetching url...")
        coms = ["yt-dlp", "-g", "-f", "best", "--youtube-skip-dash-manifest", link]
        print(shjoin(coms))
        startsplit = start.split(":")
        shour = startsplit[0]
        sminute = startsplit[1]
        ssecond = startsplit[2]
        date_time = datetime.strptime(start, "%H:%M:%S")
        a_timedelta = date_time - datetime(1900, 1, 1)
        seconds = a_timedelta.total_seconds()
        print(seconds)
        if seconds < 30:
            print("less than 30 seconds!")
            result1 = timedelta(
                hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
            )
        else:
            print("it is at least 30 seconds.")
            result1 = timedelta(
                hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
            ) - timedelta(seconds=30)
        endsplit = end.split(":")
        ehour = endsplit[0]
        eminute = endsplit[1]
        esecond = endsplit[2]
        result2 = timedelta(
            hours=int(ehour), minutes=int(eminute), seconds=int(esecond)
        ) - timedelta(hours=int(shour), minutes=int(sminute), seconds=int(ssecond))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = await out.communicate()
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
        aud = dirlinks[1]
        if seconds < 30:
            coms = [
                "ffmpeg",
                "-ss",
                str(result1),
                "-i",
                vid,
                "-t",
                str(result2),
                "-c:v",
                "libx264",
                "-c:a",
                "copy",
                f"{filename}.mkv",
            ]
        else:
            coms = [
                "ffmpeg",
                "-ss",
                str(result1),
                "-i",
                vid,
                "-ss",
                "30",
                "-t",
                str(result2),
                "-c:v",
                "libx264",
                "-c:a",
                "copy",
                f"{filename}.mkv",
            ]
        print(shjoin(coms))
        await message.edit(content="Downloading... This will take a while...")
        try:
            process = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            # for line in process.stdout:
            # print(line)
            # process.communicate()
            while process.returncode is None:
                # await asyncio.sleep(1)

                line = await process.stdout.read(100)
                if not line:
                    break
                # print(line.decode('utf-8'))
                linedec = line.decode("utf-8")

                if "frame=" in linedec:
                    if not "00:00:00.00" in linedec.split("=")[5].split(" ")[0]:
                        strpcurr = datetime.strptime(
                            linedec.split("=")[5].split(" ")[0], "%H:%M:%S.%f"
                        )
                        currtime = timedelta(
                            hours=strpcurr.hour,
                            minutes=strpcurr.minute,
                            seconds=strpcurr.second,
                            microseconds=strpcurr.microsecond,
                        )
                        print(linedec)
                        percentage = (
                            currtime.total_seconds() / result2.total_seconds()
                        ) * 100
                        print(f"{percentage}% complete...")
                        await message.edit(
                            content=f"{round(percentage, 2)}% complete..."
                        )
            os.rename(f"{filename}.mkv", f"{filename}.mp4")
            await ctx.send(file=discord.File(f"{filename}.mp4"))
            # await ctx.send(ctx.message.author.mention)
            os.remove(f"{filename}.mp4")
            await message.delete()
        except ValueError:
            await message.edit(content="An error occured... Uh, try it again.")

    @commands.command()
    async def fastclip3(self, ctx, link, start, end, filename):
        message = await ctx.send("Fetching url...")
        coms = ["yt-dlp", "-g", "-f", "best", "--youtube-skip-dash-manifest", link]
        print(shjoin(coms))
        startsplit = start.split(":")
        shour = startsplit[0]
        sminute = startsplit[1]
        ssecond = startsplit[2]
        date_time = datetime.strptime(start, "%H:%M:%S")
        a_timedelta = date_time - datetime(1900, 1, 1)
        seconds = a_timedelta.total_seconds()
        print(seconds)
        if seconds < 30:
            print("less than 30 seconds!")
            result1 = timedelta(
                hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
            )
        else:
            print("it is at least 30 seconds.")
            result1 = timedelta(
                hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
            ) - timedelta(seconds=30)

        endsplit = end.split(":")
        ehour = endsplit[0]
        eminute = endsplit[1]
        esecond = endsplit[2]
        result2 = timedelta(
            hours=int(ehour), minutes=int(eminute), seconds=int(esecond)
        ) - timedelta(hours=int(shour), minutes=int(sminute), seconds=int(ssecond))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await out.communicate()
        print(stdout)
        print(stderr)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
        aud = dirlinks[1]
        if seconds < 30:
            coms = [
                "ffmpeg",
                "-ss",
                str(result1),
                "-i",
                vid,
                "-t",
                str(result2),
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                f"{filename}.mp4",
            ]
        else:
            coms = [
                "ffmpeg",
                "-ss",
                str(result1),
                "-i",
                vid,
                "-ss",
                "30",
                "-t",
                str(result2),
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                f"{filename}.mp4",
            ]
        print(shjoin(coms))
        await message.edit(content="Downloading... This will take a while...")
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(stdout)
        print(stderr.decode("utf-8"))
        # os.rename(filename+".mkv",filename+".mp4")
        try:
            await ctx.send(file=discord.File(f"{filename}.mp4"))
        except Exception:
            await message.edit(content="I failed.")
        await ctx.send(ctx.message.author.mention)
        os.remove(f"{filename}.mp4")
        await message.delete()

    @commands.command()
    async def fastclip2(self, ctx, link, start, end, filename):
        message = await ctx.send("Fetching url...")
        coms = ["yt-dlp", "-g", "-f", "best", "--youtube-skip-dash-manifest", link]
        print(shjoin(coms))
        startsplit = start.split(":")
        shour = startsplit[0]
        sminute = startsplit[1]
        ssecond = startsplit[2]
        result1 = timedelta(
            hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
        )
        endsplit = end.split(":")
        ehour = endsplit[0]
        eminute = endsplit[1]
        esecond = endsplit[2]
        result2 = timedelta(
            hours=int(ehour), minutes=int(eminute), seconds=int(esecond)
        ) - timedelta(hours=int(shour), minutes=int(sminute), seconds=int(ssecond))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await out.communicate()
        print(stdout)
        print(stderr)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
        aud = dirlinks[1]
        coms = [
            "ffmpeg",
            "-ss",
            str(result1),
            "-i",
            vid,
            "-t",
            str(result2),
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            f"{filename}.mp4",
        ]

        print(shjoin(coms))
        await message.edit(content="Downloading... This will take a while...")
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        # stdout, stderr = await process.communicate()
        while process.returncode is None:
            line = await process.stdout.read(100)
            if not line:
                break
            # await message.edit(content=line.decode('utf-8'))
            await ctx.send(line.decode("utf-8"))
            await asyncio.sleep(1)
        if process.returncode != 0:
            await ctx.send("return code is not 0. i give up")
            return
        # print(stdout)
        # print(stderr)
        # os.rename(filename+".mkv",filename+".mp4")
        try:
            await ctx.send(file=discord.File(f"{filename}.mp4"))
        except Exception:
            await message.edit(content="I failed.")
        await ctx.send(ctx.message.author.mention)
        os.remove(f"{filename}.mp4")
        await message.delete()


def setup(client):
    client.add_cog(Clip(client))

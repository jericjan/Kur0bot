from disnake.ext import commands
import asyncio
import re
from datetime import datetime, timedelta
from shlex import join as shjoin
import math
import os
import subprocess
from myfunctions import subprocess_runner, file_handler


class Clip(commands.Cog):
    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def fastclip(self, ctx, link, start, end, *, filename):
        start = start.strip(" ")
        end = end.strip(" ")
        filename = filename.replace(" ", "_")
        zeroes = "00:00:00"
        if len(start) < 8:
            start = zeroes[: -len(start)] + start
        if len(end) < 8:
            end = zeroes[: -len(end)] + end
        if (
            re.match("\d{2}(:|;)\d{2}(:|;)\d{2}", start) != None
            and re.match("\d{2}(:|;)\d{2}(:|;)\d{2}", end) != None
        ):
            print("good timestamps!")
        else:
            print("bad timestamps!")
            await ctx.send("Timestamps are wrong. Please provide it in HH:MM:SS")
            return

        start = start.replace(";", ":")
        end = end.replace(";", ":")

        message = await ctx.send("Fetching url...")
        coms = [
            "yt-dlp",
            "-g",
            "-f",
            "b",
            "--youtube-skip-dash-manifest",
            "--no-warnings",
            link,
        ]
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
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
        if vid.endswith("index.m3u8"):
            await ctx.send(
                "yeah sorry bud, can't clip this one. m guessing it's a stream and it hasn't finished processing. come back later and try again homie."
            )
            return
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
                "-y",
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
                "-movflags",
                "faststart",
                "-y",
                f"{filename}_temp0.mp4",
            ]
        await message.edit(content="Downloading... This will take a while...")
        print(shjoin(coms))
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

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
            multiplier = 10**decimals
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
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        timelist_str = stdout.decode("utf-8").strip().split("\n")
        print(timelist_str)

        def isfloat(num):
            try:
                float(num)
                return True
            except ValueError:
                return False

        timelist_float = [float(i) for i in timelist_str if isfloat(i)]
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
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

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
                    process, stdout, stderr = await subprocess_runner.run_subprocess(
                        coms
                    )
                    next_keyframe = float(stdout.decode("utf-8"))
                else:
                    next_keyframe = min_gt(timelist_float, seconds)
                print(f"after {prev_keyframe}")
                print(f"before {next_keyframe}")
                if next_keyframe == None:
                    print("no next keyframe!(0)")
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
                    process, stdout, stderr = await subprocess_runner.run_subprocess(
                        coms
                    )
                    next_keyframe = float(stdout.decode("utf-8"))
                else:
                    next_keyframe = min_gt(timelist_float, 30)
                print(f"after {prev_keyframe}")
                print(f"before {next_keyframe}")
                if next_keyframe == None:
                    print("no next keyframe!(1)")
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
            f"{keyframe:.6f}",
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
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

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
        print("final keyframes:")
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        await file_handler.send_file(ctx, message, f"{filename}.mp4")
        await ctx.send(ctx.message.author.mention)
        file_handler.delete_file(f"{filename}.mp4")
        file_handler.delete_file(f"{filename}_temp0.mp4")
        file_handler.delete_file(f"{filename}_temp.mp4")

    ############################################################################
    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def fastclipsub(self, ctx, link, start, end, *, filename):
        filename = filename.replace(" ", "_")
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
        coms = [
            "yt-dlp",
            "-g",
            "-f",
            "b",
            "--youtube-skip-dash-manifest",
            "--no-warnings",
            link,
        ]
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
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]

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
                "-y",
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
                "-y",
                f"{filename}_temp0.mp4",
            ]
        await message.edit(content="Downloading... This will take a while...")
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

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
            multiplier = 10**decimals
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
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)
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
            "-y",
            f"{filename}_temp.mp4",
        ]
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

        round_number = 1
        round_frames = False
        seconds_earlier = 0

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
                    process, stdout, stderr = await subprocess_runner.run_subprocess(
                        coms
                    )
                    next_keyframe = float(stdout.decode("utf-8"))
                else:
                    next_keyframe = min_gt(timelist_float, seconds)
                print(f"after {prev_keyframe}")
                print(f"before {next_keyframe}")
                if next_keyframe == None:
                    print("no next keyframe!(0)")
                    keyframe = prev_keyframe
                else:
                    keyframe = (prev_keyframe + next_keyframe) / 2
            print(f"keyframe is {keyframe:.6f}")
            if round_down(seconds - prev_keyframe, round_number) == 0:
                await ctx.send(
                    "<:callipog:850365252637032479> Poggers. No need to clip to nearest keyframe."
                )
            else:
                seconds_earlier = seconds - prev_keyframe
                await ctx.send(
                    f"Clipping {round_down(seconds_earlier, round_number)} seconds earlier to nearest keyframe..."
                )

        else:
            if round_frames == True:
                keyframe = round_down(max_le(timelist_float, 30), round_number)
            else:
                prev_keyframe = max_le(timelist_float, 30)
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
                    process, stdout, stderr = await subprocess_runner.run_subprocess(
                        coms
                    )
                    next_keyframe = float(stdout.decode("utf-8"))
                else:
                    next_keyframe = min_gt(timelist_float, 30)
                print(f"after {prev_keyframe}")
                print(f"before {next_keyframe}")
                if next_keyframe == None:
                    print("no next keyframe!(1)")
                    keyframe = prev_keyframe
                else:
                    keyframe = (prev_keyframe + next_keyframe) / 2
            print(f"keyframe is {keyframe}")
            if round_down(30 - prev_keyframe, round_number) == 0:
                await ctx.send(
                    "<:callipog:850365252637032479> Poggers. No need to clip to nearest keyframe."
                )
            else:
                seconds_earlier = 30 - prev_keyframe
                await ctx.send(
                    f"Clipping {round_down(seconds_earlier, round_number)} seconds earlier to nearest keyframe..."
                )

        coms = [
            "ffmpeg",
            "-noaccurate_seek",
            "-ss",
            f"{keyframe:.6f}",
            "-i",
            f"{filename}_temp.mp4",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-avoid_negative_ts",
            "make_zero",
            "-y",
            f"{filename}_nosub.mp4",
        ]

        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

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
            f"{filename}_nosub.mp4",
        ]
        print("final keyframes:")
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

        await message.edit(content="Getting fancy subs... (en, srv3)")
        coms = [
            "yt-dlp",
            "--sub-lang",
            "en",
            "--sub-format",
            "srv3",
            "--write-sub",
            "--skip-download",
            link,
        ]
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        try:
            sub_name = re.findall(
                r"(?<=Writing video subtitles to: ).+", stdout.decode("utf-8")
            )[0]
        except:
            coms = [
                "yt-dlp",
                "--sub-lang",
                "en-US",
                "--sub-format",
                "srv3",
                "--write-sub",
                "--skip-download",
                link,
            ]
            process, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            try:
                sub_name = re.findall(
                    r"(?<=Writing video subtitles to: ).+", stdout.decode("utf-8")
                )[0]
            except:
                await message.edit(content="I give up. I dunno man...")
                return
        await message.edit(content="Converting subs...")
        coms = ["mono", "ytsubconverter/YTSubConverter.exe", sub_name]
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

        sub_name_ass = ".".join(sub_name.split(".")[:-1]) + ".ass"
        sub_name_ass2 = ".".join(sub_name.split(".")[:-2]) + "_2.en.ass"
        print(sub_name_ass)

        sub_delay = timedelta(
            hours=int(shour), minutes=int(sminute), seconds=int(ssecond)
        ) - timedelta(seconds=seconds_earlier)
        await message.edit(content="Trimming subs...")
        coms = [
            "ffmpeg",
            "-i",
            sub_name_ass,
            "-ss",
            str(sub_delay),
            "-to",
            end,
            "-y",
            sub_name_ass2,
        ]
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

        await message.edit(content="Burning subs into video...")
        coms = [
            "ffmpeg",
            "-i",
            f"{filename}_nosub.mp4",
            "-vf",
            f"subtitles='{sub_name_ass2}'",
            "-y",
            f"{filename}.mp4",
        ]
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        await file_handler.send_file(ctx, message, f"{filename}.mp4")
        await ctx.send(ctx.message.author.mention)
        file_handler.delete_file(sub_name)
        file_handler.delete_file(sub_name_ass)
        file_handler.delete_file(sub_name_ass2)
        file_handler.delete_file(f"{filename}.mp4")
        file_handler.delete_file(f"{filename}_nosub.mp4")
        file_handler.delete_file(f"{filename}_temp0.mp4")
        file_handler.delete_file(f"{filename}_temp.mp4")

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
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
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
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
        process = await asyncio.create_subprocess_exec(  # reads stdout live
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        while process.returncode is None:
            line = await process.stdout.readline()
            if not line:
                break
            await ctx.send(line.decode("utf-8"))

        print(stdout)
        print(stderr.decode("utf-8"))

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
            multiplier = 10**decimals
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
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

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
            f"{keyframe:.6f}",
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

        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

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
        print("final keyframes:")
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        await file_handler.send_file(ctx, message, f"{filename}.mp4")
        await ctx.send(ctx.message.author.mention)
        file_handler.delete_file(f"{filename}.mp4")
        file_handler.delete_file(f"{filename}_temp.mp4")

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
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
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
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
        await message.edit(content="Downloading... This will take a while...")
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)

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
            await message.edit(content="Using libmp3lame to convert to VBR 0 MP3...")
            process, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        elif filetype == "wav":
            coms = ["ffmpeg", "-i", f"{filename}.ogg", f"{filename}.wav"]
            process, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        await file_handler.send_file(ctx, message, f"{filename}.{filetype.lower()}")
        await ctx.send(ctx.message.author.mention)
        file_handler.delete_file(f"{filename}.ogg")
        file_handler.delete_file(f"{filename}.{filetype.lower()}")

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
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
        coms = [
            "yt-dlp",
            "-g",
            "-f",
            "b",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "--no-warnings",
            link,
        ]
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
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
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
            process = await asyncio.create_subprocess_exec(  # reads stdout live
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while process.returncode is None:

                line = await process.stdout.read(100)
                if not line:
                    break
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
            await file_handler.send_file(ctx, message, f"{filename}.mp4")
            file_handler.delete_file(f"{filename}.mp4")
        except ValueError:
            await message.edit(content="An error occured... Uh, try it again.")

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def fastclip3(self, ctx, link, start, end, filename):
        message = await ctx.send("Fetching url...")
        coms = [
            "yt-dlp",
            "-g",
            "-f",
            "b",
            "--youtube-skip-dash-manifest",
            "--no-warnings",
            link,
        ]
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
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
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

        await message.edit(content="Downloading... This will take a while...")
        process, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        await file_handler.send_file(ctx, message, f"{filename}.mp4")
        await ctx.send(ctx.message.author.mention)
        file_handler.delete_file(f"{filename}.mp4")

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def fastclip2(self, ctx, link, start, end, filename):
        message = await ctx.send("Fetching url...")
        coms = [
            "yt-dlp",
            "-g",
            "-f",
            "b",
            "--youtube-skip-dash-manifest",
            "--no-warnings",
            link,
        ]
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
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        dirlinks = stdout.decode("utf-8").split("\n")
        vid = dirlinks[0]
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
        process = await asyncio.create_subprocess_exec(  # reads stdout live
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        while process.returncode is None:
            line = await process.stdout.read(100)
            if not line:
                break
            await ctx.send(line.decode("utf-8"))
            await asyncio.sleep(1)
        if process.returncode != 0:
            await ctx.send("return code is not 0. i give up")
            return
        await file_handler.send_file(ctx, message, f"{filename}.mp4")
        await ctx.send(ctx.message.author.mention)
        file_handler.delete_file(f"{filename}.mp4")


def setup(client):
    client.add_cog(Clip(client))

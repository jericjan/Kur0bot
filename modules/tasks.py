# pylint: disable=E0102


import asyncio
import os
import time
from datetime import datetime
from functools import partial, wraps
from io import BytesIO
from pathlib import Path
import aiohttp
import re

from disnake.ext import commands, tasks

from myfunctions import subprocess_runner


class MyTasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delete_temp_files.start()
        self.update_ytdlp.start()
        # self.cycle_banner.start()
        self.saved_time = time.time()
        self.banner_idx = -1
    def cog_unload(self):
        self.delete_temp_files.cancel()
        self.update_ytdlp.cancel()
        self.cycle_banner.cancel()

    def wrap(func):
        @wraps(func)
        async def run(*args, loop=None, executor=None, **kwargs):
            if loop is None:
                loop = asyncio.get_event_loop()
            pfunc = partial(func, *args, **kwargs)
            return await loop.run_in_executor(executor, pfunc)

        return run

    @wrap
    def magic(self):
        files = os.listdir(r"/home/kur0/Kur0bot/temp")
        files = ["temp/" + x for x in files]
        return files

    @wrap
    def magic2(self, files):
        self.saved_time = time.time()
        for f in files:
            creation_time = os.path.getctime(f)
            print(f"{f} is {self.saved_time - creation_time} old")
            if (self.saved_time - creation_time) / (
                3600
            ) >= 12:  # if file is older than 12 hours, remove
                os.unlink(f)
                print(f"{f} removed")

    @tasks.loop(hours=1)
    async def delete_temp_files(self):
        files = await self.magic()
        channel = self.client.get_channel(976064150935576596)
        nl = "\n"
        await channel.send(
            "-------------------------------------------------\n"
            f"{time.time() - self.saved_time}\nfiles are: \n{nl.join(files)}\n"
            "-------------------------------------------------"
        )
        await self.magic2(files)

    @delete_temp_files.before_loop
    async def before_delete(self):
        print("waiting...")
        await self.client.wait_until_ready()

    @tasks.loop(hours=24)
    async def update_ytdlp(self):
        print("Checking yt-dlp version...")
        _out, stdout, _stderr = await subprocess_runner.run_subprocess(
            "poetry show yt-dlp", shell=True
        )
        # channel = self.client.get_channel(976064150935576596)
        resp = stdout.decode("utf-8")
        try:
            curr_ver = re.search(r"(version +: )(\S+)", resp).group(2)
        except:
            print("Could not find yt-dlp version.")
            return

        async with aiohttp.ClientSession() as session:
            async with session.get("https://pypi.org/pypi/yt-dlp/json") as resp:
                data = await resp.json()
        latest_ver = data.get("info", {}).get("version")

        if curr_ver == latest_ver:
            print(f"yt-dlp is up to date! ({curr_ver})")
        else:
            print(f"yt-dlp needs an update! ({curr_ver} => {latest_ver})")
            _out, _stdout, _stderr = await subprocess_runner.run_subprocess(
                ["poetry", "add", f"yt-dlp=={latest_ver}"]
            )
            print(f"yt-dlp has been updated! ({latest_ver})")

    @update_ytdlp.before_loop
    async def before_delete(self):
        print("waiting 2...")
        await self.client.wait_until_ready()

    def get_current_index(
        self, start_time: datetime, interval_minutes: int, total_items: int
    ) -> int:
        # Calculate the total elapsed time in minutes
        now = datetime.now()
        elapsed_minutes = int((now - start_time).total_seconds() / 60)

        # Calculate the current index
        index = (elapsed_minutes // interval_minutes) % total_items
        return index

    @tasks.loop(minutes=1)
    async def cycle_banner(self):
        banner_root = Path("images/banner_cycle")
        imgs = ["banner.gif", "image.png", "trmup.jpg"]

        # Random time just to start cycle at 00:00:00
        fixed_start_time = datetime(2024, 12, 8, 0, 0, 0)

        interval = 15
        total_items = len(imgs)

        # Get the current index
        current_index = self.get_current_index(fixed_start_time, interval, total_items)
        print(f"The current banner index is: {current_index}")

        if self.banner_idx != current_index:
            with (banner_root / imgs[current_index]).open("rb") as f:
                banner_bytes = BytesIO(f.read())
            banner_bytes.seek(0)

            tos = await self.client.fetch_guild(938255956247183451)
            await tos.edit(banner=banner_bytes.read())
            self.banner_idx = current_index

    @cycle_banner.before_loop
    async def before_delete(self):
        print("waiting 3...")
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(MyTasks(client))

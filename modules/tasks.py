# pylint: disable=E0102


import asyncio
import os
import time
from functools import partial, wraps

from disnake.ext import commands, tasks

from myfunctions import subprocess_runner


class MyTasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.delete_temp_files.start()
        self.update_ytdlp.start()
        self.saved_time = time.time()

    def cog_unload(self):
        self.delete_temp_files.cancel()
        self.update_ytdlp.cancel()

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
        _out, stdout, _stderr = await subprocess_runner.run_subprocess(
            "poetry show -l | grep yt-dlp", shell=True
        )
        channel = self.client.get_channel(976064150935576596)
        resp = stdout.decode("utf-8")
        clean_list = [x for x in resp.split(" ") if x != ""]
        curr_ver = clean_list[1]
        latest_ver = clean_list[2]
        if curr_ver == latest_ver:
            await channel.send(f"yt-dlp is up to date! ({curr_ver})")
        else:
            await channel.send(f"yt-dlp needs an update! ({curr_ver} => {latest_ver})")
            _out, _stdout, _stderr = await subprocess_runner.run_subprocess(
                "poetry", "add", f"yt-dlp=={latest_ver}"
            )
            await channel.send(f"yt-dlp has been updated! ({latest_ver})")

    @update_ytdlp.before_loop
    async def before_delete(self):
        print("waiting 2...")
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(MyTasks(client))

import asyncio
import atexit
import logging
import os
import signal
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Optional, Literal, Coroutine

import aiohttp
import dateutil.parser as dp
import disnake
import disnake.ext
import disnake.ext.commands
import pytz
from disnake import Webhook
from disnake.ext import commands
from dotenv import load_dotenv

from keep_alive import keep_alive

start_time = time.time()
print(f"Running Disnake {disnake.__version__}")

logging.getLogger("asyncio").setLevel(logging.DEBUG)


load_dotenv()
print(f"Asyncio Debug Mode: {os.getenv('PYTHONASYNCIODEBUG')}")

def goodbye(a=None, b=None):  # type: ignore
    print("Exiting...")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write("Exiting...\n")


atexit.register(goodbye)  # type: ignore
signal.signal(signal.SIGTERM, goodbye)  # type: ignore
signal.signal(signal.SIGINT, goodbye)  # type: ignore
# signal.signal(signal.SIGKILL, goodbye)
# signal.signal(signal.SIGSTOP, goodbye)
signal.signal(signal.SIGHUP, goodbye)  # type: ignore


class MyBot(commands.Bot):
    def __init__(self, start_time: float, log: Callable[..., None], sus_on: bool, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs) 
        self.start_time = start_time
        self.log = log
        self.sus_on = sus_on

def log(text: str, print_text: Optional[bool] = None):
    tz = pytz.timezone("Asia/Manila")
    curr_time = datetime.now(tz)
    clean_time = curr_time.strftime("%m/%d/%Y %I:%M %p")
    final = f"{clean_time} - {text}\n"
    if not print_text:
        pass
    else:
        print(final)
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(final)

intents = disnake.Intents().all()
game = disnake.Activity(name="sus gaming | k.help", type=disnake.ActivityType.playing)
client = MyBot(
    start_time,
    log,
    False,
    command_prefix="k.",
    intents=intents,
    activity=game,
    default_install_types=disnake.ApplicationInstallTypes.all(),
    default_contexts=disnake.InteractionContextTypes.all(),
)
client.remove_command("help")


print(f"{(time.time() - start_time):.2f}s - Importing Kur0's modules...")

# Files we don't want to load as an extension
exclude_files = [
    "modules/paginator.py",
    "modules/template.py",
    "myfunctions/file_handler.py",
    "myfunctions/msg_link_grabber.py",
    "myfunctions/greenscreen.py",
    "myfunctions/subprocess_runner.py",
    "myfunctions/my_db.py",
    "myfunctions/async_wrapper.py",
]

os.chdir("/app")
print(f"Current in {Path.cwd()}")
for folder in ["myfunctions", "modules"]:
    for file in Path(folder).rglob("*.py"):
        if str(file) not in exclude_files:
            module = str(file.parent).replace("/", ".") + "." + file.stem
            client.load_extension(module)
            print(f"{(time.time() - start_time):.2f}s - {module} loaded")

print(f"{(time.time() - start_time):.2f}s - Done!")


@client.before_invoke
async def common(ctx: disnake.ext.commands.Context[Any]):
    text = (
        f"k.{ctx.invoked_with} | {ctx.author.name}#{ctx.author.discriminator}"
    )
    if ctx.guild:
        text += f'| "{ctx.guild.name}"'
    if not isinstance(ctx.channel, disnake.channel.DMChannel):
        text += f' - "{ctx.channel.name}"'
    log(str(text))


@client.command()
async def stream(ctx: disnake.ext.commands.Context[Any], link: str, noembed: Optional[Literal['noembed']] = None):
    idd = None
    if link.startswith("https://youtu.be"):
        idd = link.split("/")[-1].split("?")[0]
    elif link.startswith("https://www.youtube.com/"):
        idd = link.split("=")[1].split("&")[0]
    else:
        await ctx.send("Not a YT link!", delete_after=3.0)
        return
    
    if idd:
        print(idd)

    yt_key = os.getenv("YT_API_KEY")
    if yt_key is None:
        # TODO: make this DRY
        await ctx.send("This command does not work cuz the dev forgot to specify the YT_API_KEY")
        return

    params = {
        "part": "liveStreamingDetails,snippet",
        "key": yt_key,
        "id": idd,
    }

    url = "https://www.googleapis.com/youtube/v3/videos"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            r = await resp.json()
    isotime = r["items"][0]["liveStreamingDetails"]["scheduledStartTime"]
    title = r["items"][0]["snippet"]["title"]
    author = r["items"][0]["snippet"]["channelTitle"]
    try:
        thumbnail = r["items"][0]["snippet"]["thumbnails"]["maxres"]["url"]
    except Exception:
        try:
            thumbnail = r["items"][0]["snippet"]["thumbnails"]["standard"]["url"]
        except Exception:
            try:
                thumbnail = r["items"][0]["snippet"]["thumbnails"]["high"]["url"]
            except Exception:
                try:
                    thumbnail = r["items"][0]["snippet"]["thumbnails"]["medium"][
                        "url"
                    ]
                except Exception:
                    thumbnail = r["items"][0]["snippet"]["thumbnails"]["default"][
                        "url"
                    ]
    channelid = r["items"][0]["snippet"]["channelId"]
    parsed_t = dp.parse(isotime)
    t_in_seconds = parsed_t.timestamp()
    reltime = f"<t:{str(t_in_seconds).split('.', maxsplit=1)[0]}:R>"
    dttime = datetime.strptime(isotime, "%Y-%m-%dT%H:%M:%S%z")
    with open(
        "list.txt", "a", encoding="utf-8"
    ) as f:  # add stream url and time to list.txt
        f.write(f"{link} {parsed_t.strftime('%a %b %d %Y %H:%M:%S')}\n")

    # a_file = open("list.txt", "r")
    # a_file.close()
    # ^^why did i have this? i'm reading the file then doing nothing???

    params2: dict[str, Any] = {
        "part": "snippet",
        "key": yt_key,
        "id": channelid,
    }

    url = "https://www.googleapis.com/youtube/v3/channels"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params2) as resp:
            r2 = await resp.json()
    pfp = r2["items"][0]["snippet"]["thumbnails"]["default"]["url"]
    e = disnake.Embed(title=title, timestamp=dttime, description=reltime, url=link)
    e.set_author(
        name=author,
        icon_url=pfp,
        url=f"https://www.youtube.com/channel/{channelid}",
    )
    e.set_image(url=thumbnail)
    if noembed != "noembed":
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                "https://discord.com/api/webhooks/880667610323234877/oc31FGZ3SPfu7BCru4iOd2ULJA"
                "vyOdMi1SOaqNF58sHKBknFbdhK5zfqSZhxS4NZF9pU",
                session=session,
            )
            await webhook.send(embed=e)
    else:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                "https://discord.com/api/webhooks/880667610323234877/oc31FGZ3SPfu7BCru4iOd2ULJA"
                "vyOdMi1SOaqNF58sHKBknFbdhK5zfqSZhxS4NZF9pU",
                session=session,
            )
            await webhook.send(f"{reltime} **{author}** - [{title}](<{link}>)")
    await ctx.message.delete()
    try:
        client.loop.create_task(
            run_at(parsed_t.replace(tzinfo=None), open_url(link), link)
        )
    except Exception as e:
        await ctx.send(f"Error: {e}")


async def clear_list(url: str):
    with open("list.txt", "r", encoding="utf-8") as a_file:
        lines = a_file.read().splitlines()

    with open("list.txt", "w+", encoding="utf-8") as r:
        for i in lines:
            if i.split(" ")[0] != url:
                r.write(f"{i}\n")


async def open_url(url: str):
    print(f"{url} is starting!")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"open_url running {url}\n")

    avi_guild = client.get_guild(603147860225032192)
    while avi_guild is None:
        avi_guild = client.get_guild(603147860225032192)
        await asyncio.sleep(1)

    print("got guild!")
    sched_ch = avi_guild.get_channel(879702977898741770)
    print("got channel!")
    if sched_ch is None or not isinstance(sched_ch, disnake.TextChannel):
        print("channel not found")
        return
    messages = await sched_ch.history(limit=200).flatten()
    print("got messages")

    count = 0
    for msg in messages:
        if msg.reference is not None and not msg.is_system():
            if msg.reference.message_id is not None:
                msg_id = int(msg.reference.message_id)
                msgg = await sched_ch.fetch_message(msg_id)
                for i in msgg.embeds:
                    if i.url == url:
                        print(i.url)
                        count += 1
    print(f"{count} times")

    if count == 0:
        for msg in messages:
            for i in msg.embeds:
                if i.url == url:
                    print("found specific message")
                    print(msg.jump_url.split("/")[-1])
                    msg_id = int(msg.jump_url.split("/")[-1])
                    msg = await sched_ch.fetch_message(msg_id)
                    await msg.reply("<@&888794254837706804> Starting!")
    await clear_list(url)


@client.command()
@commands.is_owner()
async def sched(ctx: disnake.ext.commands.Context[Any], url: str):
    if guild := client.get_guild(603147860225032192):
        sched_ch: disnake.TextChannel = guild.get_channel(879702977898741770)  # type: ignore
    else:
        print("guild not found")
        return
    messages = await sched_ch.history(limit=200).flatten()

    count = 0
    for msg in messages:
        if msg.reference is not None and not msg.is_system():
            if msg.reference.message_id is not None:
                msg_id = int(msg.reference.message_id)
                msgg = await sched_ch.fetch_message(msg_id)
                for i in msgg.embeds:
                    if i.url == url:
                        print(i.url)
                        count += 1
    print(f"{count} times")


@client.command()
async def tasks(ctx: disnake.ext.commands.Context[Any]):
    client.loop.set_debug(True)


@client.command()
async def ping(ctx: disnake.ext.commands.Context[Any]):
    start_time = time.time()
    msg = await ctx.send(f"My ping is {round (client.latency * 1000)}ms")
    send_time = (time.time() - start_time) * 1000
    await msg.edit(
        content=f"{msg.content} but it took {send_time:.2f}ms to send this message"
    )


async def wait_until(dt: datetime):
    # sleep until the specified datetime
    now = datetime.now()
    await asyncio.sleep((dt - now).total_seconds())


async def run_at(dt: datetime, coro: Coroutine[Any, Any, None], url: str):
    now = datetime.now()
    nowstr = now.strftime("%m/%d/%Y %H:%M:%S")
    print(f"{url} is scheduled!")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{url} - scheduled at {nowstr}\n")
    await wait_until(dt)
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{url} starting!\n")
    return await coro


def precheck():

    if not os.path.isfile("list.txt"):
        with open(
            "list.txt", "w", encoding="utf-8"
        ) as _:  # creates txt if doesn't exist
            pass

    with open("list.txt", "r", encoding="utf-8") as a_file:  # reads the txt
        lines = a_file.read().splitlines()

    with open("list.txt", "w+", encoding="utf-8") as r:
        for i in lines:
            later = datetime.strptime(i.split(" ", 1)[1], "%a %b %d %Y %H:%M:%S")
            now = datetime.now()

            if later > now:
                r.write(i + "\n")
            url = i.split(" ")[0]

            if later > now + timedelta(days=6):
                print("more than 1 week")
            else:
                client.loop.create_task(run_at(later, open_url(url), url))


tcheck = threading.Thread(target=precheck)
tcheck.start()
print(f"{(time.time() - start_time):.2f}s - schedules checked!")
keep_alive()

proc_id = os.getpid()
print(f"{(time.time() - start_time):.2f}s - Process ID: {proc_id}")
log(f"Process ID: {proc_id}", False)
# check(start_time, proc_id)  # Old code from replit days
loop = client.loop
try:
    print(f"{(time.time() - start_time):.2f}s - Connecting to bot...")
    if token := os.getenv("TOKEN"):
        loop.run_until_complete(client.start(token))
    else:
        print("You have no TOKEN in your .env file")
except KeyboardInterrupt:
    loop.run_until_complete(client.close())
    # cancel all tasks lingering
finally:
    loop.close()

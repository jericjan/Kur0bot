import time

start_time = time.time()

import disnake

print(f"Running Disnake {disnake.__version__}")

from disnake.ext import commands
import os
from keep_alive import keep_alive
import asyncio
import aiohttp
from datetime import datetime, timedelta
import pytz
import requests
import threading
import atexit
import signal
import importlib

from dotenv import load_dotenv

load_dotenv()


def goodbye(a=None, b=None):
    print("Exiting...")
    f = open("log.txt", "a")
    f.write("Exiting...\n")
    f.close()


atexit.register(goodbye)
signal.signal(signal.SIGTERM, goodbye)
signal.signal(signal.SIGINT, goodbye)
# signal.signal(signal.SIGKILL, goodbye)
# signal.signal(signal.SIGSTOP, goodbye)
signal.signal(signal.SIGHUP, goodbye)

headers = {"Authorization": f"Bot {os.getenv('TOKEN')}"}
r = requests.get(
    url="https://discord.com/api/v9/channels/809247468084133898", headers=headers
)
if r.status_code == 429:
    print(f"{(time.time() - start_time):.2f}s - Rate limited again lmao")
else:
    print(f"{(time.time() - start_time):.2f}s - Not rate limited. ({r.status_code})")


intents = disnake.Intents().all()
game = disnake.Activity(name="sus gaming | k.help", type=disnake.ActivityType.playing)
client = commands.Bot(command_prefix="k.", intents=intents, activity=game)
client.remove_command("help")


async def log(text, printText=None):
    tz = pytz.timezone("Asia/Manila")
    curr_time = datetime.now(tz)
    clean_time = curr_time.strftime("%m/%d/%Y %I:%M %p")
    final = f"{clean_time} - {text}\n"
    if printText == False:
        pass
    else:
        print(final)
    f = open("log.txt", "a")
    f.write(final)
    f.close()


import modules.events


client.sus_on = False


print(f"{(time.time() - start_time):.2f}s - Importing Kur0's modules...")
client.add_cog(modules.events.Events(client, start_time, log))
client.load_extension("modules.vc")
client.load_extension("modules.copypasta")
client.load_extension("modules.help")
client.load_extension("modules.ascii")
client.load_extension("modules.reactions")
client.load_extension("modules.others.clip")
client.load_extension("modules.others.download")
client.load_extension("modules.others.emote_sticker")
client.load_extension("modules.others.badapple")
client.load_extension("modules.others.pet")
client.load_extension("modules.others.sauce")
client.load_extension("modules.others.144p")
client.load_extension("modules.others.when")
client.load_extension("modules.others.checkcomment")
client.load_extension("modules.others.coinflip")
client.load_extension("modules.others.superchat")
client.load_extension("modules.others.gif")
client.load_extension("modules.others.resize")
client.load_extension("modules.others.deepl")
client.load_extension("modules.others.karaoke")
client.load_extension("modules.others.hall_of_shame")
client.load_extension("modules.others.vergil")
client.load_extension("modules.pacifam_only")
client.load_extension("modules.kur0_only")
client.load_extension("modules.sus")
client.load_extension("modules.tasks")

print(f"{(time.time() - start_time):.2f}s - Done!")


@client.before_invoke
async def common(ctx):
    text = f'k.{ctx.invoked_with} | {ctx.author.name}#{ctx.author.discriminator} | "{ctx.guild.name}" - "{ctx.channel.name}"'
    await log(str(text))


@client.command(aliases=["refresh"])
@commands.is_owner()
async def reload(ctx, name):
    if name == "events":
        try:
            client.get_cog("Events").cog_unload()
            client.remove_cog("Events")
        except:
            print("epic failure")
        importlib.reload(modules.events)
        client.add_cog(modules.events.Events(client, start_time, log))
    else:
        client.reload_extension(name)
    await ctx.send(f"{name} reloaded!")


@client.command()
@commands.is_owner()
async def load(ctx, name):
    client.load_extension(name)
    await ctx.send(f"{name} loaded!")


@client.command()
@commands.is_owner()
async def unload(ctx, name):
    client.unload_extension(name)
    await ctx.send(f"{name} unloaded!")


from disnake import Webhook
import dateutil.parser as dp


@client.command()
async def stream(ctx, link, noembed=None):
    if link.startswith("https://youtu.be"):
        idd = link.split("/")[-1].split("?")[0]
        wrong = False
    elif link.startswith("https://www.youtube.com/"):
        idd = link.split("=")[1].split("&")[0]
        wrong = False
    else:
        await ctx.send("Not a YT link!", delete_after=3.0)
        wrong = True

    print(idd)
    if wrong != True:
        params = {
            "part": "liveStreamingDetails,snippet",
            "key": os.getenv("YT_API_KEY"),
            "id": idd,
        }

        url = "https://www.googleapis.com/youtube/v3/videos"
        r = requests.get(url, headers=None, params=params).json()
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
        reltime = f"<t:{str(t_in_seconds).split('.')[0]}:R>"
        dttime = datetime.strptime(isotime, "%Y-%m-%dT%H:%M:%S%z")
        f = open("list.txt", "a")  # add stream url and time to list.txt
        f.write(f"{link} {parsed_t.strftime('%a %b %d %Y %H:%M:%S')}\n")
        f.close()
        a_file = open("list.txt", "r")  # reads list.txt
        a_file.close()

        params2 = {
            "part": "snippet",
            "key": os.getenv("YT_API_KEY"),
            "id": channelid,
        }

        url = "https://www.googleapis.com/youtube/v3/channels"
        r2 = requests.get(url, headers=None, params=params2).json()
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
                    "https://discord.com/api/webhooks/880667610323234877/oc31FGZ3SPfu7BCru4iOd2ULJAvyOdMi1SOaqNF58sHKBknFbdhK5zfqSZhxS4NZF9pU",
                    session=session,
                )
                await webhook.send(embed=e)
        else:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(
                    "https://discord.com/api/webhooks/880667610323234877/oc31FGZ3SPfu7BCru4iOd2ULJAvyOdMi1SOaqNF58sHKBknFbdhK5zfqSZhxS4NZF9pU",
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


async def clear_list(url):
    a_file = open("list.txt", "r")
    lines = a_file.read().splitlines()
    a_file.close()
    with open("list.txt", "w+") as r:
        for i in lines:
            if i.split(" ")[0] != url:
                r.write(f"{i}\n")


async def open_url(url):
    print(f"{url} is starting!")
    f = open("log.txt", "a")
    f.write(f"open_url running {url}\n")
    f.close()

    avi_guild = client.get_guild(603147860225032192)
    while avi_guild == None:
        avi_guild = client.get_guild(603147860225032192)
        await asyncio.sleep(1)
    else:
        print("got guild!")
        sched_ch = avi_guild.get_channel(879702977898741770)
        print("got channel!")
        messages = await sched_ch.history(limit=200).flatten()
        print("got messages")

    count = 0
    for msg in messages:
        if msg.reference is not None and not msg.is_system():

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
async def sched(ctx, url):
    sched_ch = client.get_guild(603147860225032192).get_channel(879702977898741770)
    messages = await sched_ch.history(limit=200).flatten()

    count = 0
    for msg in messages:
        if msg.reference is not None and not msg.is_system():

            msg_id = int(msg.reference.message_id)
            msgg = await sched_ch.fetch_message(msg_id)
            for i in msgg.embeds:
                if i.url == url:
                    print(i.url)
                    count += 1
    print(f"{count} times")


@client.command()
async def tasks(ctx):
    client.loop.set_debug(True)


@client.command()
async def ping(ctx):
    await ctx.send(f"My ping is {round (client.latency * 1000)}ms!")


@client.command()
async def rolecheck(ctx):
    avi_guild = client.get_guild(603147860225032192)
    while avi_guild == None:
        pass
    else:
        admin = disnake.utils.get(avi_guild.roles, name="Admin")
        moderator = disnake.utils.get(avi_guild.roles, name="Moderator")
        avilon = disnake.utils.get(avi_guild.roles, name="Aweelom")
    roles = [admin, moderator, avilon]
    if (
        any(role in roles for role in ctx.author.roles)
        or ctx.author.id == 216830153441935360
    ):
        await ctx.send("You match the roles!")
    else:
        await ctx.send("Only Avi/Admins/Mods can use this command")


async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.now()
    await asyncio.sleep((dt - now).total_seconds())


async def run_at(dt, coro, url):
    now = datetime.now()
    nowstr = now.strftime("%m/%d/%Y %H:%M:%S")
    print(f"{url} is scheduled!")
    f = open("log.txt", "a")
    f.write(f"{url} - scheduled at {nowstr}\n")
    f.close()
    await wait_until(dt)
    f = open("log.txt", "a")
    f.write(f"{url} starting!\n")
    f.close()
    return await coro


def precheck():

    if not os.path.isfile("list.txt"):
        file = open("list.txt", "w")  # creates txt if doesn't exist
        file.close()
    a_file = open("list.txt", "r")  # reads the txt
    lines = a_file.read().splitlines()
    a_file.close()
    with open("list.txt", "w+") as r:
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
isDiscordrunning = False

from running_check import check

proc_id = os.getpid()
print(f"{(time.time() - start_time):.2f}s - Process ID: {proc_id}")
asyncio.run(log(f"Process ID: {proc_id}", False))
check(start_time, proc_id)
loop = client.loop
while isDiscordrunning is False:
    try:
        print(f"{(time.time() - start_time):.2f}s - Connecting to bot...")
        loop.run_until_complete(client.start(os.getenv("TOKEN")))
        print("Setting isDiscordrunning to True")
        isDiscordrunning = True
    except KeyboardInterrupt:
        loop.run_until_complete(client.close())
        # cancel all tasks lingering
    except disnake.HTTPException as e:
        print("nope. not working")

        r = requests.head(url="https://discord.com/api/v1")
        print(f"{type(e).__name__}: {r.status_code}")
        if r.status_code == 429:
            print("Rate limited again lmao")
        try:
            minutes = round(int(r.headers["Retry-After"]) / 60)
            print(f"{minutes} minutes left")
            print("Trying again in 5 seconds")
            time.sleep(5)
            os.system("busybox reboot")
        except:
            print("No rate limit")
            print("Trying again in 5 seconds")
            time.sleep(5)
    except:
        asyncio.run(log("Something went wrong. Exiting..."))
    finally:
        loop.close()

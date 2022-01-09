import time

start_time = time.time()

import discord

print(f"Running Pycord {discord.__version__}")
from discord.ext import commands
import os

import json
from keep_alive import keep_alive
import random
import asyncio
import aiohttp
import subprocess
from gtts import gTTS
from datetime import datetime, timedelta
import pytz


import requests
import re
import threading
import io
import atexit
import signal


def goodbye():
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


# client = discord.Client()
intents = discord.Intents().default()
intents.presences = True
intents.members = True

# global client
game = discord.Activity(name="sus gaming | k.help", type=discord.ActivityType.playing)
client = commands.Bot(command_prefix="k.", intents=intents, activity=game)

client.remove_command("help")
sus_words = [
    "amongus",
    "аmongus",
    "among us",
    "аmong us",
    "sus",
    "sussy",
    "suspicious",
    "amogus",
    "аmogus",
    "imposter",
    "impostor",
]

sus_replies = [
    "that's pretty sus, bro",
    "sus",
    "you sussy baka",
    "AMOGUS!!! SO SUS!!",
    "sus gaming",
    "sussy bussy baka!",
    "amonug impostoer??",
    "is that an among us reference?",
    "ඞ",
]

hidden_commands = [
    "addoffline",
    "makeembed",
    "sched",
    "tasks",
    "removeoffline",
    "idclip",
    "id",
    "stream",
    "editembed",
    "sticker",
    "rolecheck",
    "viewoffline",
    "repost",
    "fastclip3",
    "fastclip2",
    "speak",
    "speak2",
]

pass_words = ["password", "pass word"]

sugma_replies = ["sugma balls!! hahahaaaaa", "sugma.... sugma balls!!!!!!!"]

sugoma_replies = ["sugoma balls!! hahahaaaaa", "sugoma.... sugoma balls!!!!!!!"]

custom_words = ["amgus", "amogus", "sushi", "pog"]


@client.event
async def on_ready():

    print(
        f"\033[92m{(time.time() - start_time):.2f}s - We have logged in as {client.user}\033[0m"
    )
    await log("Bot started", False)
    #  await client.change_presence(activity=discord.Game(name="sus gaming | k.help"))
    avi_guild = client.get_guild(603147860225032192)
    while avi_guild == None:
        avi_guild = client.get_guild(603147860225032192)
    else:
        print(avi_guild)
        avibot = avi_guild.get_member(855897776125640704)
        while avibot == None:
            avibot = avi_guild.get_member(855897776125640704)
        else:
            if avibot.status is discord.Status.offline:
                print("avibot ded")
                await log("avi bot ded", False)
                # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
                # msg_id = 887707057808085042
                # msg = await channel.fetch_message(msg_id)
                vc = client.get_guild(603147860225032192).get_channel(
                    887717074191937667
                )
                # await msg.edit(content="avi bot dead temporarily. password no work. so tell them that as well.")
                # staffch = client.get_guild(603147860225032192).get_channel(812666568613167125)
                await vc.edit(name="AviBot: dead")
            # await staffch.send('<@97122523086340096> bot ded')
            if avibot.status is discord.Status.online:
                print("avi bot bac")
                await log("avi bot bac", False)
                # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
                # msg_id = 887707057808085042
                # msg = await channel.fetch_message(msg_id)
                vc = client.get_guild(603147860225032192).get_channel(
                    887717074191937667
                )
                # await msg.edit(content="AviBot is online. (ignore this)")
                await vc.edit(name="AviBot: alive")


client.sus_on = False


@client.event
async def on_member_update(before, after):
    if (
        before.status is discord.Status.online
        and after.status is discord.Status.offline
        and after.guild == client.get_guild(603147860225032192)
    ):
        if after.id == 855897776125640704:
            print(after.id)
            print("avi bot ded")
            await log("avi bot ded", False)
            # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
            #  msg_id = 887707057808085042
            # msg = await channel.fetch_message(msg_id)
            vc = client.get_guild(603147860225032192).get_channel(887717074191937667)
            # await msg.edit(content="avi bot dead temporarily. password no work. so tell them that as well.")
            # staffch = client.get_guild(603147860225032192).get_channel(812666568613167125)
            await vc.edit(name="AviBot: dead")
            # await staffch.send('<@97122523086340096> bot ded')
    elif (
        before.status is discord.Status.offline
        and after.status is discord.Status.online
    ):
        if after.id == 855897776125640704:
            print(after.id)
            print("avi bot bac")
            await log("avi bot bac", False)
            # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
            # msg_id = 887707057808085042
            # msg = await channel.fetch_message(msg_id)
            vc = client.get_guild(603147860225032192).get_channel(887717074191937667)
            # await msg.edit(content="AviBot is online. (ignore this)")
            await vc.edit(name="AviBot: alive")


@client.listen("on_message")
async def sus(message):
    if message.author == client.user:
        return
    msg = message.content.lower()
    # if message.channel.id == 836222286432043018: #verification
    #   if message.content.startswith('+verify'):
    #    if not message.content.startswith('+verify poggus'):
    #      if any(word in msg for word in pass_words):
    #       await message.delete()
    #       nono = await message.channel.send('Booba! The password is not password!')
    #       await asyncio.sleep(3)
    #       await nono.delete()
    #      else:
    #       await message.delete()
    #       nono = await message.channel.send#('https://media.tenor.com/images/e2791267b28c9e57b6966bacb65578e9/tenor.gif')
    #       await asyncio.sleep(2)
    #       await nono.delete()
    #    else:
    #     await message.delete()
    #   else:
    #     await asyncio.sleep(1)
    #     print(message.channel.id)
    #      await message.delete()
    if message.channel.id == 850380119646142504:  # sus-town
        if any(word in msg for word in sus_words):
            for x in range(3):
                await message.channel.send(random.choice(sus_replies))
    else:
        if not any(word in msg for word in custom_words):
            if any(word in msg for word in sus_words):
                if client.sus_on == False:
                    await message.channel.send(
                        random.choice(sus_replies), delete_after=3.0
                    )
                    await log("sussy reply", False)
                if client.sus_on:
                    await message.channel.send(random.choice(sus_replies))
                    await log("sussy reply", False)
        else:
            if "amgus" in msg:
                await message.channel.send(
                    random.choice(sugma_replies), delete_after=3.0
                )
                await log("sussy reply", False)
            if "amogus" in msg:
                await message.channel.send(
                    random.choice(sugoma_replies), delete_after=3.0
                )
                await log("sussy reply", False)
            if "sushi" in msg:
                await message.channel.send(
                    "remove the hi from sushi. what do you get? <:sus:850628234746920971>",
                    delete_after=3.0,
                )
                await log("sussy reply", False)
            if "pog" in msg:
                await message.channel.send("poggusus", delete_after=3.0)
                await log("sussy reply", False)


@client.listen("on_message")
async def twitter_video_link_giver(message):
    if message.author == client.user:
        return

    msg = message.content.lower()
    if "twitter.com" in msg:
        threads = []
        links = re.findall("http.*twitter.com/.*/status/\d*", msg)
        print([x for x in links])
        for i in links:
            print("twitter link!")
            await log("twitter link!", False)
            args = ["youtube-dl", "-j", i]
            print(args)
            proc = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            stdout_value = proc.stdout.read() + proc.stderr.read()
            # print(stdout_value.decode("utf-8"))
            json_list = json.loads(stdout_value)
            ext = json_list["ext"]
            webpageurl = json_list["webpage_url"]
            print(ext)
            if ext == "mp4" and "twitter.com" in webpageurl:
                m1 = await message.channel.send(
                    "Beep boop! That is a twitter video!\nImma give direct video link..."
                )
                await log("twitter video!", False)

                msg = await message.channel.send(json_list["url"])
                await asyncio.sleep(3)
                if not msg.embeds:
                    await m1.edit(content="No embeds. Trying to manually upload...")
                    r = requests.get(json_list["url"])
                    # print(r.content)
                    vid = io.BytesIO(r.content)
                    filename = json_list["url"].split("/")[-1].split("?")[0]
                    await message.channel.send(
                        file=discord.File(vid, filename=filename)
                    )
                await m1.delete()


@client.listen("on_message")
async def vc_tts(message):
    if message.author == client.user:
        return
    msg = message.content.lower()
    if msg.startswith("] "):
        voice_channel = message.author.voice.channel
        await log("] command used", True)
        tts = gTTS(msg)
        with open("sounds/tts.mp3", "wb") as f:
            tts.write_to_fp(f)
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice_channel != None:

            if voice == None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
            else:
                voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
    if msg.startswith("]au "):
        await log("]au command used", True)
        voice_channel = message.author.voice.channel

        tts = gTTS(msg[3:], lang="en", tld="com.au")
        with open("sounds/tts.mp3", "wb") as f:
            tts.write_to_fp(f)
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice_channel != None:

            if voice == None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
            else:
                voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
    if msg.startswith("]uk "):
        await log("]uk command used", True)
        voice_channel = message.author.voice.channel

        tts = gTTS(msg[3:], lang="en", tld="co.uk")
        with open("sounds/tts.mp3", "wb") as f:
            tts.write_to_fp(f)
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice_channel != None:

            if voice == None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
            else:
                voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
    if msg.startswith("]in "):
        await log("]in command used", True)
        voice_channel = message.author.voice.channel

        tts = gTTS(msg[3:], lang="en", tld="co.in")
        with open("sounds/tts.mp3", "wb") as f:
            tts.write_to_fp(f)
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice_channel != None:

            if voice == None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
            else:
                voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))


print(f"{(time.time() - start_time):.2f}s - Importing Kur0's modules...")
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
client.load_extension("modules.pacifam_only")
client.load_extension("modules.kur0_only")
print(f"{(time.time() - start_time):.2f}s - Done!")


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


@client.before_invoke
async def common(ctx):
    text = f"k.{ctx.invoked_with} command used"
    print = True
    await log(str(text))


@client.command()
async def bulk(ctx, number):
    print(ctx.channel.id)
    if ctx.channel.id == 850380119646142504:
        for x in range(int(number)):
            await ctx.send(random.choice(sus_replies))
    else:
        await ctx.send("Only usable in <#850380119646142504> <:sus:850628234746920971>")


@client.command()
async def on(ctx):
    client.sus_on = True
    await ctx.send("Permanent Sus enabled!")


@client.command()
async def off(ctx):
    client.sus_on = False
    await ctx.send("Permanent Sus disabled!")


@client.command()
async def speak(ctx, *, message):
    voice_channel = ctx.author.voice.channel

    tts = gTTS(message)
    with open("sounds/tts.mp3", "wb") as f:
        tts.write_to_fp(f)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_channel != None:

        if voice == None:
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
        else:
            voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))


@client.command()
async def speak2(ctx, *, message):
    voice_channel = ctx.author.voice.channel

    tts = gTTS(message, lang="en", tld="com.au")
    with open("sounds/tts.mp3", "wb") as f:
        tts.write_to_fp(f)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_channel != None:

        if voice == None:
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
        else:
            voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))


import difflib


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"Ayo this command is on cooldown.\nWait for {error.retry_after:.2f}s to try it again.",
            delete_after=3.0,
        )
        await ctx.message.delete()
        print(dir(error))
        print(f"error: {error}\nerror args: {error.args}")
    elif isinstance(error, commands.CommandNotFound):
        err = str(error).split('"')
        commandss = [c.name for c in client.commands if c.name not in hidden_commands]
        print(commandss)
        similar = difflib.get_close_matches(err[1], commandss)
        if similar:
            await ctx.send(
                f"bruh. there's no '{err[1]}' command.\ndid you mean:\n`{', '.join(similar)}`?"
            )
        else:
            await ctx.send(f"bruh. there's no '{err[1]}' command.")
    else:
        print(error)
        print(dir(error))
        await ctx.send(error)
    await log(error, False)
    raise error  # re-raise the error so all the errors will still show up in console


import dateutil.parser as dp


@client.command()
async def when(ctx, link):
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
            "part": "snippet",
            "key": os.getenv("YT_API_KEY"),
            "id": idd,
        }
        url = "https://www.googleapis.com/youtube/v3/videos"
        r = requests.get(url, headers=None, params=params).json()
        publish_time = r["items"][0]["snippet"]["publishedAt"]
        epoch_time = dp.parse(publish_time).timestamp()
        await ctx.send(f"<t:{epoch_time:.0f}:F>")


from discord import Webhook


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
        # resos = ['maxres','standard','high','medium','default']
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
        #  dsctime = f"<t:{str(t_in_seconds).split('.')[0]}:F>"
        reltime = f"<t:{str(t_in_seconds).split('.')[0]}:R>"
        dttime = datetime.strptime(isotime, "%Y-%m-%dT%H:%M:%S%z")
        #  dayofweek = parsed_t.weekday()

        f = open("list.txt", "a")  # add stream url and time to list.txt
        f.write(f"{link} {parsed_t.strftime('%a %b %d %Y %H:%M:%S')}\n")
        f.close()
        a_file = open("list.txt", "r")  # reads list.txt
        #   lines = a_file.read().splitlines()
        a_file.close()

        params2 = {
            "part": "snippet",
            "key": os.getenv("YT_API_KEY"),
            "id": channelid,
        }

        url = "https://www.googleapis.com/youtube/v3/channels"
        r2 = requests.get(url, headers=None, params=params2).json()
        pfp = r2["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        e = discord.Embed(title=title, timestamp=dttime, description=reltime, url=link)
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
        # print(msg)
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
                #  print(i.url)
                if i.url == url:
                    print("found specific message")
                    print(msg.jump_url.split("/")[-1])
                    msg_id = int(msg.jump_url.split("/")[-1])
                    msg = await sched_ch.fetch_message(msg_id)
                    await msg.reply("<@&888794254837706804> Starting!")
                    # await msg.reply('test')
    await clear_list(url)


@client.command()
async def sched(ctx, url):
    sched_ch = client.get_guild(603147860225032192).get_channel(879702977898741770)
    messages = await sched_ch.history(limit=200).flatten()
    # print(messages)
    count = 0
    for msg in messages:
        # print(msg)
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
    # tasks = client.loop.all_tasks()
    # for i in tasks:
    #   await ctx.send(i.get_coro())
    #   await ctx.send(i.get_name())
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
        admin = discord.utils.get(avi_guild.roles, name="Admin")
        moderator = discord.utils.get(avi_guild.roles, name="Moderator")
        avilon = discord.utils.get(avi_guild.roles, name="Aweelom")
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
    # print(lines)
    with open("list.txt", "w+") as r:
        for i in lines:
            later = datetime.strptime(i.split(" ", 1)[1], "%a %b %d %Y %H:%M:%S")
            now = datetime.now()

            if later > now:
                r.write(i + "\n")
            url = i.split(" ")[0]
            #  day = i.split(" ")[1]
            #  timee = i.split(" ")[5]
            if later > now + timedelta(days=6):
                print("more than 1 week")
            else:
                # loop = asyncio.new_event_loop()
                # asyncio.set_event_loop(loop)

                # loop.run_until_complete()
                # loop.close()
                client.loop.create_task(run_at(later, open_url(url), url))


tcheck = threading.Thread(target=precheck)
tcheck.start()
print(f"{(time.time() - start_time):.2f}s - schedules checked!")
keep_alive()
isDiscordrunning = False
# client.run(os.getenv("TOKEN"))

from running_check import check

proc_id = os.getpid()
print(f"{(time.time() - start_time):.2f}s - Process ID: {proc_id}")
check(start_time, proc_id)

while isDiscordrunning is False:
    try:
        print(f"{(time.time() - start_time):.2f}s - Connecting to bot...")

        client.run(os.getenv("TOKEN"))
        isDiscordrunning = True
    except Exception as e:
        print("nope. not working")

        r = requests.head(url="https://discord.com/api/v1")
        print(f"{type(e).__name__}: {r.status_code}")
        # print(e)
        if r.status_code == 429:
            print("Rate limited again lmao")
        try:
            minutes = round(int(r.headers["Retry-After"]) / 60)
            print(f"{minutes} minutes left")
            # print(f"Trying again in {(minutes*60)+1} seconds...")
            print("Trying again in 5 seconds")
            time.sleep(5)
            os.system("busybox reboot")
        except:
            print("No rate limit")
            print("Trying again in 5 seconds")
            time.sleep(5)


# if __name__ == '__main__':
# run app in debug mode on port 5000
# schedule.clear()

import discord

print("Running Pycord {0}".format(discord.__version__))
from discord.ext import commands, pages
from discord.ui import Button, View
import os
import json
from keep_alive import keep_alive
import random
import asyncio
import aiohttp
import subprocess
from gtts import gTTS
from datetime import datetime, timedelta, timezone
from shlex import quote
from shlex import join as shjoin
import schedule
import threading
import time
import io
import math
import re
import glob


# client = discord.Client()
intents = discord.Intents().default()
intents.presences = True
intents.members = True

global client
client = commands.Bot(command_prefix="k.", intents=intents)

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

pass_words = ["password", "pass word"]

sugma_replies = ["sugma balls!! hahahaaaaa", "sugma.... sugma balls!!!!!!!"]

sugoma_replies = ["sugoma balls!! hahahaaaaa", "sugoma.... sugoma balls!!!!!!!"]

custom_words = ["amgus", "amogus", "sushi", "pog"]

may_sounds = ["sounds/totsugeki_7UWR0L4.mp3", "sounds/totsugeki-may-2.mp3"]


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Game(name="sus gaming | k.help"))
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
                if client.sus_on:
                    await message.channel.send(random.choice(sus_replies))
        else:
            if "amgus" in msg:
                await message.channel.send(
                    random.choice(sugma_replies), delete_after=3.0
                )
            if "amogus" in msg:
                await message.channel.send(
                    random.choice(sugoma_replies), delete_after=3.0
                )
            if "sushi" in msg:
                await message.channel.send(
                    "remove the hi from sushi. what do you get? <:sus:850628234746920971>",
                    delete_after=3.0,
                )
            if "pog" in msg:
                await message.channel.send("poggusus", delete_after=3.0)


@client.listen("on_message")
async def sus2(message):
    if message.author == client.user:
        return
    msg = message.content.lower()
    if "twitter.com" in msg:
        print("twitter link!")
        args = ["youtube-dl", "-j", msg]
        print(args)
        proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
        )
        stdout_value = proc.stdout.read() + proc.stderr.read()
        json_list = json.loads(stdout_value)
        ext = json_list["ext"]
        webpageurl = json_list["webpage_url"]
        print(ext)
        if ext == "mp4" and "twitter.com" in webpageurl:
            m1 = await message.channel.send("Beep boop! That is a twitter video!")
            await asyncio.sleep(0.1)
            m2 = await message.channel.send("Imma give direct video link...")
            args = ["youtube-dl", "--get-url", msg]
            print(args)
            proc = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            stdout_value = proc.stdout.read() + proc.stderr.read()
            await message.channel.send(stdout_value.decode("utf-8"))
            await m1.delete()
            await m2.delete()
            # json_list = json.loads(mixed_Slist[0])
            # title = json_list['ext']
            # print(title)


@client.listen("on_message")
async def sus3(message):
    if message.author == client.user:
        return
    msg = message.content.lower()
    if msg.startswith("] "):
        voice_channel = message.author.voice.channel
        channel = None
        tts = gTTS(msg)
        with open("sounds/tts.mp3", "wb") as f:
            tts.write_to_fp(f)
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice_channel != None:
            channel = voice_channel.name
            if voice == None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
            else:
                voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
    if msg.startswith("] "):
        voice_channel = message.author.voice.channel
        channel = None
        tts = gTTS(msg[3:], lang="en", tld="com.au")
        with open("sounds/tts.mp3", "wb") as f:
            tts.write_to_fp(f)
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice_channel != None:
            channel = voice_channel.name
            if voice == None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
            else:
                voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
    if msg.startswith("]uk "):
        voice_channel = message.author.voice.channel
        channel = None
        tts = gTTS(msg[3:], lang="en", tld="co.uk")
        with open("sounds/tts.mp3", "wb") as f:
            tts.write_to_fp(f)
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice_channel != None:
            channel = voice_channel.name
            if voice == None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
            else:
                voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
    if msg.startswith("]in "):
        voice_channel = message.author.voice.channel
        channel = None
        tts = gTTS(msg[3:], lang="en", tld="co.in")
        with open("sounds/tts.mp3", "wb") as f:
            tts.write_to_fp(f)
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice_channel != None:
            channel = voice_channel.name
            if voice == None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
            else:
                voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))


client.load_extension("vc")
client.load_extension("copypasta")


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


@client.command(aliases=["e"])
async def emote(ctx, *message):

    emoji_list = []
    webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
    print(message)
    for i in range(len(message)):
        emoji = discord.utils.get(client.emojis, name=message[i])
        emojistr = str(emoji)
        emoji_list.append(emojistr)
    if emoji == None:
        oof = await ctx.send(f"Invalid emoji name.")
        await asyncio.sleep(3)
        await oof.delete()
        await ctx.message.delete()
        return
    await webhook.send(
        "".join(emoji_list),
        username=ctx.message.author.name,
        avatar_url=ctx.message.author.avatar_url,
    )

    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()
    await ctx.message.delete()


@client.command(aliases=["s"])
async def sticker(ctx, msgID: int):
    msg = await ctx.fetch_message(msgID)
    await ctx.send(msg.stickers)


def paginate(lines, chars=2000):
    size = 0
    message = []
    for line in lines:
        if len(line) + size > chars:
            yield message
            message = []
            size = 0
        message.append(line)
        size += len(line)
    yield message


@client.command(aliases=["ge"])
async def getemotes(ctx):
    server = ctx.message.guild
    emojis = [str(x) for x in server.emojis]
    message = ""
    embed = discord.Embed()
    for guild in client.guilds:
        if guild.id != 856415893305950228 and guild.id != 856412098459860993:
            print(guild.id)
            # await ctx.send(guild.name)
            emojis = [str(x) for x in guild.emojis]
            for index, message in enumerate(paginate(emojis)):
                if index == 0:
                    embed.title = guild.name
                else:
                    embed.title = ""
                embed.description = "".join(message)
                await ctx.send(embed=embed)
        else:
            print("bad apple server")


@client.command()
async def id(ctx, title, *, message=None):
    if "cdn.discordapp.com" in message:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://cdn.discordapp.com/emojis/"
                + message.split("/")[4].split(".")[0]
            ) as response:
                img = await response.read()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://cdn.discordapp.com/emojis/" + message
            ) as response:
                img = await response.read()
    # now img contains the bytes of the image, let's create the emoji
    await ctx.guild.create_custom_emoji(name=title, image=img)
    await ctx.send("Emoji uploaded!")


@client.command()
async def fmega(ctx):
    webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
    await webhook.send(
        "https://thumbs.gfycat.com/BleakAdorableLangur-size_restricted.gif",
        username=ctx.message.author.name,
        avatar_url=ctx.message.author.avatar_url,
    )
    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()
    await ctx.message.delete()


@client.command()
async def kotowaru(ctx):
    webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
    await webhook.send(
        "https://cdn.discordapp.com/attachments/812666547520667669/852875900731392010/tenor.gif",
        username=ctx.message.author.name,
        avatar_url=ctx.message.author.avatar_url,
    )
    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()
    await ctx.message.delete()


@client.command()
async def ascend(ctx):
    webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
    await webhook.send(
        "https://tenor.com/view/bruno-bucciarati-jojo-jjba-death-gif-14981833",
        username=ctx.message.author.name,
        avatar_url=ctx.message.author.avatar_url,
    )
    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()
    await ctx.message.delete()


@client.command()
async def jizz(ctx):
    webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
    await webhook.send(
        "https://pbs.twimg.com/media/E3oLqt8VUAQpRiL?format=jpg&name=900x900",
        username=ctx.message.author.name,
        avatar_url=ctx.message.author.avatar_url,
    )
    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()
    await ctx.message.delete()


@client.command()
async def leave(ctx):
    if ctx.voice_client:  # If the bot is in a voice channel
        await ctx.guild.voice_client.disconnect()  # Leave the channel
        await ctx.send("Sus bot has left the call.", delete_after=3.0)
        await asyncio.sleep(0.3)
        await ctx.message.delete()
    else:  # But if it isn't
        await ctx.send(
            "I'm not in a voice channel, use the join command to make me join",
            delete_after=3.0,
        )
    await ctx.message.delete()


@client.command()
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Sus bot has been stopped.", delete_after=3.0)
    else:
        await ctx.send(
            "The bot is not playing anything at the moment.", delete_after=3.0
        )
    await ctx.message.delete()


@client.command()
async def stoploop(ctx):
    await ctx.guild.voice_client.disconnect()
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    await ctx.send("The loop has been stopped.", delete_after=3.0)
    await ctx.message.delete()


@client.command()
async def speak(ctx, *, message):
    voice_channel = ctx.author.voice.channel
    channel = None
    tts = gTTS(message)
    with open("sounds/tts.mp3", "wb") as f:
        tts.write_to_fp(f)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_channel != None:
        channel = voice_channel.name
        if voice == None:
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
        else:
            voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))


@client.command()
async def speak2(ctx, *, message):
    voice_channel = ctx.author.voice.channel
    channel = None
    tts = gTTS(message, lang="en", tld="com.au")
    with open("sounds/tts.mp3", "wb") as f:
        tts.write_to_fp(f)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_channel != None:
        channel = voice_channel.name
        if voice == None:
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
        else:
            voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))


@client.command()
async def join(ctx):
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    await ctx.send("Sus bot has joined the call.", delete_after=3.0)
    await ctx.message.delete()


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            "Ayo this command is on cooldown.\nWait for %.2fs to try it again."
            % error.retry_after,
            delete_after=3.0,
        )
        await ctx.message.delete()
    raise error  # re-raise the error so all the errors will still show up in console


@client.command()
@commands.cooldown(1.0, 60.0, commands.BucketType.guild)
async def badapple(ctx, *, message=None):

    webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
    for i in range(80):
        globals()[f"b{i}"] = discord.utils.get(client.emojis, name="b" + str(i))
    await webhook.send(
        str(b0)
        + str(b1)
        + str(b2)
        + str(b3)
        + str(b4)
        + str(b5)
        + str(b6)
        + str(b7)
        + str(b8)
        + str(b9)
        + "\n"
        + str(b10)
        + str(b11)
        + str(b12)
        + str(b13)
        + str(b14)
        + str(b15)
        + str(b16)
        + str(b17)
        + str(b18)
        + str(b19),
        username=ctx.message.author.name,
        avatar_url=ctx.message.author.avatar_url,
    )
    await asyncio.sleep(0.5)
    await webhook.send(
        str(b20)
        + str(b21)
        + str(b22)
        + str(b23)
        + str(b24)
        + str(b25)
        + str(b26)
        + str(b27)
        + str(b28)
        + str(b29)
        + "\n"
        + str(b30)
        + str(b31)
        + str(b32)
        + str(b33)
        + str(b34)
        + str(b35)
        + str(b36)
        + str(b37)
        + str(b38)
        + str(b39),
        username=ctx.message.author.name,
        avatar_url=ctx.message.author.avatar_url,
    )
    await asyncio.sleep(0.5)
    await webhook.send(
        str(b40)
        + str(b41)
        + str(b42)
        + str(b43)
        + str(b44)
        + str(b45)
        + str(b46)
        + str(b47)
        + str(b48)
        + str(b49)
        + "\n"
        + str(b50)
        + str(b51)
        + str(b52)
        + str(b53)
        + str(b54)
        + str(b55)
        + str(b56)
        + str(b57)
        + str(b58)
        + str(b59),
        username=ctx.message.author.name,
        avatar_url=ctx.message.author.avatar_url,
    )
    await asyncio.sleep(0.5)
    await webhook.send(
        str(b60)
        + str(b61)
        + str(b62)
        + str(b63)
        + str(b64)
        + str(b65)
        + str(b66)
        + str(b67)
        + str(b68)
        + str(b69)
        + "\n"
        + str(b70)
        + str(b71)
        + str(b72)
        + str(b73)
        + str(b74)
        + str(b75)
        + str(b76)
        + str(b77)
        + str(b78)
        + str(b79),
        username=ctx.message.author.name,
        avatar_url=ctx.message.author.avatar_url,
    )

    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()
    await ctx.message.delete()


@client.command()
async def clip(ctx, link, start, end, filename):

    if (
        re.match("\d{2}:\d{2}:\d{2}", start) != None
        and re.match("\d{2}:\d{2}:\d{2}", end) != None
    ):
        print("good timestamps!")
    else:
        print("bad timestamps!")
        await ctx.send("Timestamps are wrong. Please provide it in HH:MM:SS")
        return

    if os.path.isfile(filename + ".mkv"):
        os.remove(filename + ".mkv")
    if os.path.isfile(filename + ".mp4"):
        os.remove(filename + ".mp4")
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
            filename + ".mkv",
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
            filename + ".mkv",
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
                    print(str(percentage) + "% complete...")
                    await message.edit(
                        content=str(round(percentage, 2)) + "% complete..."
                    )
        os.rename(filename + ".mkv", filename + ".mp4")
        await ctx.send(file=discord.File(filename + ".mp4"))
        # await ctx.send(ctx.message.author.mention)
        os.remove(filename + ".mp4")
        await message.delete()
    except ValueError:
        await message.edit(content="An error occured... Uh, try it again.")


@client.command()
async def fastclip3(ctx, link, start, end, filename):
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
            filename + ".mp4",
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
            filename + ".mp4",
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
        await ctx.send(file=discord.File(filename + ".mp4"))
    except Exception:
        await message.edit(content="I failed.")
    await ctx.send(ctx.message.author.mention)
    os.remove(filename + ".mp4")
    await message.delete()


@client.command()
async def fastclip2(ctx, link, start, end, filename):
    message = await ctx.send("Fetching url...")
    coms = ["yt-dlp", "-g", "-f", "best", "--youtube-skip-dash-manifest", link]
    print(shjoin(coms))
    startsplit = start.split(":")
    shour = startsplit[0]
    sminute = startsplit[1]
    ssecond = startsplit[2]
    result1 = timedelta(hours=int(shour), minutes=int(sminute), seconds=int(ssecond))
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
        filename + ".mp4",
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
        await ctx.send(file=discord.File(filename + ".mp4"))
    except Exception:
        await message.edit(content="I failed.")
    await ctx.send(ctx.message.author.mention)
    os.remove(filename + ".mp4")
    await message.delete()


@client.command()
async def fastclip(ctx, link, start, end, filename):

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
            - timedelta(hours=int(shour), minutes=int(sminute), seconds=int(ssecond))
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
            filename + "_temp0.mp4",
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
            filename + "_temp0.mp4",
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
        filename + "_temp0.mp4",
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
        filename + "_temp0.mp4",
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        filename + "_temp.mp4",
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
                    filename + "_temp0.mp4",
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
            print("after " + str(prev_keyframe))
            print("before " + str(next_keyframe))
            if next_keyframe == None:
                print("no next keyframe!")
                keyframe = prev_keyframe
            else:
                keyframe = (prev_keyframe + next_keyframe) / 2
        print("keyframe is " + "{:.6f}".format(keyframe))
        if round_down(seconds - prev_keyframe, round_number) == 0:
            await ctx.send(
                "<:callipog:850365252637032479> Poggers. No need to clip to nearest keyframe."
            )
        else:
            await ctx.send(
                "Clipping "
                + str(round_down(seconds - prev_keyframe, round_number))
                + " seconds earlier to nearest keyframe..."
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
        print("keyframe is " + str(keyframe))
        if round_down(30 - prev_keyframe, round_number) == 0:
            await ctx.send(
                "<:callipog:850365252637032479> Poggers. No need to clip to nearest keyframe."
            )
        else:
            await ctx.send(
                "Clipping "
                + str(round_down(30 - prev_keyframe, round_number))
                + " seconds earlier to nearest keyframe..."
            )

    coms = [
        "ffmpeg",
        "-noaccurate_seek",
        "-ss",
        "{:.6f}".format(keyframe),
        "-i",
        filename + "_temp.mp4",
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        "-avoid_negative_ts",
        "make_zero",
        filename + ".mp4",
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
        filename + ".mp4",
    ]
    process = await asyncio.create_subprocess_exec(
        *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    print(stderr)
    print("final keyframes:")
    print(stdout.decode("utf-8"))

    try:

        await ctx.send(file=discord.File(filename + ".mp4"))
    except Exception:
        await message.edit(content="I failed.")
    await ctx.send(ctx.message.author.mention)
    os.remove(filename + ".mp4")
    os.remove(filename + "_temp0.mp4")
    os.remove(filename + "_temp.mp4")
    await message.delete()


@client.command()
async def idclip(ctx, link, start, end, filename, id, id2):

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
    coms = ["yt-dlp", "-g", "-f", id + "+" + id2, link]
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
            - timedelta(hours=int(shour), minutes=int(sminute), seconds=int(ssecond))
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
            filename + "_temp.mp4",
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
            filename + "_temp.mp4",
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
        filename + "_temp.mp4",
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
            print("after " + str(prev_keyframe))
            print("before " + str(next_keyframe))
            if next_keyframe == None:
                print("no next keyframe!")
                keyframe = prev_keyframe
            else:
                keyframe = (prev_keyframe + next_keyframe) / 2
        print("keyframe is " + "{:.6f}".format(keyframe))
        await ctx.send(
            "Clipping "
            + str(round_down(seconds - prev_keyframe, round_number))
            + " seconds earlier to nearest keyframe..."
        )

    else:
        if round_frames == True:
            keyframe = round_down(max_le(timelist_float, 30), round_number)
        else:
            prev_keyframe = max_le(timelist_float, 30)
            next_keyframe = min_gt(timelist_float, 30)
            keyframe = (prev_keyframe + next_keyframe) / 2
        print("keyframe is " + str(keyframe))
        await ctx.send(
            "Clipping "
            + str(round_down(30 - prev_keyframe, round_number))
            + " seconds earlier to nearest keyframe..."
        )

    coms = [
        "ffmpeg",
        "-noaccurate_seek",
        "-ss",
        "{:.6f}".format(keyframe),
        "-i",
        filename + "_temp.mp4",
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        "-avoid_negative_ts",
        "make_zero",
        filename + ".mp4",
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
        filename + ".mp4",
    ]
    process = await asyncio.create_subprocess_exec(
        *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    print(stderr)
    print("final keyframes:")
    print(stdout.decode("utf-8"))

    try:

        await ctx.send(file=discord.File(filename + ".mp4"))
    except Exception as e:
        await message.edit(content="I failed.")
        await ctx.send(e)
        print("Could not send video\n" + e)
    await ctx.send(ctx.message.author.mention)
    os.remove(filename + ".mp4")
    os.remove(filename + "_temp.mp4")
    await message.delete()


@client.command()
async def clipaudio(ctx, link, start, end, filename, filetype=None):
    if filetype not in ["mp3", "wav", "ogg"]:
        await ctx.send("Missing or no filetype provided. I can do mp3, wav, and ogg.")
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
            filename + ".ogg",
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
            filename + ".ogg",
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
            filename + ".ogg",
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "0",
            filename + ".mp3",
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
        coms = ["ffmpeg", "-i", filename + ".ogg", filename + ".wav"]
        print(shjoin(coms))
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        print(stdout)
        print(stderr.decode("utf-8"))

    # os.rename(filename+".mkv",filename+".mp4")
    try:
        await ctx.send(file=discord.File(filename + "." + filetype.lower()))
    except Exception:
        await message.edit(content="I failed.")
    await ctx.send(ctx.message.author.mention)
    os.remove(filename + ".ogg")
    os.remove(filename + "." + filetype.lower())
    await message.delete()


@client.command()
async def download(ctx, link):
    import codecs

    if "reddit.com" in link or "v.redd.it" in link:
        cookiecoms = [
            "gpg",
            "--pinentry-mode=loopback",
            "--passphrase",
            os.getenv("ENCRYPTPASSPHRASE"),
            "cookies (17).txt.gpg",
        ]
        cookieproc = await asyncio.create_subprocess_exec(
            *cookiecoms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = await cookieproc.communicate()
        message = await ctx.send("Downloading...")
        coms = [
            "yt-dlp",
            "-f",
            "bestvideo+bestaudio",
            "--cookies",
            "cookies (17).txt",
            link,
        ]
        coms2 = [
            "yt-dlp",
            "--get-filename",
            "--cookies",
            "cookies (17).txt",
            "--no-warnings",
            link,
        ]
        print(shjoin(coms))
        print(shjoin(coms2))
        proc = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        # stdout, stderr = await proc.communicate()
        while proc.returncode is None:
            line = await proc.stdout.read(100)
            if not line:
                break
            await message.edit(content=line.decode("utf-8"))
            # await ctx.send(line.decode('utf-8'))
            await asyncio.sleep(1)
        if proc.returncode != 0:
            await ctx.send("return code is not 0. trying something else")
            coms = ["yt-dlp", "--cookies", "cookies (17).txt", link]
            print(shjoin(coms))
            proc = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            # stdout, stderr = await proc.communicate()
            while proc.returncode is None:
                line = await proc.stdout.read(100)
                if not line:
                    break
                await message.edit(content=line.decode("utf-8"))
                # await ctx.send(line.decode('utf-8'))
                await asyncio.sleep(1)
            if proc.returncode != 0:
                await ctx.send("return code is not 0. i give up")
                return
        await message.edit(content="Almost there...")
        out2 = await asyncio.create_subprocess_exec(
            *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        while out2.returncode is None:
            await message.edit(content="A little more...")
        else:
            os.remove("cookies (17).txt")
            try:
                thing = await out2.stdout.read()
                filename = thing.decode("utf-8").split("\n")[0]
                await message.edit(content="Sending video...")
                try:
                    await ctx.send(file=discord.File(filename))
                except Exception as e:
                    await ctx.send(e)
                    await ctx.send(type(e).__name__)
            except discord.HTTPException:
                await ctx.send("File too large, broski <:towashrug:853606191711649812>")
        os.remove(filename)
        await message.delete()

    elif "facebook.com" in link:
        message = await ctx.send("Downloading...")
        # encypted with `gpg -c --pinentry-mode=loopback your-file.txt`
        cookiecoms = [
            "gpg",
            "--pinentry-mode=loopback",
            "--passphrase",
            os.getenv("ENCRYPTPASSPHRASE"),
            "cookies (15).txt.gpg",
        ]
        cookieproc = await asyncio.create_subprocess_exec(
            *cookiecoms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = await cookieproc.communicate()
        # res = stdout.decode('UTF-8').split('\n')[2:]
        # fin = '\n'.join(res)
        # print(fin)
        # return_data = io.BytesIO()
        # return_data.write(fin.encode())
        # return_data.seek(0)
        coms = ["yt-dlp", "-f", "best", "--cookies", "cookies (15).txt", link]
        coms2 = [
            "yt-dlp",
            "-f",
            "best",
            "--get-filename",
            "--cookies",
            "cookies (15).txt",
            "--no-warnings",
            link,
        ]
        print(shjoin(coms))
        print(shjoin(coms2))
        proc = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        while proc.returncode is None:
            line = await proc.stdout.read(100)
            if not line:
                break
            await message.edit(content=line.decode("utf-8"))
            await asyncio.sleep(1)
        await message.edit(content="Almost there...")
        out2 = await asyncio.create_subprocess_exec(
            *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        while out2.returncode is None:
            await message.edit(content="A little more...")
        else:
            os.remove("cookies (15).txt")
            try:
                thing = await out2.stdout.read()
                filename = thing.decode("utf-8").split("\n")[-2]
                print(thing.decode("utf-8"))
                await message.edit(content="Sending video...")
                try:
                    await ctx.send(file=discord.File(filename))
                except Exception as e:
                    await ctx.send(e)
            except discord.HTTPException:
                await ctx.send("File too large, broski <:towashrug:853606191711649812>")
            except Exception as e:
                await message.edit(content=e)
        os.remove(filename)

        await message.delete()

    elif "instagram.com" in link:
        message = await ctx.send("Downloading...")
        cookiecoms = [
            "gpg",
            "--pinentry-mode=loopback",
            "--passphrase",
            os.getenv("ENCRYPTPASSPHRASE"),
            "instacook.txt.gpg",
        ]
        cookieproc = await asyncio.create_subprocess_exec(
            *cookiecoms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = await cookieproc.communicate()
        # res = stdout.decode('UTF-8').split('\n')[2:]
        # fin = '\n'.join(res)
        # print(fin)
        # return_data = io.BytesIO()
        # return_data.write(fin.encode())
        # return_data.seek(0)
        coms = ["yt-dlp", "-f", "best", "--cookies", "instacook.txt", link]
        coms2 = [
            "yt-dlp",
            "-f",
            "best",
            "--get-filename",
            "--cookies",
            "instacook.txt",
            "--no-warnings",
            link,
        ]
        print(shjoin(coms))
        print(shjoin(coms2))
        proc = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        while proc.returncode is None:
            line = await proc.stdout.read(100)
            if not line:
                break
            await message.edit(content=line.decode("utf-8"))
            await asyncio.sleep(1)
        await message.edit(content="Almost there...")
        out2 = await asyncio.create_subprocess_exec(
            *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        while out2.returncode is None:
            await message.edit(content="A little more...")
        else:
            os.remove("instacook.txt")
            try:
                thing = await out2.stdout.read()
                filename = thing.decode("utf-8").split("\n")[-2]
                print(thing.decode("utf-8"))
                await message.edit(content="Sending video...")
                try:
                    await ctx.send(file=discord.File(filename))
                except Exception as e:
                    await ctx.send(e)
            except discord.HTTPException:
                await ctx.send("File too large, broski <:towashrug:853606191711649812>")
            except Exception as e:
                await message.edit(content=e)
        os.remove(filename)

        await message.delete()

        # await ctx.send('I can\'t do Facebook links, unfortunately. It should work but idk why it don\'t')
    # tiktok
    elif "tiktok.com" in link:
        message = await ctx.send("Downloading...")
        coms = ["tiktok-yt-dlp/yt-dlp", "-f", "best", link]
        coms2 = [
            "tiktok-yt-dlp/yt-dlp",
            "-f",
            "best",
            "--get-filename",
            "--no-warnings",
            link,
        ]
        print(shjoin(coms))
        print(shjoin(coms2))
        proc = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        # stdout, stderr = await proc.communicate()
        while proc.returncode is None:
            line = await proc.stdout.read(100)
            if not line:
                break
            await message.edit(content=line.decode("utf-8"))
            await asyncio.sleep(1)
        await message.edit(content="Almost there...")
        out2 = await asyncio.create_subprocess_exec(
            *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        while out2.returncode is None:
            await message.edit(content="A little more...")
        else:
            try:
                thing = await out2.stdout.read()
                filename = thing.decode("utf-8").split("\n")[0]
                await message.edit(content="Sending video...")
                try:
                    await ctx.send(file=discord.File(filename))
                except Exception as e:
                    await ctx.send(e)
            except discord.HTTPException:
                await ctx.send("File too large, broski <:towashrug:853606191711649812>")
            except Exception as e:
                await message.edit(content=e)
        os.remove(filename)
        await message.delete()

    # yt links usually
    else:
        message = await ctx.send("Downloading...")
        coms = ["yt-dlp", "-f", "best", link]
        coms2 = ["yt-dlp", "-f", "best", "--get-filename", "--no-warnings", link]
        print(shjoin(coms))
        print(shjoin(coms2))
        proc = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        # stdout, stderr = await proc.communicate()
        while proc.returncode is None:
            line = await proc.stdout.read(100)
            if not line:
                break
            await message.edit(content=line.decode("utf-8"))
            await asyncio.sleep(1)
        await message.edit(content="Almost there...")
        out2 = await asyncio.create_subprocess_exec(
            *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        while out2.returncode is None:
            await message.edit(content="A little more...")
        else:
            try:
                thing = await out2.stdout.read()
                filename = thing.decode("utf-8").split("\n")[0]
                await message.edit(content="Sending video...")
                try:
                    await ctx.send(file=discord.File(filename))
                except Exception as e:
                    await ctx.send(e)
            except discord.HTTPException:
                await ctx.send("File too large, broski <:towashrug:853606191711649812>")
            except Exception as e:
                await message.edit(content=e)
        os.remove(filename)
        await message.delete()


import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import dateutil.parser as dp

from discord import Webhook
import aiohttp


@client.command()
async def stream(ctx, link, noembed=None):
    if link.startswith("https://youtu.be"):
        idd = link.split("/")[-1].split("?")[0]
    elif link.startswith("https://www.youtube.com/"):
        idd = link.split("=")[1].split("&")[0]
    else:
        await ctx.send("Not a YT link!", delete_after=3.0)
        wrong = True
    wrong = False
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
        dsctime = "<t:" + str(t_in_seconds).split(".")[0] + ":F>"
        reltime = "<t:" + str(t_in_seconds).split(".")[0] + ":R>"
        dttime = datetime.strptime(isotime, "%Y-%m-%dT%H:%M:%S%z")
        dayofweek = parsed_t.weekday()

        f = open("list.txt", "a")  # add stream url and time to list.txt
        f.write(link + " " + parsed_t.strftime("%a %b %d %Y %H:%M:%S") + "\n")
        f.close()
        a_file = open("list.txt", "r")  # reads list.txt
        lines = a_file.read().splitlines()
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
            url="https://www.youtube.com/channel/" + channelid,
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
                await webhook.send(
                    reltime + " **" + author + "** - [" + title + "](<" + link + ">)"
                )
        await ctx.message.delete()
        try:
            client.loop.create_task(
                run_at(parsed_t.replace(tzinfo=None), open_url(link), link)
            )
        except Exception as e:
            await ctx.send("Error: " + e)


async def clear_list():
    a_file = open("list.txt", "r")
    lines = a_file.read().splitlines()
    a_file.close()
    with open("list.txt", "w+") as r:
        for i in lines:
            if i.split(" ")[0] != url:
                r.write(i + "\n")


async def open_url(url):
    print(str(url) + " is starting!")
    f = open("log.txt", "a")
    f.write("open_url running " + url + "\n")
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
    print(str(count) + " times")

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
    await clear_list()


from petpetgif import petpet
import requests
from io import BytesIO


@client.command()
async def pet(ctx, url):
    if ctx.message.mentions.__len__() > 0:
        for user in ctx.message.mentions:
            pfp = requests.get(user.avatar_url)
            source = BytesIO(
                pfp.content
            )  # file-like container to hold the emoji in memory
            source.seek(0)
            dest = BytesIO()  # container to store the petpet gif in memory
            petpet.make(source, dest)
            dest.seek(0)
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
            await webhook.send(
                file=discord.File(dest, filename=f"petpet.gif"),
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.avatar_url,
            )

            webhooks = await ctx.channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()
    elif url.startswith("http"):
        pfp = requests.get(url)
        source = BytesIO(pfp.content)  # file-like container to hold the emoji in memory
        source.seek(0)
        dest = BytesIO()  # container to store the petpet gif in memory
        petpet.make(source, dest)
        dest.seek(0)
        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        await webhook.send(
            file=discord.File(dest, filename=f"petpet.gif"),
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.avatar_url,
        )

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()


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
    print(str(count) + " times")


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
async def makeembed(ctx, title, description):
    if ctx.author.id == 396892407884546058:
        print("is kur0")
        if description.startswith("https"):
            print("description is url")
            x = requests.get(
                "https://quiet-sun-6d6e.cantilfrederick.workers.dev/?"
                + str(description)
            )
            embed = discord.Embed(title=title, description=x.text)
            await ctx.send(embed=embed)
            await ctx.message.delete()
        else:
            print("description is text")
            embed = discord.Embed(title=title, description=description)
            await ctx.send(embed=embed)
            await ctx.message.delete()
    else:
        print(ctx.author.id)
        await ctx.send("only kur0 can do this lel")
        await ctx.message.delete()


@client.command()
async def editembed(ctx, id: int, title, description):
    if ctx.author.id == 396892407884546058:
        print("is kur0")
        if description.startswith("https"):
            print("description is url")
            msg = await ctx.fetch_message(id)
            x = requests.get(
                "https://quiet-sun-6d6e.cantilfrederick.workers.dev/?"
                + str(description)
            )
            embed = discord.Embed(title=title, description=x.text)
            await msg.edit(embed=embed)
            await ctx.message.delete()
        else:
            print("description is text")
            msg = await ctx.fetch_message(id)
            embed = discord.Embed(title=title, description=description)
            await msg.edit(embed=embed)
            await ctx.message.delete()
    else:
        print(ctx.author.id)
        await ctx.send("only kur0 can do this lel")
        await ctx.message.delete()


@client.command()
async def repost(ctx, url):
    if ctx.author.id == 396892407884546058:
        print("is kur0")
        msg = await ctx.send("Checking for updates...")
        coms = ["rclone/rclone", "selfupdate"]
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = await out.communicate()
        await msg.edit(content=msg.content + "\n" + stdout.decode())
        await msg.edit(content=msg.content + "\n" + "Download config file...")
        coms = [
            "wget",
            os.getenv("RCLONE_CONFIG_URL"),
            "-O",
            "/config/rclone/rclone.conf",
        ]
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = await out.communicate()
        print(stdout.decode())
        await msg.edit(content=msg.content + "Done!")
        if "www.youtube.com/watch" in url:
            fixed_link = "https://youtu.be/" + url[32:43]
        elif "www.youtube.com/shorts" in url:
            fixed_link = "https://youtu.be/" + url[27:38]
        elif "youtu.be" in url:
            fixed_link = url[0:28]

        else:
            fixed_link = url
        # download vid
        await msg.edit(content=msg.content + "\n" + "Downloading video...")
        coms = [
            "yt-dlp",
            "-i",
            "--no-warnings",
            "--yes-playlist",
            "--add-metadata",
            "--merge-output-format",
            "mkv",
            "--all-subs",
            "--write-sub",
            "--convert-subs",
            "srt",
            "--embed-subs",
            "-f",
            "bestvideo[ext=webm]+bestaudio[ext=webm]/bestvideo+bestaudio/best",
            "-o",
            "%(title)s-%(id)s.%(ext)s",
            fixed_link,
        ]
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = await out.communicate()
        print(stdout.decode())

        if out.returncode == 0:
            await msg.edit(content=msg.content + "Done! (" + str(out.returncode) + ")")
        else:
            try:
                await msg.edit(
                    content=msg.content
                    + "\n Return code: "
                    + str(out.returncode)
                    + "\n"
                    + stderr.decode()
                )
            except:
                await msg.edit(
                    content=msg.content
                    + "\n Return code: "
                    + str(out.returncode)
                    + "\n"
                    + stdout.decode()
                )
            return

        # get title and filename
        await msg.edit(content=msg.content + "\n" + "Getting title and filename...")
        coms = [
            "yt-dlp",
            "--get-title",
            "--get-filename",
            "-o",
            "%(title)s-%(id)s",
            "--no-warnings",
            fixed_link,
        ]
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = await out.communicate()
        result = stdout.decode()
        title = result.splitlines()[-2]
        filename = result.splitlines()[-1]
        print(title + "\n" + filename)
        fname1 = glob.glob(glob.escape(filename) + ".*")
        for i in fname1:
            if not i.endswith(".srt") and not i.endswith(".json"):
                fname = i
            else:
                os.remove(i)
        print(fname)

        if out.returncode == 0:
            await msg.edit(content=msg.content + "Done! (" + str(out.returncode) + ")")
        else:
            try:
                await msg.edit(
                    content=msg.content
                    + "\n Return code: "
                    + str(out.returncode)
                    + "\n"
                    + stderr.decode()
                )
            except:
                await msg.edit(
                    content=msg.content
                    + "\n Return code: "
                    + str(out.returncode)
                    + "\n"
                    + stdout.decode()
                )
            return
        # copy to drive
        await msg.edit(content=msg.content + "\n" + "Copying to Drive...")
        coms = [
            "rclone/rclone",
            "copy",
            fname,
            "g2:/archived youtube vids/",
            "--transfers",
            "20",
            "--checkers",
            "20",
            "-v",
            "--stats=5s",
            "--buffer-size",
            "128M",
            "--drive-chunk-size",
            "128M",
            "--drive-acknowledge-abuse",
            "--drive-keep-revision-forever",
            "--drive-server-side-across-configs=true",
            "--suffix=2021_12_22_092152",
            "--suffix-keep-extension",
        ]
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = await out.communicate()
        print(stdout.decode())
        # print(stderr)

        if out.returncode == 0:
            await msg.edit(content=msg.content + "Done! (" + str(out.returncode) + ")")
        else:
            try:
                await msg.edit(
                    content=msg.content
                    + "\n Return code: "
                    + str(out.returncode)
                    + "\n"
                    + stderr.decode()
                )
            except:
                await msg.edit(
                    content=msg.content
                    + "\n Return code: "
                    + str(out.returncode)
                    + "\n"
                    + stdout.decode()
                )
            return
        # upload to fb
        await msg.edit(content=msg.content + "\n" + "Uploading to FB...")
        access_token = os.getenv("FB_ACCESS_TOKEN")

        url = (
            "https://graph-video.facebook.com/v8.0/100887555109330/videos?access_token="
            + access_token
            + "&limit=10"
        )
        files = {"file": ("vid.mp4", open(fname, mode="rb"))}
        flag = requests.post(
            url,
            files=files,
            data={"description": title + "\n(NOT MINE) Source: " + fixed_link},
        )  # .text
        flagg = flag.text

        data = json.loads(flagg)

        if flag.status_code != 200:
            print(flagg)

        else:
            print("We gucci, my dude.")
            vid_id = data["id"]

            if out.returncode == 0:
                await msg.edit(
                    content=msg.content + "Done! (" + str(out.returncode) + ")"
                )
            else:
                try:
                    await msg.edit(
                        content=msg.content
                        + "\n Return code: "
                        + str(out.returncode)
                        + "\n"
                        + stderr.decode()
                    )
                except:
                    await msg.edit(
                        content=msg.content
                        + "\n Return code: "
                        + str(out.returncode)
                        + "\n"
                        + stdout.decode()
                    )
                return
            await msg.delete()
            await ctx.send(title + " has been uploaded!")
            await ctx.send(
                "Vid link: https://web.facebook.com/100887555109330/videos/" + vid_id
            )
            post_link = "https://web.facebook.com/100887555109330/videos/" + vid_id
            await ctx.send(
                "Share to FB: https://www.facebook.com/sharer.php?u=" + post_link
            )
            os.remove(fname)
    else:
        print(ctx.author.id)
        await ctx.send("you found secret command. only kur0 can do this tho lel")


from ftplib import FTP

# from aiomcrcon import Client as mcrconClient
from mcrcon import MCRcon

# from rcon import rcon


@client.command()
async def addoffline(ctx, username):
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
        await ctx.send("Adding " + str(username) + " to list of offline users...")

        ftp = FTP(host="us01.pebblehost.com")
        ftp.login(user=os.getenv("PEBBLE_EMAIL"), passwd=os.getenv("PEBBLE_PASS"))
        # ftp.cwd('mods')
        # ftp.cwd('EasyAuth')
        r = io.BytesIO()
        ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
        config = json.loads(r.getvalue())
        if username.lower() in config["main"]["forcedOfflinePlayers"]:
            await ctx.send(str(username) + " is alreading in the list!")
            return
        else:
            config["main"]["forcedOfflinePlayers"].append(username.lower())
        print(config["main"]["forcedOfflinePlayers"])
        dump = json.dumps(config, indent=2).encode("utf-8")
        # print(dump)
        ftp.storbinary("STOR /mods/EasyAuth/config.json", io.BytesIO(dump))
        # print(ftp.retrlines('LIST'))
        # coms = ["mcrcon", "-H", "51.81.142.14", "--password", str(os.getenv("RCON_PASS")), "-w", "1", "auth reload"]

        # out = await asyncio.create_subprocess_exec(*coms,
        #          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # stdout, stderr = await out.communicate()
        # print(stdout.decode())
        # print(stderr)
        # mc_client = mcrconClient("51.81.142.14", 25575, str(os.getenv("RCON_PASS")))
        # await mc_client.connect()

        # response = await mc_client.send_cmd("/say a")
        # print(response)
        # await mc_client.close()

        with MCRcon("51.81.142.14", str(os.getenv("RCON_PASS")), 8082) as mcr:
            resp = mcr.command("/auth reload")
            print(resp)
        await ctx.send("Done!")

        # response = await rcon('/say a',host='51.81.142.14', port=25575, passwd=str(os.getenv("RCON_PASS")))
        # print(response)
    else:
        await ctx.send("Only Avi/Admins/Mods can use this command")


@client.command()
async def viewoffline(ctx):
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

        ftp = FTP(host="us01.pebblehost.com")
        ftp.login(user=os.getenv("PEBBLE_EMAIL"), passwd=os.getenv("PEBBLE_PASS"))
        r = io.BytesIO()
        ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
        config = json.loads(r.getvalue())
        print(config["main"]["forcedOfflinePlayers"])
        await ctx.send(
            "Players added to the offline list are: "
            + ", ".join(config["main"]["forcedOfflinePlayers"])
        )
    else:
        await ctx.send("Only Avi/Admins/Mods can use this command")


@client.command()
async def removeoffline(ctx, username):
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
        await ctx.send("Removing " + str(username) + " from list of offline users...")

        ftp = FTP(host="us01.pebblehost.com")
        ftp.login(user=os.getenv("PEBBLE_EMAIL"), passwd=os.getenv("PEBBLE_PASS"))
        # ftp.cwd('mods')
        # ftp.cwd('EasyAuth')
        r = io.BytesIO()
        ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
        config = json.loads(r.getvalue())
        if username.lower() in config["main"]["forcedOfflinePlayers"]:
            config["main"]["forcedOfflinePlayers"].remove(username.lower())
        else:
            await ctx.send(str(username) + " isn't in the list!")
            return
        print(config["main"]["forcedOfflinePlayers"])
        dump = json.dumps(config, indent=2).encode("utf-8")
        # print(dump)
        ftp.storbinary("STOR /mods/EasyAuth/config.json", io.BytesIO(dump))
        # print(ftp.retrlines('LIST'))
        # coms = ["mcrcon", "-H", "51.81.142.14", "--password", str(os.getenv("RCON_PASS")), "-w", "1", "auth reload"]

        # out = await asyncio.create_subprocess_exec(*coms,
        #          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # stdout, stderr = await out.communicate()
        # print(stdout.decode())
        # print(stderr)
        # mc_client = mcrconClient("51.81.142.14", 25575, str(os.getenv("RCON_PASS")))
        # await mc_client.connect()

        # response = await mc_client.send_cmd("/say a")
        # print(response)
        # await mc_client.close()

        with MCRcon("51.81.142.14", str(os.getenv("RCON_PASS")), 8082) as mcr:
            resp = mcr.command("/auth reload")
            print(resp)
        await ctx.send("Done!")

        # response = await rcon('/say a',host='51.81.142.14', port=25575, passwd=str(os.getenv("RCON_PASS")))
        # print(response)
    else:
        await ctx.send("Only Avi/Admins/Mods can use this command")


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


from saucenao_api import SauceNao


@client.command(aliases=["findsauce", "sauce"])
async def getsauce(ctx, link=None):

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

            # print("embmeds: {0}".format(msg.embeds))
            # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
            #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
            # link= msg.attachments[0].url
            else:
                await ctx.send("the message you replied to has no image, baka!")
        else:
            await ctx.send("you did something wrong. brug. try again.")
            return
        print(link)

    msg = await ctx.send("Getting sauce...")
    sauce = SauceNao(os.getenv("SAUCENAO_KEY"))
    try:
        results = sauce.from_url(link)  # or from_file()
        print("30S: {0}".format(results.short_remaining))
        print("24H: {0}".format(results.long_remaining))
        await msg.edit(
            content="30s limit: {0} request(s) left\n24h limit: {1} request(s) left".format(
                results.short_remaining, results.long_remaining
            ),
            delete_after=5,
        )
    except Exception as e:
        await msg.edit("I fail. Reason:\n{0}".format(e))
        return
    print("{0} results!".format(len(results)))
    result_count = len(results)
    results_dict = {}
    embed_dict = {}
    i = 0
    while i < result_count:
        results_dict[i] = results[i]
        i += 1
        print(len(results_dict))
    for i in range(len(results_dict)):
        # await ctx.send(results_dict[i].title)
        try:
            site_name = re.search(r"(?<=https:\/\/)[^\/]*", results_dict[i].urls[0])
            embed_dict[i] = discord.Embed(
                title=results_dict[i].title,
                description="{0}% accurate".format(results_dict[i].similarity),
                url=results_dict[i].urls[0],
            )
            embed_dict[i].set_author(name=results_dict[i].author)
            embed_dict[i].set_image(url=results_dict[i].thumbnail)
            embed_dict[i].set_footer(text=site_name[0])
        except IndexError:
            embed_dict[i] = discord.Embed(
                title=results_dict[i].title,
                description="{0}% accurate".format(results_dict[i].similarity),
            )
            embed_dict[i].set_author(name=results_dict[i].author)
            embed_dict[i].set_image(url=results_dict[i].thumbnail)
        #  embed_dict[i].set_footer(text="{0}/{1}".format(i+1,result_count))
        except Exception as e:
            print(e)
        # try:
        #   await msg.delete()
        # except:
        #   pass
        # button1 = Button(label="Previous")
        # button2 = Button(label="Next")

        # async def prev_callback(interaction):
        #   await interaction.response.send_message() #i want it to send outside_var

        # button1.callback = prev_callback()
        # view= View()
        # view.add_item(button1)
        # view.add_item(button2)
    paginator = pages.Paginator(pages=embed_dict)
    await paginator.send(ctx)
    # await ctx.send(embed=embed_dict[i],view=view)
    # await buttons.send(
    # channel = ctx.channel.id,
    # content = None,
    # embed = embed_dict[i],
    # components = [
    # ActionRow([
    # Button(
    #   style = ButtonType().Secondary,
    #   label = "Previous",
    #   custom_id = "previous"
    #       ),
    # Button(
    #   style = ButtonType().Secondary,
    #   label = "Next",
    #   custom_id = "next"
    #       )
    # ])
    # ])

    # await ctx.send(embed = e)


# ----------------------------------------------------
# HELP
@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(
        title="Commands",
        description="Here are my sussy commands!\nUse __**k.help <command>**__ for more info on that command.",
    )
    em.add_field(
        name="copypasta",
        value="glasses\nnene\nnenelong\nstopamongus\nconfession\nwristworld",
    )
    em.add_field(name="sus", value="on\noff\nmegasus\nbulk")
    em.add_field(name="why", value="fortnite")
    em.add_field(
        name="others",
        value="emote\ngetemotes\nbadapple\nclip\nfastclip\nclipaudio\ndownload\nstream\npet\nsauce",
    )
    em.add_field(name="reactions", value="fmega\nkotowaru\nascend\njizz")
    em.add_field(
        name="vc",
        value="join\nstop\nstoploop\nleave\nletsgo\nvtubus\nding\nyodayo\nyodazo\njonathan\njoseph\njotaro\njosuke\ngiorno\nkira\npillarmen\nbotansneeze\nboom\nogey\nrrat\nfart\nmogumogu\nbababooey\ndog\ntotsugeki\ntacobell\namongus\ndanganronpa\nwater\nnecoarc\nvsauce\ngigachad",
    )
    em.add_field(
        name="TTS", value=' just do ] while in VC ("k.help tts" for more info)'
    )
    await ctx.send(embed=em)


@help.command()
async def glasses(ctx):
    em = discord.Embed(
        title="Glasses", description="Gives the entire fubuki glasses copypasta"
    )
    await ctx.send(embed=em)


@help.command()
async def nene(ctx):
    em = discord.Embed(title="Nene", description="Gives Nenechi's full title")
    await ctx.send(embed=em)


@help.command()
async def nenelong(ctx):
    em = discord.Embed(title="Nene", description="Gives Nenechi's LONGER full title")
    await ctx.send(embed=em)


@help.command()
async def on(ctx):
    em = discord.Embed(
        title="On",
        description="Enables permanent sus mode. Sus replies do not get deleted within 3 seconds.",
    )
    await ctx.send(embed=em)


@help.command()
async def off(ctx):
    em = discord.Embed(
        title="Off",
        description="Disables permanent sus mode. Sus replies get deleted within 3 seconds.",
    )
    await ctx.send(embed=em)


@help.command()
async def megasus(ctx):
    em = discord.Embed(
        title="Megasus",
        description="Gives some random amongus copypasta I found on reddit.",
    )
    await ctx.send(embed=em)


@help.command()
async def bulk(ctx):
    em = discord.Embed(title="Bulk", description="Sends sus messages in bulk.")
    em.add_field(name="**Syntax**", value="k.bulk <number>")
    await ctx.send(embed=em)


@help.command()
async def stopamongus(ctx):
    em = discord.Embed(
        title="Stop posting about Among Us!",
        description="Sends the stop posting about among us copypasta",
    )
    await ctx.send(embed=em)


@help.command()
async def confession(ctx):
    em = discord.Embed(
        title="Matsuri's Confession", description="Sends Matsuri's confession to Fubuki"
    )
    await ctx.send(embed=em)


@help.command()
async def fortnite(ctx):
    em = discord.Embed(title="Fortnite", description="Sends the fortnite dance in text")
    await ctx.send(embed=em)


@help.command(aliases=["e"])
async def emote(ctx):
    em = discord.Embed(
        title="Emote",
        description="Sends an animated emote from any server that this bot is in.",
    )
    em.add_field(name="**Syntax**", value="k.emote <emotename>")
    em.add_field(name="**Aliases**", value="e")
    await ctx.send(embed=em)


@help.command(aliases=["ge"])
async def getemotes(ctx):
    em = discord.Embed(
        title="Get Emotes!",
        description="Sends all emotes that this bot has. It has emotes for all servers it's in.",
    )
    em.add_field(name="**Aliases**", value="ge")
    await ctx.send(embed=em)


@help.command()
async def wristworld(ctx):
    em = discord.Embed(
        title="Wristworld", description="Sends the wristworld miku copypasta."
    )
    await ctx.send(embed=em)


@help.command()
async def fmega(ctx):
    em = discord.Embed(title="F Mega!", description="Sends the F MEGA gif from Jojo's.")
    await ctx.send(embed=em)


@help.command()
async def kotowaru(ctx):
    em = discord.Embed(
        title="Daga kotowaru!", description="Use this to refuse someone's offer"
    )
    await ctx.send(embed=em)


@help.command()
async def ascend(ctx):
    em = discord.Embed(
        title="Ascend to Heaven!",
        description="Use this to to ascend when something glorious occurs.",
    )
    await ctx.send(embed=em)


@help.command()
async def jizz(ctx):
    em = discord.Embed(title="Jizz", description="Use this to jizz.")
    await ctx.send(embed=em)


@help.command()
async def letsgo(ctx):
    em = discord.Embed(title="Let's go!", description="Playus 'Let's gooo' in vc")
    await ctx.send(embed=em)


@help.command()
async def vtubus(ctx):
    em = discord.Embed(title="Vtubus", description="vtubus")
    await ctx.send(embed=em)


@help.command()
async def ding(ctx):
    em = discord.Embed(
        title="Ding ding ding ding ding ddi di ding", description="amongus"
    )
    await ctx.send(embed=em)


@help.command()
async def yodayo(ctx):
    em = discord.Embed(title="Yo dayo!", description="Plays Ayame's 'Yo dayo!' in VC")
    await ctx.send(embed=em)


@help.command()
async def yodazo(ctx):
    em = discord.Embed(title="Yo dazo!", description="Plays Ayame's 'Yo dazo!' in VC")
    await ctx.send(embed=em)


@help.command()
async def jonathan(ctx):
    em = discord.Embed(
        title="Jonathan's theme", description="Plays Jonathan's theme in VC"
    )
    await ctx.send(embed=em)


@help.command()
async def joseph(ctx):
    em = discord.Embed(title="Joseph's theme", description="Plays Joseph's theme in VC")
    await ctx.send(embed=em)


@help.command()
async def jotaro(ctx):
    em = discord.Embed(title="Jotaro's theme", description="Plays Jotaro's theme in VC")
    await ctx.send(embed=em)


@help.command()
async def josuke(ctx):
    em = discord.Embed(title="Josuke's theme", description="Plays Josuke's theme in VC")
    await ctx.send(embed=em)


@help.command()
async def giorno(ctx):
    em = discord.Embed(title="Giorno's theme", description="Plays Giorno's theme in VC")
    await ctx.send(embed=em)


@help.command()
async def kira(ctx):
    em = discord.Embed(
        title="Yoshikage Kira's theme", description="Plays Yoshikage Kira's theme in VC"
    )
    await ctx.send(embed=em)


@help.command()
async def pillarmen(ctx):
    em = discord.Embed(
        title="Pillar Men Theme", description="Plays the Pillar Men Theme in VC"
    )
    await ctx.send(embed=em)


@help.command()
async def tts(ctx):
    em = discord.Embed(title="Text to speech", description="Send a TTS message in VC")
    em.add_field(name="**Syntax**", value="] <message>")
    em.add_field(
        name="**Accents**",
        value="] (US default)\n]au (Australia)\n]uk (United Kingdom)\n]in (India)",
    )
    await ctx.send(embed=em)


@help.command()
async def badapple(ctx):
    em = discord.Embed(
        title="Bad Apple but in custom emotes",
        description="Sends 80 animated emotes that all make up the Bad Apple PV (Only works on PC)",
    )
    em.add_field(name="**Emotes by:**", value="https://github.com/gohjoseph")
    await ctx.send(embed=em)


@help.command()
async def clip(ctx):
    em = discord.Embed(
        title="Clip a YT Video",
        description="clips a YouTube video given the start and end times (HH:MM:SS)\n**SLOWER** than `fastclip` but accurate",
    )
    em.add_field(
        name="**Syntax**", value="k.clip <url> <start time> <end time> <filename>"
    )
    em.add_field(
        name="**Example**",
        value="k.clip https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:00:52 00:01:05 filename",
    )
    await ctx.send(embed=em)


@help.command()
async def fastclip(ctx):
    em = discord.Embed(
        title="Quickly clip a YT Video",
        description="clips a YouTube video given the start and end times (HH:MM:SS)\n**FASTER** than `clip` but will start at the nearest keyframe, so it'll start a couple seconds earlier than the given timestamp",
    )
    em.add_field(
        name="**Syntax**", value="k.clip <url> <start time> <end time> <filename>"
    )
    em.add_field(
        name="**Example**",
        value="k.fastclip https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:00:52 00:01:05 filename",
    )
    await ctx.send(embed=em)


@help.command()
async def download(ctx):
    em = discord.Embed(
        title="Download a YT Video", description="Download a YouTube of your choice"
    )
    em.add_field(name="**Syntax**", value="k.download <url>")
    await ctx.send(embed=em)


@help.command()
async def botansneeze(ctx):
    em = discord.Embed(
        title="Botan Sneeze", description="because fuck you, have a botan sneeze"
    )
    em.add_field(name="**Syntax**", value="k.botansneeze [loop]")
    await ctx.send(embed=em)


@help.command()
async def boom(ctx):
    em = discord.Embed(
        title="Vine Boom SFX", description="plays the funni boom sfx in vc"
    )
    await ctx.send(embed=em)


@help.command(aliases=["ogei"])
async def ogey(ctx):
    em = discord.Embed(title="Ogey...", description="Plays Pekora's ogey in VC.")
    em.add_field(name="**Aliases**", value="ogei")
    await ctx.send(embed=em)


@help.command()
async def rrat(ctx):
    em = discord.Embed(title="Rrat!", description="Plays Pekora's rrat in VC.")
    await ctx.send(embed=em)


@help.command()
async def fart(ctx):
    em = discord.Embed(
        title="Reverb fart sfx", description="Plays funni fart sound in VC."
    )
    await ctx.send(embed=em)


@help.command()
async def mogumogu(ctx):
    em = discord.Embed(title="Mogu mogu!", description="Plays okayu's mogu mogu in VC.")
    await ctx.send(embed=em)


@help.command()
async def bababooey(ctx):
    em = discord.Embed(title="Bababooey!", description="Plays bababooey in VC.")
    await ctx.send(embed=em)


@help.command()
async def dog(ctx):
    em = discord.Embed(
        title="What the dog doin?", description="Plays 'what da dog doin' in VC."
    )
    await ctx.send(embed=em)


@help.command()
async def totsugeki(ctx):
    em = discord.Embed(title="TOTSUGEKI!!!", description="Plays May's Totsugeki in VC.")
    await ctx.send(embed=em)


@help.command(aliases=["bong"])
async def tacobell(ctx):
    em = discord.Embed(
        title="Taco Bell bong sfx",
        description="Plays the funny taco bell sound effect in VC.",
    )
    em.add_field(name="**Aliases**", value="bong")
    await ctx.send(embed=em)


@help.command(aliases=["amogus"])
async def amongus(ctx):
    em = discord.Embed(
        title="AMONGUS!", description="Plays the guy yelling amongus in VC."
    )
    em.add_field(name="**Aliases**", value="amogus")
    await ctx.send(embed=em)


@help.command(aliases=["classtrial"])
async def danganronpa(ctx):
    em = discord.Embed(
        title="Class trial time!",
        description="Plays '議論 -HEAT UP-' from Danganronpa in VC.",
    )
    em.add_field(name="**Aliases**", value="classtrial")
    await ctx.send(embed=em)


@help.command()
async def join(ctx):
    em = discord.Embed(title="Join VC", description="Sus bot will enter the VC.")
    await ctx.send(embed=em)


@help.command()
async def stop(ctx):
    em = discord.Embed(
        title="STOP!",
        description="Sus bot will stop playing if it's playing something in VC.",
    )
    await ctx.send(embed=em)


@help.command()
async def stoploop(ctx):
    em = discord.Embed(
        title="STOP THE LOOP!",
        description="Sus bot will stop playing if it's playing something in VC that has loop mode enabled.",
    )
    em.add_field(name="**How loop???**", value="k.commandname loop")
    await ctx.send(embed=em)


@help.command()
async def leave(ctx):
    em = discord.Embed(title="Sayonara...", description="Sus bot will leave the VC.")
    await ctx.send(embed=em)


@help.command()
async def stream(ctx):
    em = discord.Embed(
        title="YouTube Stream Time Embed",
        description="Sends an embed of a YouTube stream with its start time.",
    )
    em.add_field(name="**Syntax**", value="k.stream https://youtu.be/wNMW87foNAI")
    await ctx.send(embed=em)


@help.command()
async def water(ctx):
    em = discord.Embed(
        title="Water and Water and Water Water",
        description="Plays 'Water and Water and Water Water'in VC.",
    )
    await ctx.send(embed=em)


@help.command()
async def necoarc(ctx):
    em = discord.Embed(title="Neco arc", description="Plays neco arc in VC.")
    await ctx.send(embed=em)


@help.command()
async def vsauce(ctx):
    em = discord.Embed(
        title="Vsauce music", description="Plays the vsauce music in VC."
    )
    await ctx.send(embed=em)


@help.command()
async def gigachad(ctx):
    em = discord.Embed(
        title="Gigachad", description="Plays a bit of 'Can You Feel My Heart' in VC."
    )
    await ctx.send(embed=em)


@help.command()
async def pet(ctx):
    em = discord.Embed(
        title="Pet user", description="Sends a gif of the mentioned user being petted."
    )
    em.add_field(name="**Syntax**", value="k.pet <mentioned user>\nk.pet <image url>")
    await ctx.send(embed=em)


@help.command(aliases=["findsauce", "getsauce"])
async def sauce(ctx):
    em = discord.Embed(
        title="Get sauce", description="Uses Saucenao API to find sauce."
    )
    em.add_field(
        name="**Syntax**",
        value="k.sauce <url>\nUpload image with k.sauce\nReply to a message with k.sauce ",
    )
    em.add_field(name="**Aliases**", value="findsauce,getsauce")
    await ctx.send(embed=em)


@help.command()
async def clipaudio(ctx):
    em = discord.Embed(
        title="Clip Audio", description="Clips the audio of a given YouTube video"
    )
    em.add_field(
        name="**Syntax**",
        value="k.clipaudio <url> <start time> <end time> <filename> <filetype>",
    )
    em.add_field(name="**Filetypes**", value="mp3\nwav\nogg")
    em.add_field(
        name="**Example**",
        value="k.clipaudio https://www.youtube.com/watch?v=UIp6_0kct_U 00:00:56 00:01:05 poger mp3",
    )
    await ctx.send(embed=em)


async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.now()
    await asyncio.sleep((dt - now).total_seconds())


async def run_at(dt, coro, url):
    now = datetime.now()
    nowstr = now.strftime("%m/%d/%Y %H:%M:%S")
    print(url + " is scheduled!")
    f = open("log.txt", "a")
    f.write(url + " - scheduled at " + nowstr + "\n")
    f.close()
    await wait_until(dt)
    f = open("log.txt", "a")
    f.write(url + " starting!" + "\n")
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
            day = i.split(" ")[1]
            timee = i.split(" ")[5]
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
print("schedules checked!")
keep_alive()
isDiscordrunning = False
try:
    client.run(os.getenv("TOKEN"))
    isDiscordrunning = True
except Exception as e:
    while isDiscordrunning is False:
        try:
            client.run(os.getenv("TOKEN"))
            isDiscordrunning = True
        except Exception as e:
            print("nope. not working")
            print(type(e).__name__)
            time.sleep(900)


# if __name__ == '__main__':
# run app in debug mode on port 5000
# schedule.clear()

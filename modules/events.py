from disnake.ext import commands
import disnake
import time
import random
import re
import subprocess
import json
import asyncio
from gtts import gTTS
import difflib
from datetime import datetime
import pytz
import os

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

sugma_replies = ["sugma balls!! hahahaaaaa", "sugma.... sugma balls!!!!!!!"]

sugoma_replies = ["sugoma balls!! hahahaaaaa", "sugoma.... sugoma balls!!!!!!!"]

custom_words = ["amgus", "amogus", "sushi", "pog"]

deez_replies = [
    "can i put my balls in yo jaws",
    "ong fr?",
    "ligma",
    "updog",
    "my name jef",
]

# hidden_commands = [
#     "addoffline",
#     "makeembed",
#     "sched",
#     "tasks",
#     "removeoffline",
#     "idclip",
#     "id",
#     "stream",
#     "editembed",
#     "sticker",
#     "rolecheck",
#     "viewoffline",
#     "repost",
#     "fastclip3",
#     "fastclip2",
#     "speak",
#     "speak2",
#     "load",
#     "reload",
#     "unload",
#     "checkhelp"
# ]

with open("modules/commands.json") as f:
    data = json.load(f)
    hidden_commands = data["hidden"]


class Events(commands.Cog):
    def __init__(self, client, start_time, log):
        self.client = client
        self.start_time = start_time
        self.log = log

    @commands.Cog.listener()
    async def on_ready(self):

        print(
            f"\033[92m{(time.time() - self.start_time):.2f}s - We have logged in as {self.client.user}\033[0m"
        )
        await self.log("Bot started", False)
        #  await client.change_presence(activity=discord.Game(name="sus gaming | k.help"))
        avi_guild = self.client.get_guild(603147860225032192)
        while avi_guild == None:
            avi_guild = self.client.get_guild(603147860225032192)
        else:
            print(avi_guild)
            avibot = avi_guild.get_member(855897776125640704)
            while avibot == None:
                avibot = avi_guild.get_member(855897776125640704)
            else:
                if avibot.status is disnake.Status.offline:
                    print("avibot ded")
                    await self.log("avi bot ded", False)
                    # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
                    # msg_id = 887707057808085042
                    # msg = await channel.fetch_message(msg_id)
                    vc = self.client.get_guild(603147860225032192).get_channel(
                        887717074191937667
                    )
                    # await msg.edit(content="avi bot dead temporarily. password no work. so tell them that as well.")
                    # staffch = client.get_guild(603147860225032192).get_channel(812666568613167125)
                    await vc.edit(name="AviBot: dead")
                # await staffch.send('<@97122523086340096> bot ded')
                if avibot.status is disnake.Status.online:
                    print("avi bot bac")
                    await self.log("avi bot bac", False)
                    # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
                    # msg_id = 887707057808085042
                    # msg = await channel.fetch_message(msg_id)
                    vc = self.client.get_guild(603147860225032192).get_channel(
                        887717074191937667
                    )
                    # await msg.edit(content="AviBot is online. (ignore this)")
                    await vc.edit(name="AviBot: alive")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if (
            before.status is disnake.Status.online
            and after.status is disnake.Status.offline
            and after.guild == self.client.get_guild(603147860225032192)
        ):
            if after.id == 855897776125640704:
                print(after.id)
                print("avi bot ded")
                await self.log("avi bot ded", False)
                # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
                #  msg_id = 887707057808085042
                # msg = await channel.fetch_message(msg_id)
                vc = self.client.get_guild(603147860225032192).get_channel(
                    887717074191937667
                )
                # await msg.edit(content="avi bot dead temporarily. password no work. so tell them that as well.")
                # staffch = client.get_guild(603147860225032192).get_channel(812666568613167125)
                await vc.edit(name="AviBot: dead")
                # await staffch.send('<@97122523086340096> bot ded')
        elif (
            before.status is disnake.Status.offline
            and after.status is disnake.Status.online
        ):
            if after.id == 855897776125640704:
                print(after.id)
                print("avi bot bac")
                await self.log("avi bot bac", False)
                # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
                # msg_id = 887707057808085042
                # msg = await channel.fetch_message(msg_id)
                vc = self.client.get_guild(603147860225032192).get_channel(
                    887717074191937667
                )
                # await msg.edit(content="AviBot is online. (ignore this)")
                await vc.edit(name="AviBot: alive")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        msg = message.content.lower()

        ################SUSSY REPLIES##################

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
                    if self.client.sus_on == False:
                        await message.channel.send(
                            random.choice(sus_replies), delete_after=3.0
                        )
                        await self.log("sussy reply", False)
                    if self.client.sus_on:
                        await message.channel.send(random.choice(sus_replies))
                        await self.log("sussy reply", False)
            else:
                if "amgus" in msg:
                    await message.channel.send(
                        random.choice(sugma_replies), delete_after=3.0
                    )
                    await self.log("sussy reply", False)
                if "amogus" in msg:
                    await message.channel.send(
                        random.choice(sugoma_replies), delete_after=3.0
                    )
                    await self.log("sussy reply", False)
                if "sushi" in msg:
                    await message.channel.send(
                        "remove the hi from sushi. what do you get? <:sus:850628234746920971>",
                        delete_after=3.0,
                    )
                    await self.log("sussy reply", False)
                if "pog" in msg:
                    await message.channel.send("poggusus", delete_after=3.0)
                    await self.log("sussy reply", False)

        #############TWITTER LINK GIVER####################

        if "twitter.com" in msg:
            # threads = []
            links = re.findall("http.*twitter.com/.*/status/\d*", msg)
            print([x for x in links])
            for i in links:
                print("twitter link!")
                await self.log("twitter link!", False)
                args = ["yt-dlp", "-j", i]
                print(args)
                proc = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                )
                stdout_value = proc.stdout.read() + proc.stderr.read()
                # print(stdout_value.decode("utf-8"))
                try:
                    json_list = json.loads(stdout_value)
                except:
                    print("Nothing to load as JSON.")
                    return
                ext = json_list["ext"]
                webpageurl = json_list["webpage_url"]
                print(ext)
                if ext == "mp4" and "twitter.com" in webpageurl:
                    m1 = await message.channel.send(
                        "Beep boop! That is a twitter video!\nImma give direct video link..."
                    )
                    await self.log("twitter video!", False)

                    msg = await message.channel.send(json_list["url"])
                    await asyncio.sleep(3)
                    # if not msg.embeds:
                    #     await m1.edit(content="No embeds. Trying to manually upload...")
                    #     r = requests.get(json_list["url"])
                    #     # print(r.content)
                    #     vid = io.BytesIO(r.content)
                    #     filename = json_list["url"].split("/")[-1].split("?")[0]
                    #     await message.channel.send(
                    #         file=disnake.File(vid, filename=filename)
                    #     )
                    await m1.delete()

        ######################TEXT TO SPEECH#################

        if msg.startswith("] "):
            voice_channel = message.author.voice.channel
            await self.log("] command used", True)
            tts = gTTS(msg)
            with open("sounds/tts.mp3", "wb") as f:
                tts.write_to_fp(f)
            voice = disnake.utils.get(self.client.voice_clients, guild=message.guild)
            if voice_channel != None:

                if voice == None:
                    vc = await voice_channel.connect()
                    vc.play(disnake.FFmpegPCMAudio(source="sounds/tts.mp3"))
                else:
                    voice.play(disnake.FFmpegPCMAudio(source="sounds/tts.mp3"))
        if msg.startswith("]au "):
            await self.log("]au command used", True)
            voice_channel = message.author.voice.channel

            tts = gTTS(msg[3:], lang="en", tld="com.au")
            with open("sounds/tts.mp3", "wb") as f:
                tts.write_to_fp(f)
            voice = disnake.utils.get(self.client.voice_clients, guild=message.guild)
            if voice_channel != None:

                if voice == None:
                    vc = await voice_channel.connect()
                    vc.play(disnake.FFmpegPCMAudio(source="sounds/tts.mp3"))
                else:
                    voice.play(disnake.FFmpegPCMAudio(source="sounds/tts.mp3"))
        if msg.startswith("]uk "):
            await self.log("]uk command used", True)
            voice_channel = message.author.voice.channel

            tts = gTTS(msg[3:], lang="en", tld="co.uk")
            with open("sounds/tts.mp3", "wb") as f:
                tts.write_to_fp(f)
            voice = disnake.utils.get(self.client.voice_clients, guild=message.guild)
            if voice_channel != None:

                if voice == None:
                    vc = await voice_channel.connect()
                    vc.play(disnake.FFmpegPCMAudio(source="sounds/tts.mp3"))
                else:
                    voice.play(disnake.FFmpegPCMAudio(source="sounds/tts.mp3"))
        if msg.startswith("]in "):
            await self.log("]in command used", True)
            voice_channel = message.author.voice.channel

            tts = gTTS(msg[3:], lang="en", tld="co.in")
            with open("sounds/tts.mp3", "wb") as f:
                tts.write_to_fp(f)
            voice = disnake.utils.get(self.client.voice_clients, guild=message.guild)
            if voice_channel != None:

                if voice == None:
                    vc = await voice_channel.connect()
                    vc.play(disnake.FFmpegPCMAudio(source="sounds/tts.mp3"))
                else:
                    voice.play(disnake.FFmpegPCMAudio(source="sounds/tts.mp3"))

        ########################FRIDAY IN CALIFORNIA#########################
        if "friday" in msg:
            tz = pytz.timezone("America/Los_Angeles")
            curr_time = datetime.now(tz)
            day = curr_time.strftime("%A")
            if day == "Friday":
                print("It is Friday... in California. SHOOT!")
                await message.channel.send(file=disnake.File("videos/friday.webm"))

        if any(word in msg for word in ["deez", "deez nuts"]):
            await message.channel.send(random.choice(deez_replies), delete_after=3.0)

    ################################ON_COMMAND_ERROR#############
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
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
            commandss = [
                c.name for c in self.client.commands if c.name not in hidden_commands
            ]
            print(commandss)
            similar = difflib.get_close_matches(err[1], commandss)
            if similar:
                await ctx.send(
                    f"bruh. there's no '{err[1]}' command.\ndid you mean:\n`{', '.join(similar)}`?"
                )
            else:
                await ctx.send(f"bruh. there's no '{err[1]}' command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            command = self.client.get_command(f"help {ctx.command}")
            ctx.command = command
            ctx.invoked_subcommand = command
            await self.client.invoke(ctx)
        elif isinstance(error, commands.NotOwner):
            await ctx.send(
                "Bruh, how'd you find this command? Only Kur0 can use this tho lmao."
            )
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, disnake.NotFound):
                await ctx.send(
                    "404 moment. I dunno what you just did but I can't find something. Automod deleted it perhaps? Maybe it doesn't actually exist? Maybe it's a bug lol."
                )
            elif isinstance(error.original, disnake.HTTPException):
                print("HTTPException!")
                if error.original.status == 429:
                    print("Rate limited lmao")
                    os.system("busybox reboot")
                elif error.original.status == 413:
                    print("File too big!")
                    await ctx.send(
                        "Your server isn't strong enough to handle the size of the file I'm sending <a:trollplant:934777423881445436>"
                    )
                else:
                    await ctx.send(error.original)
                await self.log(error.original, False)
            elif isinstance(error.original, disnake.ClientException):   
                if str(error.original) == "Already playing audio.":
                    await ctx.send("I'm still playing smth rn bruh. Hold on.",delete_after=3)
                else:
                    await ctx.send(error.original)                    
            else:
                await ctx.send(error.original)
        else:
            print(f"ERROR: {error}")
            # print(dir(error))
            for i in dir(error):
                if not str(i).startswith("_"):
                    print(f"{i}: {getattr(error,i)}\n")
            print(f"invoked command: {ctx.command}")
            await ctx.send(error)
        await self.log(error, False)
        raise error  # re-raise the error so all the errors will still show up in console


# def setup(client,start_time,log):
#     client.add_cog(Events(client,start_time,log))

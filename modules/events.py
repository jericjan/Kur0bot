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
                    vc = self.client.get_guild(603147860225032192).get_channel(
                        887717074191937667
                    )
                    await vc.edit(name="AviBot: dead")
                if avibot.status is disnake.Status.online:
                    print("avi bot bac")
                    await self.log("avi bot bac", False)

                    vc = self.client.get_guild(603147860225032192).get_channel(
                        887717074191937667
                    )
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
                vc = self.client.get_guild(603147860225032192).get_channel(
                    887717074191937667
                )
                await vc.edit(name="AviBot: dead")
        elif (
            before.status is disnake.Status.offline
            and after.status is disnake.Status.online
        ):
            if after.id == 855897776125640704:
                print(after.id)
                print("avi bot bac")
                await self.log("avi bot bac", False)
                vc = self.client.get_guild(603147860225032192).get_channel(
                    887717074191937667
                )
                await vc.edit(name="AviBot: alive")

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        new_user_activities = after.activities
        id_list = []
        game_names = []
        game_names.append("Mobile Legends: Bang Bang")
        id_list.append(588739191433723914)  # mobile_legends
        game_names.append("League of Legends")
        id_list.append(401518684763586560)  # league
        game_names.append("Honkai Impact 3rd")
        game_names.append("honka donka badonkers")
        id_list.append(604089691519713300)  # honkai 3rd
        game_names.append("Honkai Impact 3")
        id_list.append(614393437030187008)  # honkai 3
        game_names.append("Genshin Impact")
        id_list.append(762434991303950386)  # genshin
        if new_user_activities:
            for activity in new_user_activities:
                if str(activity.type) == "ActivityType.playing" and after.bot == False:
                    try:
                        game_id = activity.application_id
                    except:
                        game_id = "UNKNOWN"
                    with open("activities.txt", "a") as f:
                        f.write(
                            f"({game_id}) [{after.guild}] {after.name}: started playing {activity.name}"
                        )
                    if game_id in id_list or activity.name in game_names:
                        hall_of_shame_json = json.load(
                            open("modules/others/hall_of_shame_ids.json")
                        )
                        try:
                            hall_of_shame_channel_id = hall_of_shame_json[
                                str(after.guild.id)
                            ]["channel-id"]
                            hall_of_shame_embed_id = hall_of_shame_json[
                                str(after.guild.id)
                            ]["embed-id"]
                            hall_of_shame_channel = await self.client.fetch_channel(
                                hall_of_shame_channel_id
                            )
                            hall_of_shame = await hall_of_shame_channel.fetch_message(
                                hall_of_shame_embed_id
                            )
                            if after.guild == hall_of_shame.guild:
                                em = hall_of_shame.embeds[0]
                                name_list = [i.name for i in em.fields]
                                try:
                                    start_time = (
                                        f"<t:{round(activity.start.timestamp())}:R>"
                                    )
                                except:
                                    start_time = "at an unknown time"
                                value = f"{after.mention} opened **{activity.name}** {start_time}"
                                name = after.name
                                if name in name_list:
                                    index = name_list.index(name)
                                    em.remove_field(index)
                                em.add_field(name=name, value=value, inline=False)
                                while len(name_list) > 10:
                                    em.remove_field(0)
                                    name_list = [i.name for i in em.fields]
                                await hall_of_shame.edit(embed=em)
                        except Exception as e:
                            print(
                                f"UNSET: ({game_id}) [{after.guild}] {after.name}: started playing {activity.name}\n{e}"
                            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        msg = message.content.lower()

        ################SUSSY REPLIES##################
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

        if isinstance(error, commands.CommandInvokeError):
            error = error.original
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
        elif isinstance(error, commands.BotMissingPermissions):
            missing_perms = [f"**{x}**" for x in error.missing_permissions]
            try:
                await ctx.send(
                    f"Doktor, turn off my {' and '.join(missing_perms)} inhibitors"
                )
            except:
                await ctx.author.send(
                    f"Doktor, turn off my {' and '.join(missing_perms)} inhibitors"
                )
        # elif isinstance(error, commands.CommandInvokeError):

        # CCCCCCCVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
        elif isinstance(error, disnake.NotFound):
            await ctx.send(
                "404 moment. I dunno what you just did but I can't find something. Automod deleted it perhaps? Maybe it doesn't actually exist? Maybe it's a bug lol."
            )
        elif isinstance(error, disnake.HTTPException):
            print("HTTPException!")
            if error.status == 429:
                print("Rate limited lmao")
                os.system("busybox reboot")
            elif error.status == 413:
                print("File too big!")
                await ctx.send(
                    "Your server isn't strong enough to handle the size of the file I'm sending <a:trollplant:934777423881445436>"
                )

            elif error.status == 403:  # Forbidden
                if error.code == 50013:  # missing permissions
                    responses = [
                        "I NEED MORE POWER! By that I mean permissions. I don't have enough permissions. What's up with that bruh.",
                        "Doktor, turn off my permission inhibitors! I don't have enough permissions to do the thing you want me to do. Yeah, You gotta give me it. ",
                    ]
                    traceback = error.__traceback__
                    log_thing = ""
                    while traceback.tb_next:
                        filename = traceback.tb_frame.f_code.co_filename
                        line_no = traceback.tb_lineno
                        if filename.startswith("/home/kur0/Kur0bot"):
                            log_thing += f"{filename}:{line_no}\n"
                            with open(filename) as f:
                                for pos, line in enumerate(f):
                                    if pos + 1 == int(line_no):
                                        log_thing += f"{line}\n"
                                        break
                        traceback = traceback.tb_next
                    message = random.choice(responses)
                    await ctx.send(f"{message}\n```\n{log_thing}```")
                elif error.code == 50001:  # missing access
                    await ctx.author.send(
                        "Yo dawg. I can't acess that channel/thread. Give me perms bruv."
                    )
                else:
                    await ctx.send(error)
            else:
                await ctx.send(error)
            await self.log(error, False)
        elif isinstance(error, disnake.ClientException):
            if str(error) == "Already playing audio.":
                await ctx.send(
                    "I'm still playing smth rn bruh. Hold on.", delete_after=3
                )
            else:
                await ctx.send(error)
                # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        else:
            print(f"ERROR: {error}")
            for i in dir(error):
                if not str(i).startswith("_"):
                    print(f"{i}: {getattr(error,i)}\n")
            print(f"invoked command: {ctx.command}")
            await ctx.send(error)
        await self.log(error, False)
        raise error  # re-raise the error so all the errors will still show up in console

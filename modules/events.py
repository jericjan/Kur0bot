import asyncio
import difflib
import json
import os
import random
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

import disnake
import numpy
import pytz
from disnake.ext import commands
from gtts import gTTS

from myfunctions.async_wrapper import async_wrap

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
    def __init__(self, client):
        self.client = client
        self.start_time = self.client.start_time
        self.log = self.client.log

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.loop.set_debug(True)
        print(
            f"\033[92m{(time.time() - self.start_time):.2f}s - We have logged in as {self.client.user}\033[0m"
        )
        await self.log("Bot started", False)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        @async_wrap
        def load_json():
            return json.load(open("modules/others/hall_of_shame_ids.json"))

        @async_wrap
        def log_activity(game_id, guild, name, activity_name):
            with open("activities.txt", "a") as f:
                f.write(
                    f"({game_id}) [{guild}] {name}: started playing {activity_name}"
                )

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

        game_names.append("Honkai: Star Rail")

        game_names.append("Genshin Impact")
        id_list.append(762434991303950386)  # genshin

        game_names.append("Destiny 2")
        if new_user_activities:
            for activity in new_user_activities:
                if str(activity.type) == "ActivityType.playing" and after.bot == False:
                    try:
                        game_id = activity.application_id
                    except:
                        game_id = "UNKNOWN"

                    await log_activity(game_id, after.guild, after.name, activity.name)

                    if game_id in id_list or activity.name in game_names:
                        hall_of_shame_json = await load_json()
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
                            pass
                            # print(
                            # f"UNSET: ({game_id}) [{after.guild}] {after.name}: started playing {activity.name}\n{e}"
                            # )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        msg = message.content.lower()

        if message.channel.id == 1203784333341491302:
            return  # temp, disabled for #serious-chat

        ################SUSSY REPLIES##################
        if message.channel.id == 850380119646142504:  # sus-town
            if any(word in msg for word in sus_words):
                for x in range(3):
                    await message.channel.send(random.choice(sus_replies))
        else:
            if any(word in msg for word in sus_words):
                if self.client.sus_on == False:
                    await message.channel.send(
                        random.choice(sus_replies), delete_after=3.0
                    )
                    await self.log("sussy reply", False)
                if self.client.sus_on:
                    await message.channel.send(random.choice(sus_replies))
                    await self.log("sussy reply", False)
        if "amgus" in msg:
            await message.channel.send(random.choice(sugma_replies), delete_after=3.0)
            await self.log("sussy reply", False)
        if "amogus" in msg:
            await message.channel.send(random.choice(sugoma_replies), delete_after=3.0)
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

        # le strepto
        if any(
            word in msg
            for word in ["feet", "foot", "toe", "ankle", "heel", "arch", "sole"]
        ):
            strepto_in_server = await message.guild.getch_member(268188421871108097)
            if strepto_in_server:
                await message.channel.send("<@268188421871108097>")  # pings strepto

        # PACIFAM ONLY
        pacifam_servers = [603147860225032192, 938255956247183451]
        if any([message.guild.id == x for x in pacifam_servers]):
            if "dox" in msg:
                choice = random.choice(
                    [
                        "videos/professional_doxxers.mp4",
                        "images/allen_quote.png",
                        "images/dex_quote.png",
                    ]
                )
                await message.channel.send(file=disnake.File(choice))
            if any(word in msg for word in ["hurensohn", "hurensöhne"]):
                peeps = ["304268898637709312", "1200519236834041898"]
                await message.channel.send(
                    f"<@{random.choice(peeps)}>"
                )  # pings strepto
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

        if "wednesday" in msg:
            tz_str_list = [
                "Etc/GMT+12",
                "Etc/GMT-14",
                "Etc/GMT-12",
            ]  # signs are opposite for some reason
            tz_day_list = [
                datetime.now(pytz.timezone(x)).strftime("%A") for x in tz_str_list
            ]

            if "Wednesday" in tz_day_list:
                today = datetime.now(pytz.timezone("Etc/GMT+12"))
                thursday = datetime(
                    today.year,
                    today.month,
                    today.day + ((3 - today.weekday()) % 7),
                    tzinfo=pytz.timezone("Etc/GMT+12"),
                )
                epoch = int(thursday.timestamp())

                wed_vids = [
                    Path("videos/mococo") / x
                    for x in [
                        "mococo_wednesday.mp4",
                        "mococo_679.mp4",
                        "fuwamoco_tsunami.mp4",
                        "bau_city.mp4",
                        "fuwamoco_family_ties.mp4",
                        "fuwamoco_silent_hill.mp4",
                    ]
                ] + [Path("videos/wednesday.mp4")]

                wed_choice = numpy.random.choice(
                    wed_vids, p=[0.8, 0.037, 0.037, 0.037, 0.037, 0.037, 0.015]
                )

                if wed_choice.parent.name == "mococo":
                    epoch = f"Mococo Wednesday ends <t:{epoch}:R>"
                else:
                    epoch = f"Moco... SIKE! Walter Wednesday ends <t:{epoch}:R>"

                await message.channel.send(epoch, file=disnake.File(str(wed_choice)))

        if any(word in msg for word in ["10:49pm", "10:49 pm", "10 49 pm", "10 49pm"]):
            await message.channel.send(file=disnake.File("videos/10_49_pm.mp4"))

        if any(word in msg for word in ["deez", "deez nuts"]):
            await message.channel.send(random.choice(deez_replies), delete_after=3.0)

        if "reaction" in msg:
            await message.channel.send(
                "https://tenor.com/view/kronii-hololive-edoman-3d-anime-gif-2423112144377621699"
            )

        if "crazy" in msg:
            await message.channel.send("Crazy?")

        if "wah" in msg:
            await message.channel.send(file=disnake.File("videos/wah.mp4"))

        if "balls" in msg:
            await message.channel.send(file=disnake.File("videos/the_balls.mp4"))

        if any(word in msg for word in ["fuck you tatsu", "fuck off tatsu"]):
            async for x in message.channel.history(limit=10):
                if x.author.id == 172002275412279296:
                    await x.delete()
                    break

        if "jdon my soul" in msg:
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/809247468084133898/1219821713752330351/GJCNx-HaIAAlZiz.png"
            )

    def get_full_class_name(self, obj):
        module = obj.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return obj.__class__.__name__
        return module + "." + obj.__class__.__name__

    ################################ON_COMMAND_ERROR#############
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx, "_ignore_me_"):
            return

        def full_error(err):
            return f"{self.get_full_class_name(err)}: {err}"

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
            commands_with_help_msg = [
                c.name for c in self.client.get_command("help").commands
            ]
            print("Missing req arg")
            await ctx.send(f"missing argument `{error.param}`, g")
            command = self.client.get_command(f"help {ctx.command}")
            ctx.command = command
            ctx.invoked_subcommand = command
            if ctx.command.name in commands_with_help_msg:
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
                    await ctx.send(full_error(error))
            else:
                await ctx.send(full_error(error))
            await self.log(error, False)
        elif isinstance(error, disnake.ClientException):
            if str(error) == "Already playing audio.":
                await ctx.send(
                    "I'm still playing smth rn bruh. Hold on.", delete_after=3
                )
            else:
                await ctx.send(full_error(error))
                # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        else:
            print(f"ERROR: {error}")
            for i in dir(error):
                if not str(i).startswith("_"):
                    print(f"{i}: {getattr(error,i)}\n")
            print(f"invoked command: {ctx.command}")
            await ctx.send(full_error(error))
        await self.log(error, False)
        raise error  # re-raise the error so all the errors will still show up in console

    ################################ON_SLASH_COMMAND_ERROR#############
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        await inter.followup.send(f"{self.get_full_class_name(error)}: {error}")


def setup(client):
    client.add_cog(Events(client))

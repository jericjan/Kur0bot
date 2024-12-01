import asyncio
import difflib
import json
import os
import random
import re
import subprocess
import time
from datetime import datetime, timedelta, timezone
from operator import attrgetter
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

deez_replies = [
    "can i put my balls in yo jaws",
    "ong fr?",
    "ligma",
    "updog",
    "my name jef",
]


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.start_time = self.client.start_time
        self.log = self.client.log

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.loop.set_debug(True)
        print(
            f"\033[92m{(time.time() - self.start_time):.2f}s - We have logged in as "
            f"{self.client.user}\033[0m"
        )
        await self.log("Bot started", False)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        @async_wrap
        def load_json():
            with open("modules/others/hall_of_shame_ids.json", encoding="utf-8") as f:
                res = json.load(f)
            return res

        @async_wrap
        def log_activity(game_id, guild, name, activity_name):
            with open("activities.txt", "a", encoding="utf-8") as f:
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
                if str(activity.type) == "ActivityType.playing" and not after.bot:
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
                        except:
                            pass
                            # print(
                            # f"UNSET: ({game_id}) [{after.guild}] {after.name}: "
                            # "started playing {activity.name}\n{e}"
                            # )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        msg = message.content.lower()

        if any(
            message.channel.id == x for x in [1203784333341491302, 1210328711455440926]
        ):
            return  # temp, disabled for #serious-chat

        motor = self.client.get_cog("MotorDbManager")

        toggles = motor.get_collection_for_server("toggles", message.guild.id)

        stats_cog = self.client.get_cog("Stats")
        user_stat = stats_cog.get_user(message.guild.id, message.author.id)

        ################SUSSY REPLIES##################
        if message.channel.id == 850380119646142504:  # sus-town
            if any(word in msg for word in sus_words):
                for x in range(3):
                    await user_stat.increment("Sussy replies", 1)
                    await message.channel.send(random.choice(sus_replies))
        else:
            if any(word in msg for word in sus_words):
                await user_stat.increment("Sussy replies", 1)
                if not self.client.sus_on:
                    await message.channel.send(
                        random.choice(sus_replies), delete_after=3.0
                    )
                    await self.log("sussy reply", False)
                if self.client.sus_on:
                    await message.channel.send(random.choice(sus_replies))
                    await self.log("sussy reply", False)

        other_sus_dict = {
            "amgus": random.choice(sugma_replies),
            "amogus": random.choice(sugoma_replies),
            "sushi": "remove the hi from sushi. what do you get? <:sus:850628234746920971>",
            "pog": "poggusus",
        }

        for target_word, response in other_sus_dict.items():
            if target_word in msg:
                await user_stat.increment("Sussy replies", 1)
                await message.channel.send(response, delete_after=3.0)
                await self.log("sussy reply", False)

        # le strepto
        if all(message.channel.id != x for x in [1260889287931723839]):
            if any(
                word in msg
                for word in [
                    "feet",
                    "foot",
                    "toe",
                    "ankle",
                    "heel",
                    "arch",
                    "sole",
                    "🦶",
                ]
            ):
                strepto_in_server = await message.guild.getch_member(268188421871108097)
                if strepto_in_server:
                    await user_stat.increment("Feet-related", 1)

                    days_list = self.client.get_cog("TimeAndDates").get_current_days(
                        show_date=False
                    )

                    strepto_ping = "<@268188421871108097>"

                    if "Friday" in days_list:
                        strepto_ping += (
                            "\nhttps://cdn.discordapp.com/attachments/809247468084133898/"
                            "1231538142129946715/20240420_183246.png"
                        )

                    await message.channel.send(strepto_ping)  # pings strepto

        if re.search(r"blue.archive", msg):
            await user_stat.increment("Blue Archive mentioned", 1)
            user_id = 480466417884463137
            kyle_in_server = await message.guild.getch_member(user_id)
            if kyle_in_server:
                await message.channel.send(f"<@{user_id}>")

        if re.search(r"(?:fkn|fucking) hell", msg):
            await user_stat.increment("Hell fucking", 1)
            user_id = 327595393237909505
            in_server = await message.guild.getch_member(user_id)
            if in_server:
                await message.channel.send(f"They're fucking <@{user_id}>")

        if all(word in msg for word in ["blue archive", "cunny", "uoh", "sui"]):
            user_id = 1009325079336853515
            in_server = await message.guild.getch_member(user_id)
            if in_server:
                await user_stat.increment("The Magic Kakuy Spell", 1)
                await message.channel.send(
                    f"You've uttered the Magic Kakuy Spell! <@{user_id}> will remember this..."
                )
        # PACIFAM ONLY
        pacifam_servers = [603147860225032192, 938255956247183451]
        if any(message.guild.id == x for x in pacifam_servers):
            if "dox" in msg:
                choice = random.choice(
                    [
                        "videos/professional_doxxers.mp4",
                        "images/allen_quote.png",
                        "images/dex_quote.png",
                    ]
                )
                await user_stat.increment("Doxx", 1)
                await message.channel.send(file=disnake.File(choice))
            if any(word in msg for word in ["hurensohn", "hurensöhne"]):
                await user_stat.increment("Hurensohn", 1)
                await message.channel.send("<@1200519236834041898>")  # pings nana
        #############TWITTER LINK GIVER####################
        twt_links = re.findall(r"(?:https://(?:www\.)?)(?:x|twitter)(?:\.com\S+)", msg)
        resp = [f"Fixed some twitter links for ya:\n"]
        for idx, link in enumerate(twt_links):
            if idx == 0:
                resp[0] += re.sub(
                    r"(https://(?:www\.)?)(x|twitter)(?=\.com\S+)", r"\1fixvx", link
                )
            else:
                resp.append(
                    re.sub(
                        r"(https://(?:www\.)?)(x|twitter)(?=\.com\S+)", r"\1fixvx", link
                    )
                )
        if twt_links:
            for x in resp:
                await message.channel.send(x)

        ######################TEXT TO SPEECH#################

        if msg.startswith("] "):
            voice_channel = message.author.voice.channel
            await self.log("] command used", True)
            tts = gTTS(msg)
            with open("sounds/tts.mp3", "wb") as f:
                tts.write_to_fp(f)
            voice = disnake.utils.get(self.client.voice_clients, guild=message.guild)
            if voice_channel is not None:

                if voice is None:
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
            if voice_channel is not None:

                if voice is None:
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
            if voice_channel is not None:

                if voice is None:
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
            if voice_channel is not None:

                if voice is None:
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
                await user_stat.increment("Friday in California", 1)
                await message.channel.send(file=disnake.File("videos/friday.webm"))

        if "wednesday" in msg:
            get_days, get_boundary, to_timestamp = attrgetter(
                "get_current_days", "get_date_boundary", "tz_to_discord_timestamp"
            )(self.client.get_cog("TimeAndDates"))

            tz_day_list = get_days(show_date=False)

            if "Wednesday" in tz_day_list:
                day_ends = get_boundary("end", weekday="thursday")
                epoch = to_timestamp(day_ends)

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
                    epoch = f"Mococo Wednesday ends {epoch}"
                    await user_stat.increment("Wednesday.Mococo", 1)
                else:
                    epoch = f"Moco... SIKE! Walter Wednesday ends {epoch}"
                    await user_stat.increment("Wednesday.Walter", 1)

                await message.channel.send(epoch, file=disnake.File(str(wed_choice)))

        if any(word in msg for word in ["10:49pm", "10:49 pm", "10 49 pm", "10 49pm"]):
            await user_stat.increment("10:49 pm", 1)
            await message.channel.send(file=disnake.File("videos/10_49_pm.mp4"))

        if any(word in msg for word in ["deez", "deez nuts"]):
            await user_stat.increment("Deez Nuts", 1)
            await message.channel.send(random.choice(deez_replies), delete_after=3.0)

        if all(message.channel.id != x for x in [1260889287931723839]):
            if "reaction" in msg:
                await user_stat.increment("Kronii Reaction", 1)
                await message.channel.send(
                    "https://tenor.com/view/kronii-hololive-edoman-3d-anime-gif-2423112144377621699"
                )

        if "crazy" in msg:
            await user_stat.increment("Crazy", 1)
            await message.channel.send("Crazy?")

        if "wah" in msg:
            await user_stat.increment("Wah", 1)
            await message.channel.send(file=disnake.File("videos/wah.mp4"))

        if "balls" in msg:
            idx, file = random.choice(
                [(0, "videos/the_balls.mp4"), (1, "videos/testicle-zap.mp4")]
            )
            if idx == 0:
                await user_stat.increment("The Balls", 1)
            elif idx == 1:
                await user_stat.increment("Testicle Zap", 1)
            await message.channel.send(file=disnake.File(file))

        tatsu_id = 172002275412279296

        if any(word in msg for word in ["fuck you tatsu", "fuck off tatsu"]):
            if message.reference is not None:
                if message.reference.resolved.author.id == tatsu_id:
                    await user_stat.increment("Tatsu bot murders", 1)
                    await message.reference.resolved.delete()
            else:
                async for x in message.channel.history(limit=10):
                    if x.author.id == tatsu_id:
                        await user_stat.increment("Tatsu bot murders", 1)
                        await x.delete()
                        break

        if message.reference is not None:
            if message.reference.resolved.author.id == tatsu_id:
                gpt_resp = ""
                while gpt_resp != "True" and gpt_resp != "False":
                    gpt_msg = f"Is the following phrase offensive? respond ONLY with True or False:\n{message.content}"
                    gpt_resp = self.client.get_cog("OpenAI").prompt(gpt_msg)
                if gpt_resp == "True":
                    await user_stat.increment("Tatsu bot murders", 1)
                    await message.reference.resolved.delete()

        if "jdon my soul" in msg:
            await user_stat.increment("JdonMySoul", 1)
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/809247468084133898/1219821713752330351/GJCN"
                "x-HaIAAlZiz.png"
            )

        if any(word in msg for word in ["stuff", "🥙"]):
            await user_stat.increment("Stuff react", 1)
            emote_server = await self.client.fetch_guild(1034100571667447860)
            stuff = await emote_server.fetch_emoji(1235625865090437252)
            await message.add_reaction(stuff)

        if "cunny" in msg or re.search("uo+h", msg):
            await user_stat.increment("Cunny react", 1)
            await message.add_reaction("😭")
            await message.add_reaction("💢")

        im_pattern = re.compile(
            r"\b(i(?:‘|’|')m|im|i am) (.*?)(?=(?:\b\1\b|$|\n|\.|,|\?|!))"
        )
        """ 
        It should match like this:
        i‘m dead. [dead]
        i’m dead! [dead]
        i'm dead? [dead]
        i'm dead; or maybe not [dead; or maybe not]
        i'm killing myself, rn i am sad [killing myself] [sad]
        i'm dead [dead]
        im impressed [impressed]
        im him [him]
        imposter []
        jimmy []
        """


        trollplant = "<a:trollplant:934777423881445436>"

        dad_jokes = await toggles.find_one({"title": "Dad Jokes"})

        if (dad_jokes is None or dad_jokes.get("enabled")) and im_pattern.search(msg):
            victim_db = motor.get_collection_for_server(
                "dad_joke_victims", message.guild.id
            )

            async def new_victim():
                user_list = [x for x in message.guild.members if not x.bot]
                victim_id = random.choice(user_list).id
                victim_notified = False

                print(f"New victim is: {victim_id}")
                if victim_id == message.author.id:
                    await message.channel.send(
                        f"Hey there {message.author.mention}, you appear to be my latest victim"
                        f" for today! {trollplant*3}"
                    )
                    await user_stat.increment("Victimized", 1)
                    victim_notified = True

                user_dic = {"user_id": victim_id, "notified": victim_notified}
                await victim_db.insert_one(user_dic)
                return user_dic

            if await victim_db.count_documents({}) == 0:
                victim = await new_victim()
            else:
                victim = await motor.get_latest_doc(victim_db)
                victim_id = victim["user_id"]

                print(f"Existing victim id is: {victim_id}")
                time_since = victim["_id"].generation_time
                time_difference = datetime.now(timezone.utc) - time_since
                if time_difference >= timedelta(hours=24):
                    print("New victim time!")
                    victim = await new_victim()

            respond_with_dad_joke = numpy.random.choice([True, False], p=[0.1, 0.9])

            if respond_with_dad_joke or message.author.id == victim["user_id"]:

                if message.author.id == victim["user_id"] and not victim["notified"]:
                    await message.channel.send(
                        f"Yo {message.author.mention}, you're a little late but, you're my latest"
                        f" victim for today! {trollplant*3}"
                    )
                    await user_stat.increment("Victimized", 1)
                    await victim_db.update_one(
                        {"_id": victim["_id"]}, {"$set": {"notified": True}}
                    )

                results = im_pattern.findall(msg)
                results = [f"**{x[1].strip()}**" for x in results if x[1].strip() != ""]
                names = " AKA ".join(results)
                if len(results) == 0:
                    response = (
                        "You're WHAT? What the fuck are you trying to say, you doofus."
                    )
                else:
                    response = f"hi {names}, i'm kur0 sus bot! {trollplant}"

                await user_stat.increment("Im Sus Bot", 1)
                await message.channel.send(response)

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
                f"Ayo this command is on cooldown.\nWait for {error.retry_after:.2f}s to try it "
                "again.",
                delete_after=3.0,
            )
            await ctx.message.delete()
            print(dir(error))
            print(f"error: {error}\nerror args: {error.args}")
        elif isinstance(error, commands.CommandNotFound):
            err = str(error).split('"')

            with open("modules/commands.json", encoding="utf-8") as f:
                data = json.load(f)
                hidden_commands = data["hidden"]

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
            except Exception as e:
                print(f"missing perms: {e}")
                await ctx.author.send(
                    f"Doktor, turn off my {' and '.join(missing_perms)} inhibitors"
                )
        # elif isinstance(error, commands.CommandInvokeError):

        # CCCCCCCVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
        elif isinstance(error, disnake.NotFound):
            await ctx.send(
                "404 moment. I dunno what you just did but I can't find something. Automod deleted"
                " it perhaps? Maybe it doesn't actually exist? Maybe it's a bug lol."
            )
        elif isinstance(error, disnake.HTTPException):
            print("HTTPException!")
            if error.status == 429:
                print("Rate limited lmao")
                os.system("busybox reboot")
            elif error.status == 413:
                print("File too big!")
                await ctx.send(
                    "Your server isn't strong enough to handle the size of the file I'm sending"
                    "<a:trollplant:934777423881445436>"
                )

            elif error.status == 403:  # Forbidden
                if error.code == 50013:  # missing permissions
                    responses = [
                        "I NEED MORE POWER! By that I mean permissions. I don't have enough "
                        "permissions. What's up with that bruh.",
                        "Doktor, turn off my permission inhibitors! I don't have enough permissions"
                        " to do the thing you want me to do. Yeah, You gotta give me it. ",
                    ]
                    traceback = error.__traceback__
                    log_thing = ""
                    while traceback.tb_next:
                        filename = traceback.tb_frame.f_code.co_filename
                        line_no = traceback.tb_lineno
                        if filename.startswith("/home/kur0/Kur0bot"):
                            log_thing += f"{filename}:{line_no}\n"
                            with open(filename, encoding="utf-8") as f:
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

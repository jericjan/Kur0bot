# followed this https://gist.github.com/15696/a1b10f044fbd658ce76ab1f862a1bda2
# client becomes self.client

import asyncio
import base64
import json
import os
import random
import time
import uuid
from io import BytesIO
from tempfile import NamedTemporaryFile

import aiohttp
import disnake
from disnake.ext import commands
from typing import Any

from myfunctions import subprocess_runner
from myfunctions.my_db import get_db


class Vc(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.dbname = get_db("music_queue")
        self.temp_servers_playing = {}
        self.song_now_playing = {}

    async def run_queue(self, ctx: commands.Context[Any]):
        try:
            server_queue = self.dbname[str(ctx.guild.id)]
            music_queue = server_queue.find().sort("epoch_time", 1)
            song_count = server_queue.count_documents({})
            if song_count != 0:
                print(f"THere is a queue {song_count}")
                first_epoch = [x["epoch_time"] for x in music_queue][0]
                print(f"first epoch is {first_epoch}")
                myquery = {"epoch_time": first_epoch}
                first_doc = server_queue.find_one(myquery)
                url = first_doc["url"]
                title = first_doc["title"]
                await self.pre_play(ctx, url, title)
                server_queue.delete_one(myquery)

            else:
                print("no mo queue")
                self.temp_servers_playing.pop(ctx.guild.id)
                self.song_now_playing.pop(ctx.guild.id)
                await ctx.send("Queue has ended")
        except KeyError:
            pass
        except Exception as e:

            def get_full_class_name(obj):
                module = obj.__class__.__module__
                if module is None or module == str.__class__.__module__:
                    return obj.__class__.__name__
                return module + "." + obj.__class__.__name__

            print(f"run_queue exception: {get_full_class_name(e)}: {e}")

    async def vcplay(self, ctx: commands.Context[Any], a, loop=None, is_random=None, **kwargs):

        voicestate = ctx.author.voice
        if voicestate:
            voice_channel = ctx.author.voice.channel
            can_connect = voice_channel.permissions_for(ctx.guild.me).connect
            can_speak = voice_channel.permissions_for(ctx.guild.me).speak

        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voicestate is not None:
            if voice is None:
                if can_connect and can_speak:
                    voice = await voice_channel.connect()
                else:
                    missing_perms = []
                    if not can_connect:
                        missing_perms.append("connect")
                    if not can_speak:
                        missing_perms.append("speak")
                    raise commands.BotMissingPermissions(missing_perms)
            if loop == "loop":

                def loop_func():
                    if is_random:
                        b = random.choice(a)
                        voice.play(
                            disnake.FFmpegPCMAudio(source=b),
                            after=lambda e: loop_func(),
                        )
                    else:

                        voice.play(
                            disnake.FFmpegPCMAudio(source=a),
                            after=lambda e: loop_func(),
                        )

                loop_func()
            else:
                if is_random:
                    a = random.choice(a)

                if "music_bot" in kwargs:
                    before_options = (
                        "-reconnect 1 -reconnect_at_eof 0 -reconnect_streamed 1 "
                        "-reconnect_delay_max 10 -copy_unknown"
                    )
                    voice.play(
                        disnake.FFmpegPCMAudio(source=a, before_options=before_options),
                        after=lambda e: asyncio.run_coroutine_threadsafe(
                            self.run_queue(ctx), self.client.loop
                        ),
                    )
                elif "file_obj" in kwargs:
                    print(f"file object is {type(a)}")
                    a.seek(0)
                    with NamedTemporaryFile() as fp:
                        fp.write(a.getbuffer())
                        fp.seek(0)
                        print(f"temp file is {fp.name}")
                        pcm_audio = disnake.FFmpegPCMAudio(source=fp.name)
                        pcm_audio.read()  # doesn't work without this
                        voice.play(pcm_audio)
                else:
                    voice.play(disnake.FFmpegPCMAudio(source=a))

        else:
            await ctx.send(
                f"{ctx.author.name} is not in a VC. Sending file instead...",
                delete_after=3,
            )

            if is_random:
                a = random.choice(a)
            print(f"playing {a}")

            if "custom_name" in kwargs:
                filename = kwargs["custom_name"]
            elif not isinstance(a, BytesIO):
                filename = a.split("/")[-1]
                print(f"filename is: {filename}")
                if a.split("/")[1] == "mgr":
                    speaker = a.split("/")[-2]
                    with open("modules/mgr_users.json", encoding="utf-8") as f:
                        mgr_json = json.load(f)
                    if speaker in mgr_json:
                        if isinstance(ctx.channel, disnake.TextChannel):
                            webhook = await ctx.channel.create_webhook(
                                name=mgr_json[speaker]["name"]
                            )
                            await webhook.send(
                                file=disnake.File(a, filename=filename),
                                username=mgr_json[speaker]["name"],
                                avatar_url=mgr_json[speaker]["pfp"],
                            )
                            await webhook.delete()
                        elif isinstance(ctx.channel, disnake.Thread):
                            webhook = await ctx.channel.parent.create_webhook(
                                name=mgr_json[speaker]["name"]
                            )
                            await webhook.send(
                                file=disnake.File(a, filename=filename),
                                username=mgr_json[speaker]["name"],
                                avatar_url=mgr_json[speaker]["pfp"],
                                thread=ctx.channel,
                            )
                            await webhook.delete()
                    elif filename in mgr_json:
                        if isinstance(ctx.channel, disnake.TextChannel):
                            webhook = await ctx.channel.create_webhook(
                                name=mgr_json[filename]["name"]
                            )
                            await webhook.send(
                                file=disnake.File(a, filename=filename),
                                username=mgr_json[filename]["name"],
                                avatar_url=mgr_json[filename]["pfp"],
                            )
                            await webhook.delete()
                        elif isinstance(ctx.channel, disnake.Thread):
                            webhook = await ctx.channel.parent.create_webhook(
                                name=mgr_json[filename]["name"]
                            )
                            await webhook.send(
                                file=disnake.File(a, filename=filename),
                                username=mgr_json[filename]["name"],
                                avatar_url=mgr_json[filename]["pfp"],
                                thread=ctx.channel,
                            )
                            await webhook.delete()
                    else:
                        await ctx.send(file=disnake.File(a, filename=filename))
                    return

            await ctx.send(file=disnake.File(a, filename=filename))
        # Delete command after the audio is done playing.
        if "dont_delete" not in kwargs:
            await ctx.message.delete()

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def join(self, ctx: commands.Context[Any]):
        voicestate = ctx.author.voice
        if voicestate:
            voice_channel = ctx.author.voice.channel
        else:
            await ctx.send("Brooo you're not even in a vc. Get in one bruh")
            return
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        can_connect = voice_channel.permissions_for(ctx.guild.me).connect
        can_speak = voice_channel.permissions_for(ctx.guild.me).speak
        if can_connect and can_speak:
            if not voice:
                await voice_channel.connect()
                await ctx.send("Sus bot has joined the call.", delete_after=3.0)
                await ctx.message.delete()
            elif ctx.guild.me.voice.channel == voice_channel:
                await ctx.send("I'm already in the VC! Zamn.", delete_after=3.0)
                await ctx.message.delete()
            else:
                await ctx.guild.voice_client.disconnect()
                await voice_channel.connect()
                await ctx.send("Sus bot has moved to this VC.", delete_after=3.0)
                await ctx.message.delete()
        else:
            missing_perms = []
            if not can_connect:
                missing_perms.append("connect")
            if not can_speak:
                missing_perms.append("speak")
            raise commands.BotMissingPermissions(missing_perms)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def stop(self, ctx: commands.Context[Any]):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Sus bot has been stopped.", delete_after=3.0)
        else:
            await ctx.send(
                "The bot is not playing anything at the moment.", delete_after=3.0
            )
        await ctx.message.delete()

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def stoploop(self, ctx: commands.Context[Any]):
        await ctx.guild.voice_client.disconnect()
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
        await ctx.send("The loop has been stopped.", delete_after=3.0)
        await ctx.message.delete()

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def leave(self, ctx: commands.Context[Any]):
        if ctx.voice_client:  # If the bot is in a voice channel
            await ctx.guild.voice_client.disconnect()  # Leave the channel
            await ctx.send("Sus bot has left the call.", delete_after=3.0)
            await ctx.message.delete()
        else:  # But if it isn't
            await ctx.send(
                "I'm not in a voice channel, use the join command to make me join",
                delete_after=3.0,
            )

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def letsgo(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/vibez-lets-go.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def vtubus(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/vtubus.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def giorno(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/giorno theme.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def ding(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(
            ctx, "sounds/DING DING DING DING DING DING DING DI DI DING.mp3", loop
        )

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def yodayo(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/Nakiri Ayame's yo dayo_.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def yodazo(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/Yo Dazo!.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def jonathan(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(
            ctx, "sounds/Jonathan's theme but its only the BEST part.mp3", loop
        )

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def joseph(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(
            ctx, "sounds/Joseph's theme but only the good part (1).mp3", loop
        )

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def jotaro(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(
            ctx, "sounds/Jotaro’s theme but it’s only the good part.mp3", loop
        )

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def josuke(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(
            ctx, "sounds/Josuke theme but it's only the good part.mp3", loop
        )

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def kira(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(
            ctx,
            "sounds/Killer (Yoshikage Kira's Theme) - Jojo's Bizarre Adventure Part 4_ "
            "Diamond Is Unbreakable.mp3",
            loop,
        )

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def pillarmen(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(
            ctx, "sounds/Jojo's Bizarre Adventure- Awaken(Pillar Men Theme).mp3", loop
        )

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def boom(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/boom.mp3", loop)

    @commands.command(aliases=["ogei"])
    @commands.bot_has_permissions(manage_messages=True)
    async def ogey(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/ogey.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def rrat(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/rrat.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def fart(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/fart.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def mogumogu(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/mogu.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def bababooey(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/bababooey.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def dog(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/dog.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def totsugeki(self, ctx: commands.Context[Any], loop=None):
        may_sounds = ["sounds/totsugeki_7UWR0L4.mp3", "sounds/totsugeki-may-2.mp3"]
        await self.vcplay(ctx, may_sounds, loop, True)

    @commands.command(aliases=["bong"])
    @commands.bot_has_permissions(manage_messages=True)
    async def tacobell(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/tacobell.mp3", loop)

    @commands.command(aliases=["amogus"])
    @commands.bot_has_permissions(manage_messages=True)
    async def amongus(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/amongus.mp3", loop)

    @commands.command(aliases=["classtrial"])
    @commands.bot_has_permissions(manage_messages=True)
    async def danganronpa(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/danganronpa.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def botansneeze(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/botansneeze.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def water(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/water.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def necoarc(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/necoarc.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def vsauce(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/vsauce.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def gigachad(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/gigachad.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def bruh(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/rushiabruh.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def believeit(self, ctx: commands.Context[Any], loop=None):
        believeit_files = os.listdir("sounds/believeit/")
        believeit_files = [f"sounds/believeit/{x}" for x in believeit_files]
        await self.vcplay(ctx, believeit_files, loop, True)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def pikamee(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/pikamee.mp3", loop)

    @commands.command(aliases=["hellskitchen", "violin"])
    @commands.bot_has_permissions(manage_messages=True)
    async def waterphone(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/waterphone.mp3", loop)

    @commands.command(aliases=["boo-womp"])
    @commands.bot_has_permissions(manage_messages=True)
    async def boowomp(self, ctx: commands.Context[Any], loop=None):
        await self.vcplay(ctx, "sounds/boowomp.mp3", loop)

    @commands.command()
    @commands.bot_has_permissions(manage_webhooks=True, manage_messages=True)
    async def mgr(self, ctx: commands.Context[Any], *, name):
        loop = None
        matches = []
        for root, _dirs, files in os.walk("sounds/mgr/", topdown=False):
            for x in files:
                if any(word in x for word in [name]):
                    matches.append(os.path.join(root, x))

        if matches:
            numbered_mgr_files = [
                f"{index} - {item.split('/')[-2]}: {item.split('/')[-1].split('.')[0]}"
                for index, item in enumerate(matches, 1)
            ]
            if len(matches) == 1:
                await self.vcplay(ctx, matches[0], loop)
            else:
                nl = "\n"
                msg = await ctx.send(
                    f"{len(matches)} matches. Pick a number. YOU HAVE 10 SECONDS!!!\n"
                    f"`{nl.join(numbered_mgr_files)}`"
                )

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                try:
                    await_msg = await self.client.wait_for(
                        "message", check=check, timeout=10
                    )
                    if int(await_msg.content) in list(range(1, len(matches) + 1)):
                        index = int(await_msg.content) - 1
                        await self.vcplay(ctx, matches[index], loop)
                    else:
                        await ctx.send("Invalid number!", delete_after=3)
                        await ctx.message.delete()
                    await await_msg.delete()
                except asyncio.TimeoutError:
                    await ctx.send("Too slow lmao!", delete_after=3)
                    await ctx.message.delete()
                await msg.delete()
                #
        else:
            await ctx.send("No matches lol.", delete_after=3)

    async def pre_play(self, ctx: commands.Context[Any], url, title=None):
        start_time = time.time()
        tasks = []

        tasks.append(subprocess_runner.run_subprocess([
            "yt-dlp",
            "-f",
            "bestaudio",
            "--get-url",
            "--force-ipv4",
            "--no-warnings",
            url,
        ]))

        if title is None:
            tasks.append(subprocess_runner.run_subprocess([
                "yt-dlp",
                "-f",
                "bestaudio",
                "--get-title",
                "--force-ipv4",
                "--no-warnings",
                url,
            ]))

        gathered = await asyncio.gather(*tasks)
        direct_url = gathered[0][1].decode("utf-8").splitlines()[0]
        if title is None:
            title = gathered[1][1].decode("utf-8").splitlines()[0]
        print(f"tasks ran: {(time.time()-start_time):.2f}")
        start_time = time.time()
        asyncio.run_coroutine_threadsafe(
            self.vcplay(ctx, direct_url, dont_delete=True, music_bot=True),
            self.client.loop,
        )
        await ctx.send(f"Playing **{title}**...")
        self.song_now_playing[ctx.guild.id] = f"[{title}]({url})"
        print(f"playing sent: {(time.time()-start_time):.2f}")

    def there_is_queue(self, ctx: commands.Context[Any]):
        server_queue = self.dbname[str(ctx.guild.id)]
        music_queue = server_queue.find().sort("epoch_time", 1)
        music_queue = "\n".join([f"[{x['title']}]({x['url']})" for x in music_queue])
        if music_queue:
            return True
        return False

    @commands.command(aliases=["p"])
    async def play(self, ctx: commands.Context[Any], url=None):
        if url is None:
            if self.there_is_queue(ctx):
                asyncio.run_coroutine_threadsafe(self.run_queue(ctx), self.client.loop)
                em = disnake.Embed(
                    title="▶ CONTINUING! ▶", description="There's a queue! Playing it!"
                )
                await ctx.send(embed=em)
            else:
                await ctx.send("You didn't give me anything. There is no queue either.")
            return
        voicestate = ctx.author.voice
        if not voicestate:
            await ctx.send("You ain't in a VC buhhhh")
            return
        # loop = asyncio.get_running_loop()
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice is None:
            voice_channel = ctx.author.voice.channel
            voice = await voice_channel.connect()
        if not voice.is_playing() and not ctx.guild.id in self.temp_servers_playing:
            # loop.create_task(self.pre_play(ctx, url))
            asyncio.run_coroutine_threadsafe(self.pre_play(ctx, url), self.client.loop)
            self.temp_servers_playing[
                ctx.guild.id
            ] = 0  # temporarily adds to this dict to let bot now the server is playing music
        else:
            _proc, stdout, _stderr = await subprocess_runner.run_subprocess([
                "yt-dlp",
                "-f",
                "bestaudio",
                "--get-title",
                "--force-ipv4",
                "--no-warnings",
                url,
            ])
            title = stdout.decode("utf-8").splitlines()[0]
            try:
                self.temp_servers_playing[ctx.guild.id] += 1
            except KeyError:
                self.temp_servers_playing[ctx.guild.id] = 1
            await ctx.send(
                f"Adding **{title}** to queue... ({self.temp_servers_playing[ctx.guild.id]})"
            )
            server_queue = self.dbname[str(ctx.guild.id)]
            item = {"title": title, "url": url, "epoch_time": time.time()}
            server_queue.insert_one(item)

    @commands.command(aliases=["mq"])
    @commands.bot_has_permissions(embed_links=True)
    async def mqueue(self, ctx: commands.Context[Any]):
        server_queue = self.dbname[str(ctx.guild.id)]
        music_queue = server_queue.find().sort("epoch_time", 1)
        music_queue = "\n".join([f"[{x['title']}]({x['url']})" for x in music_queue])
        if music_queue:
            em = disnake.Embed(title="💥 THE QUEUE 💥", description=music_queue)
            await ctx.send(embed=em)
        else:
            await ctx.send("Ain't no way bruh. There's no queue!! :skull:")

    @commands.command(aliases=["np"])
    @commands.bot_has_permissions(embed_links=True)
    async def nowplaying(self, ctx: commands.Context[Any]):
        try:
            np = self.song_now_playing[ctx.guild.id]
        except KeyError:
            await ctx.send("Nothin's playin rn :sob:")
            server_queue = self.dbname[str(ctx.guild.id)]
            music_queue = server_queue.find().sort("epoch_time", 1)
            music_queue = "\n".join(
                [f"[{x['title']}]({x['url']})" for x in music_queue]
            )
            if music_queue:
                asyncio.run_coroutine_threadsafe(self.run_queue(ctx), self.client.loop)
                em = disnake.Embed(
                    title="▶ CONTINUING! ▶", description="There's a queue! Playing it!"
                )
                await ctx.send(embed=em)
            return
        if np:
            em = disnake.Embed(title="🎧 NOW PLAYING 🎧", description=np)
            await ctx.send(embed=em)
        else:
            await ctx.send("Nothin's playin rn :sob:")

    @commands.command(aliases=["s"])
    @commands.bot_has_permissions(embed_links=True)
    async def skip(self, ctx: commands.Context[Any]):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            try:
                np = self.song_now_playing[ctx.guild.id]
            except KeyError:
                await ctx.send("Nothing is playing rn bruh. can't skip shit")
            voice_client.stop()
            asyncio.run_coroutine_threadsafe(self.run_queue(ctx), self.client.loop)
            em = disnake.Embed(
                title="⏩ SKIPPED! ⏩", description=f"{np} has been skipped"
            )
            await ctx.send(embed=em)
        else:
            if self.there_is_queue(ctx):
                asyncio.run_coroutine_threadsafe(self.run_queue(ctx), self.client.loop)
                em = disnake.Embed(
                    title="▶ CONTINUING! ▶", description="There's a queue! Playing it!"
                )
                await ctx.send(embed=em)
            else:
                await ctx.send("Nothing is playing rn bruh. can't skip shit")

    @commands.command(aliases=["ultrakill"])
    async def sam(self, ctx: commands.Context[Any], *, msg):
        file_path = f"sam/{uuid.uuid4()}.wav"        
        await subprocess_runner.run_subprocess([
            "node", "sam/bundle.js", "--wav", file_path, msg
        ])
        await self.vcplay(ctx, file_path, delete_file=True, custom_name="sam.wav")

    @commands.command(aliases=["tt"])
    async def tiktok(self, ctx: commands.Context[Any], *, msg):
        if len(msg) > 300:
            await ctx.send(
                "Shortening text to 300 characters. It's beyond my control. "
                "<:towashrug:853606191711649812>"
            )
            msg = msg[:300]
        json_data = {
            "text": msg,
            "voice": "en_us_001",
        }
        url = "https://tiktok-tts.weilnet.workers.dev/api/generation"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data) as response:
                json_resp = await response.json()
        base64_data = json_resp["data"]
        if base64_data is None:
            await ctx.send("There was an error. i dunno.")
            return
        raw_bytes = base64.b64decode(base64_data)
        with BytesIO(raw_bytes) as file_obj:
            await self.vcplay(
                ctx, file_obj, file_obj=True, custom_name="tiktok_voice.mp3"
            )


def setup(client: commands.Bot):
    client.add_cog(Vc(client))

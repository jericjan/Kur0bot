"""
help command stuff. inline means they fields remain on the same line. check here for example:
https://discordjs.guide/popular-topics/embeds.html#embed-preview
"""

import json
import os
from typing import TYPE_CHECKING, Any, Optional, TypeAlias, cast

import disnake
from disnake.ext import commands

if TYPE_CHECKING:
    from modules.kur0_only import Kur0only
    Command: TypeAlias = commands.core.Command[Any, Any, Any]

class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.group(invoke_without_command=True)
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, ctx: commands.Context[Any], extra: Optional[str] = None):
        """
        General help command. If invalid subcommand is given, it will go in `extra`
        """

        if extra:
            public_comms = cast(
                "Kur0only", 
                self.client.get_cog("Kur0only")
            ).get_public_commands()
            

            for command_name in public_comms:
                comm = cast("Optional[Command]", self.client.get_command(command_name))
                if comm is not None:
                    for alias in comm.aliases:
                        if alias == extra:  # found the command with matching alias
                            command = cast("Optional[Command]", self.client.get_command(f"help {comm.name}"))
                            ctx.command = command
                            ctx.invoked_subcommand = command
                            await self.client.invoke(ctx) # pyright: ignore[reportUnknownMemberType]
                            return
            await ctx.send(
                "Brother, I don't think I've ever heard of that command before."
            )
            return

        em = disnake.Embed(
            title="Commands",
            description="Here are my sussy commands!\nUse __**k.help <command>**__ for more info "
            "on that command.\n<> means required, [] means optional",
        )

        with open("modules/commands.json", encoding="utf-8") as f:
            data = json.load(f)
            for i in data:
                if i == "hidden":
                    pass
                else:
                    em.add_field(
                        name=i,
                        value="\n".join(data[i]),
                    )

        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def glasses(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Glasses", description="Gives the entire fubuki glasses copypasta"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def nene(self, ctx: commands.Context[Any]):
        em = disnake.Embed(title="Nene", description="Gives Nenechi's full title")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def nenelong(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Nene", description="Gives Nenechi's LONGER full title"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def on(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="On",
            description="Enables permanent sus mode. "
            "Sus replies do not get deleted within 3 seconds.",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def off(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Off",
            description="Disables permanent sus mode. Sus replies get deleted within 3 seconds.",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def megasus(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Megasus",
            description="Gives some random amongus copypasta I found on reddit.",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def bulk(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Bulk",
            description="Sends sus messages in bulk.\nOnly usable in channels named `sus-town` "
            "<:sus:850628234746920971>",
        )
        em.add_field(name="**Syntax**", value="k.bulk <number>")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def stopamongus(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Stop posting about Among Us!",
            description="Sends the stop posting about among us copypasta",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def confession(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Matsuri's Confession",
            description="Sends Matsuri's confession to Fubuki",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def fortnite(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Fortnite", description="Sends the fortnite dance in text"
        )
        await ctx.send(embed=em)

    @help.command(aliases=["e"])
    @commands.bot_has_permissions(embed_links=True)
    async def emote(self, ctx: commands.Context[commands.Bot]):
        em = disnake.Embed(
            title="Emote",
            description="Sends an animated emote from any server that this bot is in.",
        )
        em.add_field(name="**Syntax**", value="k.emote <emotename>")
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["ge"])
    @commands.bot_has_permissions(embed_links=True)
    async def getemotes(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Get Emotes!",
            description="Sends all emotes that this bot has. "
            "It has emotes for all servers it's in.",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def wristworld(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Wristworld", description="Sends the wristworld miku copypasta."
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def fmega(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="F Mega!", description="Sends the F MEGA gif from Jojo's."
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kotowaru(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Daga kotowaru!", description="Use this to refuse someone's offer"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def ascend(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Ascend to Heaven!",
            description="Use this to to ascend when something glorious occurs.",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def jizz(self, ctx: commands.Context[Any]):
        em = disnake.Embed(title="Jizz", description="Use this to jizz.")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def letsgo(self, ctx: commands.Context[Any]):
        em = disnake.Embed(title="Let's go!", description="Playus 'Let's gooo' in vc")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def vtubus(self, ctx: commands.Context[Any]):
        em = disnake.Embed(title="Vtubus", description="vtubus")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def ding(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Ding ding ding ding ding ddi di ding", description="amongus"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def yodayo(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Yo dayo!", description="Plays Ayame's 'Yo dayo!' in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def yodazo(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Yo dazo!", description="Plays Ayame's 'Yo dazo!' in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def jonathan(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Jonathan's theme", description="Plays Jonathan's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def joseph(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Joseph's theme", description="Plays Joseph's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def jotaro(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Jotaro's theme", description="Plays Jotaro's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def josuke(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Josuke's theme", description="Plays Josuke's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def giorno(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Giorno's theme", description="Plays Giorno's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kira(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Yoshikage Kira's theme",
            description="Plays Yoshikage Kira's theme in VC",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pillarmen(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Pillar Men Theme", description="Plays the Pillar Men Theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def tts(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Text to speech", description="Send a TTS message in VC"
        )
        em.add_field(name="**Syntax**", value="] <message>")
        em.add_field(
            name="**Accents**",
            value="] (US default)\n]au (Australia)\n]uk (United Kingdom)\n]in (India)",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["tt"])
    @commands.bot_has_permissions(embed_links=True)
    async def tiktok(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Tiktok TTS",
            description="Reads text in the tiktok voice in VC or as a file.",
        )
        em.add_field(name="**Syntax**", value="k.tiktok <message>")
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def badapple(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Bad Apple but in custom emotes",
            description="Sends 80 animated emotes that all make up the Bad Apple PV (Only works on "
            "PC)",
        )
        em.add_field(name="**Emotes by:**", value="https://github.com/gohjoseph")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def clip(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Clip a YT Video",
            description="clips a YouTube video given the start and end times (HH:MM:SS)\n**SLOWER**"
            " than `fastclip` but accurate",
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
    @commands.bot_has_permissions(embed_links=True)
    async def fastclip(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Quickly clip a YT Video",
            description="clips a YouTube video given the start and end times (HH:MM:SS)\n**FASTER**"
            " than `clip` but will start at the nearest keyframe, so it'll start a couple seconds "
            "earlier than the given timestamp",
        )
        em.add_field(
            name="**Syntax**",
            value="k.fastclip <url> <start time> <end time> <filename>",
        )
        em.add_field(
            name="**Example**",
            value="k.fastclip https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:00:52 00:01:05 "
            "filename",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def fastclipsub(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Quickly clip a YT Video w/ fancy subs",
            description="Like fastclip but also burns fancy subs into the vod",
        )
        em.add_field(
            name="**Syntax**",
            value="k.fastclipsub <url> <start time> <end time> <filename>",
        )
        em.add_field(
            name="**Example**",
            value="k.fastclipsub https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:00:52 00:01:05 "
            "filename",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def download(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Download a YT Video", description="Download a YouTube of your choice"
        )
        em.add_field(name="**Syntax**", value="k.download <url> [--audio]")
        em.add_field(
            name="**Flags**",
            value="`--audio` - will download only the audio of a video",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def botansneeze(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Botan Sneeze",
            description="because fuck you, have a botan sneeze",
        )
        em.add_field(name="**Syntax**", value="k.botansneeze [loop]", inline=False)
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def boom(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Vine Boom SFX", description="plays the funni boom sfx in vc"
        )
        await ctx.send(embed=em)

    @help.command(aliases=["ogei"])
    @commands.bot_has_permissions(embed_links=True)
    async def ogey(self, ctx: commands.Context[Any]):
        em = disnake.Embed(title="Ogey...", description="Plays Pekora's ogey in VC.")
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def rrat(self, ctx: commands.Context[Any]):
        em = disnake.Embed(title="Rrat!", description="Plays Pekora's rrat in VC.")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def fart(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Reverb fart sfx", description="Plays funni fart sound in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def mogumogu(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Mogu mogu!", description="Plays okayu's mogu mogu in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def bababooey(self, ctx: commands.Context[Any]):
        em = disnake.Embed(title="Bababooey!", description="Plays bababooey in VC.")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def dog(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="What the dog doin?", description="Plays 'what da dog doin' in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def totsugeki(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="TOTSUGEKI!!!", description="Plays May's Totsugeki in VC."
        )
        await ctx.send(embed=em)

    @help.command(aliases=["bong"])
    @commands.bot_has_permissions(embed_links=True)
    async def tacobell(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Taco Bell bong sfx",
            description="Plays the funny taco bell sound effect in VC.",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["amogus"])
    @commands.bot_has_permissions(embed_links=True)
    async def amongus(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="AMONGUS!", description="Plays the guy yelling amongus in VC."
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["classtrial"])
    @commands.bot_has_permissions(embed_links=True)
    async def danganronpa(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Class trial time!",
            description="Plays '議論 -HEAT UP-' from Danganronpa in VC.",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def join(self, ctx: commands.Context[Any]):
        em = disnake.Embed(title="Join VC", description="Sus bot will enter the VC.")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def stop(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="STOP!",
            description="Sus bot will stop playing if it's playing something in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def stoploop(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="STOP THE LOOP!",
            description="Sus bot will stop playing if it's playing something in VC that has loop "
            "mode enabled.",
        )
        em.add_field(name="**How loop???**", value="k.commandname loop")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def leave(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Sayonara...", description="Sus bot will leave the VC."
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def stream(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="YouTube Stream Time Embed",
            description="Sends an embed of a YouTube stream with its start time.",
        )
        em.add_field(name="**Syntax**", value="k.stream https://youtu.be/wNMW87foNAI")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def water(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Water and Water and Water Water",
            description="Plays 'Water and Water and Water Water'in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def necoarc(self, ctx: commands.Context[Any]):
        em = disnake.Embed(title="Neco arc", description="Plays neco arc in VC.")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def vsauce(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Vsauce music", description="Plays the vsauce music in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def gigachad(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Gigachad",
            description="Plays a bit of 'Can You Feel My Heart' in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def bruh(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Rushia Bruh SFX",
            description="Plays Rushia saying bruh in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def believeit(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Naruto - Believe it!",
            description='Plays Naruto saying "Believe it!" in VC. 82 variations.',
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pikamee(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="pikamee is insane",
            description='Plays a clip of Pikamee saying "Pikamee, how are you doing? I feel '
            'awesome. I killed everyone but I feel awesome."',
        )
        await ctx.send(embed=em)

    @help.command(aliases=["hellskitchen", "violin"])
    @commands.bot_has_permissions(embed_links=True)
    async def waterphone(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Hell's Kitchen SFX",
            description="Plays the Hell's Kitchen sound effect.",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["boo-womp"])
    @commands.bot_has_permissions(embed_links=True)
    async def boowomp(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Boo-womp!",
            description="Plays the boo-womp sound effect that they play on Spongebob when something"
            " sad happens.",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pet(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Pet user",
            description="Sends a gif of the mentioned user being petted.",
        )
        em.add_field(
            name="**Syntax**", value="k.pet <mentioned user>\nk.pet <image url>"
        )
        await ctx.send(embed=em)

    @help.command(aliases=["findsauce", "getsauce"])
    @commands.bot_has_permissions(embed_links=True)
    async def sauce(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Get sauce", description="Uses Saucenao API to find sauce."
        )
        em.add_field(
            name="**Syntax**",
            value="k.sauce <url>\nUpload image with k.sauce\nReply to a message with k.sauce ",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def altsauce(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Alternate way to get sauce",
            description="Use this in case the default one breaks for some reason.",
        )
        em.add_field(
            name="**Syntax**",
            value="k.altsauce <url>\nUpload image with k.sauce\nReply to a message with k.sauce ",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def clipaudio(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Clip Audio", description="Clips the audio of a given YouTube video"
        )
        em.add_field(
            name="**Syntax**",
            value="k.clipaudio <url> <start time> <end time> <filename> <filetype>",
        )
        em.add_field(name="**Filetypes**", value="mp3\nwav\nogg")
        em.add_field(
            name="**Example**",
            value="k.clipaudio https://www.youtube.com/watch?v=UIp6_0kct_U 00:00:56 00:01:05 poger "
            "mp3",
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def ping(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Ping",
            description="Pings the bot. What else would this be lol.",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["flip"])
    @commands.bot_has_permissions(embed_links=True)
    async def coinflip(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Coin Flip",
            description="Flips a coin. That's it",
        )
        em.add_field(name="**Syntax**", value="k.coinflip  heads\nk.coinflip tails")
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["shitify", "pixelize"])
    @commands.bot_has_permissions(embed_links=True)
    async def lowqual(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Low quality-ify",
            description="Aggressively downscales video or photo to 36x20px :sunglasses:",
        )
        em.add_field(
            name="**Syntax**",
            value="k.lowqual <url>\nUpload video/photo with k.lowqual\nReply to a video/photo "
            "message with k.lowqual ",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def when(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="When?",
            description="Tells you exactly when a YT video has been uploaded, or when a stream has "
            "started and ended",
        )
        em.add_field(name="**Syntax**", value="k.when <yt_url>")
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def checkcomment(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="YT Comment Checker",
            description="Give it a YT comment link and it will keep checking if it exists for the "
            "next 5 minutes. If it doesn't exist before then, it will ping you.",
        )
        em.add_field(name="**Syntax**", value="k.checkcomment <yt_comment_url>")
        await ctx.send(embed=em)

    @help.command(aliases=["akasupa", "supacha"])
    @commands.bot_has_permissions(embed_links=True)
    async def superchat(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Superchat!",
            description="Sends an image of a superchat of your choosing.",
        )
        em.add_field(
            name="**Syntax**",
            value="k.superchat <amount with currency> <message>",
        )
        em.add_field(
            name="**Example**",
            value="k.superchat $100 poggers",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["oldakasupa", "oldsupacha"])
    @commands.bot_has_permissions(embed_links=True)
    async def oldsuperchat(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Superchat! (OLD)",
            description="Old ver. of k.superchat. It just goes to a [site](https://ytsc.leko.moe/) "
            "that creates the image for you. ",
        )
        em.add_field(
            name="**Syntax**",
            value="k.oldsuperchat <amount with currency> <message>",
        )
        em.add_field(
            name="**Example**",
            value="k.oldsuperchat $100 poggers",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["vid2gif", "gifify"])
    @commands.bot_has_permissions(embed_links=True)
    async def gif(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Video to Gif",
            description="Converts a video to GIF. Doesn't work with YouTube URLs yet.",
        )
        em.add_field(
            name="**Syntax**",
            value="k.gif <video_url>\nUpload video with k.gif\nReply to a video with k.gif ",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["vid2gif2", "gifify2"])
    @commands.bot_has_permissions(embed_links=True)
    async def gif2(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Video to Gif 2",
            description="k.gif but higher quality and slower",
        )
        em.add_field(
            name="**Syntax**",
            value="k.gif2 <video_url>\nUpload video with k.gif2\nReply to a video with k.gif2 \n\n"
            "Optional: you can add include quality (1-100) at the end of the command. Default: 70",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def resize(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Resize image",
            description="Resizes an image to a given resolution",
        )
        em.add_field(
            name="**Syntax**",
            value="k.resize <width> <height> <link>\nYou can also leave <link> blank and just "
            "upload or reply to an image.",
        )
        await ctx.send(embed=em)

    def paginate(self, lines: str, chars: int =4096):
        size = 0
        message: list[str] = []
        for line in lines:
            if len(line) + size > chars:
                yield message
                message = []
                size = 0
            message.append(line)
            size += len(line)
        yield message

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def mgr(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Metal Gear Rising: Revengeance Soundboard",
            description="Plays any MGR quote that I have. (no loop support)",
        )
        em.add_field(
            name="**Syntax**",
            value="k.mgr <sound_name>",
        )
        await ctx.send(embed=em)

        mgr_list = ""
        for _root, dirs, _files in os.walk("sounds/mgr/", topdown=False):
            for name in dirs:
                mgr_list += f"**{name}:**\n"
                mgr_list += "\n".join(
                    [f"- {x.split('.')[0]}" for x in os.listdir(f"sounds/mgr/{name}")]
                )
                mgr_list += "\n\n"
        embed = disnake.Embed()
        for index, message in enumerate(self.paginate(mgr_list)):
            if index == 0:
                embed.title = "Sounds (you can enter a part of the name)"
            else:
                embed.title = ""
            embed.description = "".join(message)
            await ctx.send(embed=embed)

    @help.command(aliases=["us"])
    @commands.bot_has_permissions(embed_links=True)
    async def uploadsticker(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Upload sticker",
            description="Uploads an image as a sticker.",
        )
        em.add_field(
            name="**Syntax**",
            value="k.uploadsticker <name> <emoji as text> <url>\nUpload image with k.uploadsticker "
            "<name> <emoji as text>\n"
            "Reply to a message with k.uploadsticker <name> <emoji as text>",
            inline=False,
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        em.add_field(
            name="**Example**",
            value="k.uploadsticker agony cry https://cdn.discordapp.com/attachments/"
            "812666551051747369/983132328945680434/IMG_1963.jpg",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["uploademoji", "ue"])
    @commands.bot_has_permissions(embed_links=True)
    async def uploademote(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Upload emote",
            description="Uploads an image as an emote.",
        )
        em.add_field(
            name="**Syntax**",
            value="k.uploademote <name> <url\\emote ID>\nUpload image with k.uploademote <name>\n"
            "Reply to a message with k.uploademote <name>",
            inline=False,
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        em.add_field(
            name="**Example**",
            value="k.uploademote stuff https://cdn.discordapp.com/attachments/809247468084133898/"
            "985504342461280306/stuff.png",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["japanese"])
    @commands.bot_has_permissions(embed_links=True)
    async def nihongo(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Translate to Japanese",
            description="Translate given text to Japanese. Uses Google Translate because I can't "
            "get access to the DeepL API because I'm filipino :(",
        )
        em.add_field(name="**Syntax**", value="k.nihongo <sentence>", inline=False)
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        em.add_field(
            name="**Example**",
            value="k.nihongo hello",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["english"])
    @commands.bot_has_permissions(embed_links=True)
    async def eigo(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Translate to English",
            description="Translate given text to English. Uses Google Translate because I can't get"
            " access to the DeepL API because I'm filipino :(",
        )
        em.add_field(name="**Syntax**", value="k.eigo <sentence>", inline=False)
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        em.add_field(
            name="**Example**",
            value="k.eigo 草",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["german"])
    @commands.bot_has_permissions(embed_links=True)
    async def doitsu(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Translate to German",
            description="Translate given text to German. Uses Google Translate.",
        )
        em.add_field(name="**Syntax**", value="k.doitsu <sentence>", inline=False)
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        em.add_field(
            name="**Example**",
            value="k.doitsu hello",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["addqueue", "insertqueue", "removequeue", "clearqueue"])
    @commands.bot_has_permissions(embed_links=True)
    async def queue(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Queue",
            description="The server's queue. This was originally made for Karaoke in the pacifam "
            "server to keep track of queues but it can be used for anything. For now, the queues "
            "are unique to each server and anybody can modify them.",
        )
        em.add_field(
            name="**Commands**",
            value="__k.queue__ - shows the server's queue\n\n"
            "__k.addqueue <things separated w/ spaces>__ - adds things to queue\n\n"
            "__k.insertqueue <name of thing to insert new thing after> <new thing>__ - insert new "
            "thing right after an existing thing\n\n"
            "__k.removequeue <thing>__ - removes thing from queue\n\n"
            "__k.clearqueue__ - clears the queue",
            inline=False,
        )
        await ctx.send(embed=em)

    @help.command(aliases=["quickvergil"])
    @commands.bot_has_permissions(embed_links=True)
    async def vergil(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Vergil Cut Green Screen",
            description="Give it an image and Vergil will cut through it with his unending\n"
            "**ＭＯＴＩＶＡＴＩＯＮ**.",
        )
        em.add_field(
            name="**Commands**",
            value="__k.vergil <image>__ - normal version\n\n"
            "__k.quickvergil <image>__ - just greenscreen, image doesn't get sliced but a couple "
            "seconds faster than above",
            inline=False,
        )
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def hallofshame(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Hall Of Shame",
            description="The hall of shame where people who commit cringe will be posted on.",
        )
        em.add_field(
            name="**Syntax**", value="k.hallofshame <mention_channel>", inline=False
        )
        em.add_field(
            name="**Cringe Requirements:**",
            value="You will be cringe when you play any of these games: \n"
            "⦁ Mobile Legends: Bang Bang\n"
            "⦁ League of Legends\n"
            "⦁ Honkai Impact 3\n"
            "⦁ Genshin Impact\n"
            "(and no, these cannot be customized <a:trollplant:934777423881445436>)",
            inline=False,
        )
        await ctx.send(embed=em)

    @help.command(
        aliases=[
            "getmap",
            "getosu",
            "getosumap2",
            "getmap2",
            "getosu2",
            "getosumap3",
            "getmap3",
            "getosu3",
        ]
    )
    @commands.bot_has_permissions(embed_links=True)
    async def getosumap(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Get osu! map",
            description="Sends you the osu! map someone is playing.",
        )
        em.add_field(
            name="**Syntax**", value=r"k.getosumap <user\ping\id>", inline=False
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        em.add_field(
            name="**Example**",
            value="k.getosumap Kur0",
        )
        em.add_field(
            name="**Alternative**",
            value="you can try k.getosumap2 and k.getosumap3 for a different method of grabbing "
            "maps.",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["mq"])
    @commands.bot_has_permissions(embed_links=True)
    async def mqueue(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Not a music queue",
            description="Does not show the queue of songs you've queued",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["p"])
    @commands.bot_has_permissions(embed_links=True)
    async def play(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Not a music player",
            description="Does not play a song in VC given a YT link",
        )
        em.add_field(name="**Syntax**", value=r"k.play <yt_url>", inline=False)
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["np"])
    @commands.bot_has_permissions(embed_links=True)
    async def nowplaying(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Not a nowplaying shower",
            description="Does not show the currently playing song in VC",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["s"])
    @commands.bot_has_permissions(embed_links=True)
    async def skip(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Not a song skipper",
            description="Does not skip the currently playing song in VC",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command(aliases=["ultrakill"])
    @commands.bot_has_permissions(embed_links=True)
    async def sam(self, ctx: commands.Context[Any]):
        em = disnake.Embed(
            title="Sam TTS",
            description="Plays Sam TTS, commonly known as the Ultrakill TTS, in VC",
        )
        em.add_field(name="**Aliases**", value=",".join(cast("Command", ctx.command).aliases)) # pyright: ignore[reportUnknownMemberType]
        await ctx.send(embed=em)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def google(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx,
            "Google Search",
            "Searches Google and sends back results as an embed.",
            self.client,
        ) as em:
            em.add_syntax(r"k.google <search_query>")

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def meme(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx, "Meme Generator", "Make a quick meme with this command", self.client
        ) as em:
            em.add_syntax(
                r"k.meme <top_text> <bottom_text> <img_url/reply to a message>"
            )

    @help.command(aliases=["this"])
    @commands.bot_has_permissions(embed_links=True)
    async def thisrighthere(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx,
            "This right here...",
            "Creates a video saying appreciating an image sent by a user.",
            self.client,
        ) as em:
            em.add_syntax("k.this <image>")
            em.show_aliases()

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def jisho(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx,
            "Jisho dictionary",
            "Searches through the Jisho database given a Japanese word",
            self.client,
        ) as em:
            em.add_example("k.jisho 草")

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def gpt(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx, "GPT", "Simple AI chat. Doesn't remember shit.", self.client
        ) as em:
            em.add_syntax("k.gpt <message>")

    @help.command(aliases=["convert"])
    @commands.bot_has_permissions(embed_links=True)
    async def currency(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx,
            "Currency Converter",
            "Converts currencies.\n"
            "Check [here]"
            "(https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json) "
            "for what currencies I support.",
            self.client,
        ) as em:
            em.add_syntax("k.currency <base currency> <target currency> <value>")
            em.add_example("k.curency usd php 100")
            em.show_aliases()

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def height(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx,
            "Height convert",
            "Converts height from cm to foot-inches and vice versa",
            self.client,
        ) as em:
            em.add_syntax("k.height <height>")
            em.add_example("k.height 100cm\nk.height 5'3\"")

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def image(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx,
            "Image searcher",
            "Searches for images. Uses the SerpApi API.",
            self.client,
        ) as em:
            em.add_syntax("k.image <query>")
            em.add_example("k.image amogus")

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def day(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx,
            "Day boundaries",
            "Tells you when the current day ends or the next one starts for all timezones",
            self.client,
        ):
            pass

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def say(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx, "Say", "Makes the bot say things. That's it.", self.client
        ) as em:
            em.add_syntax("k.say stuff")

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def stats(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx,
            "Kur0bot Stats",
            "Gives you stats for certain things a user has done that are related to the bot",
            self.client,
        ) as em:
            em.add_syntax("k.stats <user> (leave blank to get your own stats)")
            em.add_example("k.stats Kur0")

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kill(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx, "KILL", "Murderizes someone. Just try it.", self.client
        ) as em:
            em.add_syntax("k.ill Kur0")
            em.show_aliases(auto=True)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def removesticker(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx, "Remove sticker", "Removes a sticker.", self.client
        ) as em:
            em.add_syntax("k.rs <sticker_name>")
            em.show_aliases(auto=True)

    @help.command()
    @commands.bot_has_permissions(embed_links=True)
    async def removeemote(self, ctx: commands.Context[Any]):
        async with EmbedMaker(
            ctx, "Remove emote", "Removes an emote.", self.client
        ) as em:
            em.add_syntax("k.re <emote_name>")
            em.show_aliases(auto=True)

class EmbedMaker:
    def __init__(self, ctx: commands.Context[Any], title: str, desc: str, client: Optional[commands.Bot] = None):
        self.ctx = ctx
        self.client = client
        self.em = disnake.Embed(
            title=title,
            description=desc,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any):
        await self.ctx.send(embed=self.em)

    def add_syntax(self, syntax: str, inline: bool=False):
        self.em.add_field(name="**Syntax**", value=syntax, inline=inline)

    def add_example(self, ex: str, inline: bool =False):
        self.em.add_field(name="**Example**", value=ex, inline=inline)

    def show_aliases(self, auto: bool = False):
        """
        need to rewrite this.
        """

        command = cast("Command", self.ctx.command) # pyright: ignore[reportUnknownMemberType]
        # Uses when you don't specify aliases in the help command itself
        if auto:
            if self.client is None:
                raise Exception(
                    "self.client not provided when show_aliases() is auto mode!"
                )
            command = cast("Command", self.client.get_command(command.name)) # pyright: ignore[reportUnknownMemberType]
            self.em.add_field(
                name="**Aliases**",
                value=",".join(
                    cast("Command", self.client.get_command(command.name))
                    .aliases
                ),
            )
        else:
            self.em.add_field(
                name="**Aliases**", value=",".join(command.aliases)
            )


def setup(client: commands.Bot):
    client.add_cog(Help(client))

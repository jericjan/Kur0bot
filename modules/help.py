from discord.ext import commands
import discord


class Help(commands.Cog):
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(
            title="Commands",
            description="Here are my sussy commands!\nUse __**k.help <command>**__ for more info on that command.",
        )
        em.add_field(
            name="copypasta",
            value="glasses\nnene\nnenelong\nstopamongus\nconfession\nwristworld\nmegasus",
        )
        em.add_field(name="sus", value="on\noff\nbulk")
        em.add_field(name="ascii", value="fortnite")
        em.add_field(
            name="others",
            value="emote\ngetemotes\nbadapple\nclip\nfastclip\nclipaudio\ndownload\nstream\npet\nsauce\nping",
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
    async def glasses(self, ctx):
        em = discord.Embed(
            title="Glasses", description="Gives the entire fubuki glasses copypasta"
        )
        await ctx.send(embed=em)

    @help.command()
    async def nene(self, ctx):
        em = discord.Embed(title="Nene", description="Gives Nenechi's full title")
        await ctx.send(embed=em)

    @help.command()
    async def nenelong(self, ctx):
        em = discord.Embed(
            title="Nene", description="Gives Nenechi's LONGER full title"
        )
        await ctx.send(embed=em)

    @help.command()
    async def on(self, ctx):
        em = discord.Embed(
            title="On",
            description="Enables permanent sus mode. Sus replies do not get deleted within 3 seconds.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def off(self, ctx):
        em = discord.Embed(
            title="Off",
            description="Disables permanent sus mode. Sus replies get deleted within 3 seconds.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def megasus(self, ctx):
        em = discord.Embed(
            title="Megasus",
            description="Gives some random amongus copypasta I found on reddit.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def bulk(self, ctx):
        em = discord.Embed(title="Bulk", description="Sends sus messages in bulk.")
        em.add_field(name="**Syntax**", value="k.bulk <number>")
        await ctx.send(embed=em)

    @help.command()
    async def stopamongus(self, ctx):
        em = discord.Embed(
            title="Stop posting about Among Us!",
            description="Sends the stop posting about among us copypasta",
        )
        await ctx.send(embed=em)

    @help.command()
    async def confession(self, ctx):
        em = discord.Embed(
            title="Matsuri's Confession",
            description="Sends Matsuri's confession to Fubuki",
        )
        await ctx.send(embed=em)

    @help.command()
    async def fortnite(self, ctx):
        em = discord.Embed(
            title="Fortnite", description="Sends the fortnite dance in text"
        )
        await ctx.send(embed=em)

    @help.command(aliases=["e"])
    async def emote(self, ctx):
        em = discord.Embed(
            title="Emote",
            description="Sends an animated emote from any server that this bot is in.",
        )
        em.add_field(name="**Syntax**", value="k.emote <emotename>")
        em.add_field(name="**Aliases**", value="e")
        await ctx.send(embed=em)

    @help.command(aliases=["ge"])
    async def getemotes(self, ctx):
        em = discord.Embed(
            title="Get Emotes!",
            description="Sends all emotes that this bot has. It has emotes for all servers it's in.",
        )
        em.add_field(name="**Aliases**", value="ge")
        await ctx.send(embed=em)

    @help.command()
    async def wristworld(self, ctx):
        em = discord.Embed(
            title="Wristworld", description="Sends the wristworld miku copypasta."
        )
        await ctx.send(embed=em)

    @help.command()
    async def fmega(self, ctx):
        em = discord.Embed(
            title="F Mega!", description="Sends the F MEGA gif from Jojo's."
        )
        await ctx.send(embed=em)

    @help.command()
    async def kotowaru(self, ctx):
        em = discord.Embed(
            title="Daga kotowaru!", description="Use this to refuse someone's offer"
        )
        await ctx.send(embed=em)

    @help.command()
    async def ascend(self, ctx):
        em = discord.Embed(
            title="Ascend to Heaven!",
            description="Use this to to ascend when something glorious occurs.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def jizz(self, ctx):
        em = discord.Embed(title="Jizz", description="Use this to jizz.")
        await ctx.send(embed=em)

    @help.command()
    async def letsgo(self, ctx):
        em = discord.Embed(title="Let's go!", description="Playus 'Let's gooo' in vc")
        await ctx.send(embed=em)

    @help.command()
    async def vtubus(self, ctx):
        em = discord.Embed(title="Vtubus", description="vtubus")
        await ctx.send(embed=em)

    @help.command()
    async def ding(self, ctx):
        em = discord.Embed(
            title="Ding ding ding ding ding ddi di ding", description="amongus"
        )
        await ctx.send(embed=em)

    @help.command()
    async def yodayo(self, ctx):
        em = discord.Embed(
            title="Yo dayo!", description="Plays Ayame's 'Yo dayo!' in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def yodazo(self, ctx):
        em = discord.Embed(
            title="Yo dazo!", description="Plays Ayame's 'Yo dazo!' in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def jonathan(self, ctx):
        em = discord.Embed(
            title="Jonathan's theme", description="Plays Jonathan's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def joseph(self, ctx):
        em = discord.Embed(
            title="Joseph's theme", description="Plays Joseph's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def jotaro(self, ctx):
        em = discord.Embed(
            title="Jotaro's theme", description="Plays Jotaro's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def josuke(self, ctx):
        em = discord.Embed(
            title="Josuke's theme", description="Plays Josuke's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def giorno(self, ctx):
        em = discord.Embed(
            title="Giorno's theme", description="Plays Giorno's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def kira(self, ctx):
        em = discord.Embed(
            title="Yoshikage Kira's theme",
            description="Plays Yoshikage Kira's theme in VC",
        )
        await ctx.send(embed=em)

    @help.command()
    async def pillarmen(self, ctx):
        em = discord.Embed(
            title="Pillar Men Theme", description="Plays the Pillar Men Theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def tts(self, ctx):
        em = discord.Embed(
            title="Text to speech", description="Send a TTS message in VC"
        )
        em.add_field(name="**Syntax**", value="] <message>")
        em.add_field(
            name="**Accents**",
            value="] (US default)\n]au (Australia)\n]uk (United Kingdom)\n]in (India)",
        )
        await ctx.send(embed=em)

    @help.command()
    async def badapple(self, ctx):
        em = discord.Embed(
            title="Bad Apple but in custom emotes",
            description="Sends 80 animated emotes that all make up the Bad Apple PV (Only works on PC)",
        )
        em.add_field(name="**Emotes by:**", value="https://github.com/gohjoseph")
        await ctx.send(embed=em)

    @help.command()
    async def clip(self, ctx):
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
    async def fastclip(self, ctx):
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
    async def download(self, ctx):
        em = discord.Embed(
            title="Download a YT Video", description="Download a YouTube of your choice"
        )
        em.add_field(name="**Syntax**", value="k.download <url>")
        await ctx.send(embed=em)

    @help.command()
    async def botansneeze(self, ctx):
        em = discord.Embed(
            title="Botan Sneeze", description="because fuck you, have a botan sneeze"
        )
        em.add_field(name="**Syntax**", value="k.botansneeze [loop]")
        await ctx.send(embed=em)

    @help.command()
    async def boom(self, ctx):
        em = discord.Embed(
            title="Vine Boom SFX", description="plays the funni boom sfx in vc"
        )
        await ctx.send(embed=em)

    @help.command(aliases=["ogei"])
    async def ogey(self, ctx):
        em = discord.Embed(title="Ogey...", description="Plays Pekora's ogey in VC.")
        em.add_field(name="**Aliases**", value="ogei")
        await ctx.send(embed=em)

    @help.command()
    async def rrat(self, ctx):
        em = discord.Embed(title="Rrat!", description="Plays Pekora's rrat in VC.")
        await ctx.send(embed=em)

    @help.command()
    async def fart(self, ctx):
        em = discord.Embed(
            title="Reverb fart sfx", description="Plays funni fart sound in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    async def mogumogu(self, ctx):
        em = discord.Embed(
            title="Mogu mogu!", description="Plays okayu's mogu mogu in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    async def bababooey(self, ctx):
        em = discord.Embed(title="Bababooey!", description="Plays bababooey in VC.")
        await ctx.send(embed=em)

    @help.command()
    async def dog(self, ctx):
        em = discord.Embed(
            title="What the dog doin?", description="Plays 'what da dog doin' in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    async def totsugeki(self, ctx):
        em = discord.Embed(
            title="TOTSUGEKI!!!", description="Plays May's Totsugeki in VC."
        )
        await ctx.send(embed=em)

    @help.command(aliases=["bong"])
    async def tacobell(self, ctx):
        em = discord.Embed(
            title="Taco Bell bong sfx",
            description="Plays the funny taco bell sound effect in VC.",
        )
        em.add_field(name="**Aliases**", value="bong")
        await ctx.send(embed=em)

    @help.command(aliases=["amogus"])
    async def amongus(self, ctx):
        em = discord.Embed(
            title="AMONGUS!", description="Plays the guy yelling amongus in VC."
        )
        em.add_field(name="**Aliases**", value="amogus")
        await ctx.send(embed=em)

    @help.command(aliases=["classtrial"])
    async def danganronpa(self, ctx):
        em = discord.Embed(
            title="Class trial time!",
            description="Plays '議論 -HEAT UP-' from Danganronpa in VC.",
        )
        em.add_field(name="**Aliases**", value="classtrial")
        await ctx.send(embed=em)

    @help.command()
    async def join(self, ctx):
        em = discord.Embed(title="Join VC", description="Sus bot will enter the VC.")
        await ctx.send(embed=em)

    @help.command()
    async def stop(self, ctx):
        em = discord.Embed(
            title="STOP!",
            description="Sus bot will stop playing if it's playing something in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def stoploop(self, ctx):
        em = discord.Embed(
            title="STOP THE LOOP!",
            description="Sus bot will stop playing if it's playing something in VC that has loop mode enabled.",
        )
        em.add_field(name="**How loop???**", value="k.commandname loop")
        await ctx.send(embed=em)

    @help.command()
    async def leave(self, ctx):
        em = discord.Embed(
            title="Sayonara...", description="Sus bot will leave the VC."
        )
        await ctx.send(embed=em)

    @help.command()
    async def stream(self, ctx):
        em = discord.Embed(
            title="YouTube Stream Time Embed",
            description="Sends an embed of a YouTube stream with its start time.",
        )
        em.add_field(name="**Syntax**", value="k.stream https://youtu.be/wNMW87foNAI")
        await ctx.send(embed=em)

    @help.command()
    async def water(self, ctx):
        em = discord.Embed(
            title="Water and Water and Water Water",
            description="Plays 'Water and Water and Water Water'in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def necoarc(self, ctx):
        em = discord.Embed(title="Neco arc", description="Plays neco arc in VC.")
        await ctx.send(embed=em)

    @help.command()
    async def vsauce(self, ctx):
        em = discord.Embed(
            title="Vsauce music", description="Plays the vsauce music in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    async def gigachad(self, ctx):
        em = discord.Embed(
            title="Gigachad",
            description="Plays a bit of 'Can You Feel My Heart' in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def pet(self, ctx):
        em = discord.Embed(
            title="Pet user",
            description="Sends a gif of the mentioned user being petted.",
        )
        em.add_field(
            name="**Syntax**", value="k.pet <mentioned user>\nk.pet <image url>"
        )
        await ctx.send(embed=em)

    @help.command(aliases=["findsauce", "getsauce"])
    async def sauce(self, ctx):
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
    async def clipaudio(self, ctx):
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

    @help.command()
    async def ping(self, ctx):
        em = discord.Embed(
            title="Ping",
            description="Pings the bot. What else would this be lol.",
        )
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Help(client))
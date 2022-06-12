from disnake.ext import commands
import disnake
import json
import os

class Help(commands.Cog):
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = disnake.Embed(
            title="Commands",
            description="Here are my sussy commands!\nUse __**k.help <command>**__ for more info on that command.",
        )

        with open("modules/commands.json") as f:
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
    async def glasses(self, ctx):
        em = disnake.Embed(
            title="Glasses", description="Gives the entire fubuki glasses copypasta"
        )
        await ctx.send(embed=em)

    @help.command()
    async def nene(self, ctx):
        em = disnake.Embed(title="Nene", description="Gives Nenechi's full title")
        await ctx.send(embed=em)

    @help.command()
    async def nenelong(self, ctx):
        em = disnake.Embed(
            title="Nene", description="Gives Nenechi's LONGER full title"
        )
        await ctx.send(embed=em)

    @help.command()
    async def on(self, ctx):
        em = disnake.Embed(
            title="On",
            description="Enables permanent sus mode. Sus replies do not get deleted within 3 seconds.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def off(self, ctx):
        em = disnake.Embed(
            title="Off",
            description="Disables permanent sus mode. Sus replies get deleted within 3 seconds.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def megasus(self, ctx):
        em = disnake.Embed(
            title="Megasus",
            description="Gives some random amongus copypasta I found on reddit.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def bulk(self, ctx):
        em = disnake.Embed(
            title="Bulk",
            description="Sends sus messages in bulk.\nOnly usable in channels named `sus-town` <:sus:850628234746920971>",
        )
        em.add_field(name="**Syntax**", value="k.bulk <number>")
        await ctx.send(embed=em)

    @help.command()
    async def stopamongus(self, ctx):
        em = disnake.Embed(
            title="Stop posting about Among Us!",
            description="Sends the stop posting about among us copypasta",
        )
        await ctx.send(embed=em)

    @help.command()
    async def confession(self, ctx):
        em = disnake.Embed(
            title="Matsuri's Confession",
            description="Sends Matsuri's confession to Fubuki",
        )
        await ctx.send(embed=em)

    @help.command()
    async def fortnite(self, ctx):
        em = disnake.Embed(
            title="Fortnite", description="Sends the fortnite dance in text"
        )
        await ctx.send(embed=em)

    @help.command(aliases=["e"])
    async def emote(self, ctx):
        em = disnake.Embed(
            title="Emote",
            description="Sends an animated emote from any server that this bot is in.",
        )
        em.add_field(name="**Syntax**", value="k.emote <emotename>")
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command(aliases=["ge"])
    async def getemotes(self, ctx):
        em = disnake.Embed(
            title="Get Emotes!",
            description="Sends all emotes that this bot has. It has emotes for all servers it's in.",
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command()
    async def wristworld(self, ctx):
        em = disnake.Embed(
            title="Wristworld", description="Sends the wristworld miku copypasta."
        )
        await ctx.send(embed=em)

    @help.command()
    async def fmega(self, ctx):
        em = disnake.Embed(
            title="F Mega!", description="Sends the F MEGA gif from Jojo's."
        )
        await ctx.send(embed=em)

    @help.command()
    async def kotowaru(self, ctx):
        em = disnake.Embed(
            title="Daga kotowaru!", description="Use this to refuse someone's offer"
        )
        await ctx.send(embed=em)

    @help.command()
    async def ascend(self, ctx):
        em = disnake.Embed(
            title="Ascend to Heaven!",
            description="Use this to to ascend when something glorious occurs.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def jizz(self, ctx):
        em = disnake.Embed(title="Jizz", description="Use this to jizz.")
        await ctx.send(embed=em)

    @help.command()
    async def letsgo(self, ctx):
        em = disnake.Embed(title="Let's go!", description="Playus 'Let's gooo' in vc")
        await ctx.send(embed=em)

    @help.command()
    async def vtubus(self, ctx):
        em = disnake.Embed(title="Vtubus", description="vtubus")
        await ctx.send(embed=em)

    @help.command()
    async def ding(self, ctx):
        em = disnake.Embed(
            title="Ding ding ding ding ding ddi di ding", description="amongus"
        )
        await ctx.send(embed=em)

    @help.command()
    async def yodayo(self, ctx):
        em = disnake.Embed(
            title="Yo dayo!", description="Plays Ayame's 'Yo dayo!' in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def yodazo(self, ctx):
        em = disnake.Embed(
            title="Yo dazo!", description="Plays Ayame's 'Yo dazo!' in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def jonathan(self, ctx):
        em = disnake.Embed(
            title="Jonathan's theme", description="Plays Jonathan's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def joseph(self, ctx):
        em = disnake.Embed(
            title="Joseph's theme", description="Plays Joseph's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def jotaro(self, ctx):
        em = disnake.Embed(
            title="Jotaro's theme", description="Plays Jotaro's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def josuke(self, ctx):
        em = disnake.Embed(
            title="Josuke's theme", description="Plays Josuke's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def giorno(self, ctx):
        em = disnake.Embed(
            title="Giorno's theme", description="Plays Giorno's theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def kira(self, ctx):
        em = disnake.Embed(
            title="Yoshikage Kira's theme",
            description="Plays Yoshikage Kira's theme in VC",
        )
        await ctx.send(embed=em)

    @help.command()
    async def pillarmen(self, ctx):
        em = disnake.Embed(
            title="Pillar Men Theme", description="Plays the Pillar Men Theme in VC"
        )
        await ctx.send(embed=em)

    @help.command()
    async def tts(self, ctx):
        em = disnake.Embed(
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
        em = disnake.Embed(
            title="Bad Apple but in custom emotes",
            description="Sends 80 animated emotes that all make up the Bad Apple PV (Only works on PC)",
        )
        em.add_field(name="**Emotes by:**", value="https://github.com/gohjoseph")
        await ctx.send(embed=em)

    @help.command()
    async def clip(self, ctx):
        em = disnake.Embed(
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
        em = disnake.Embed(
            title="Quickly clip a YT Video",
            description="clips a YouTube video given the start and end times (HH:MM:SS)\n**FASTER** than `clip` but will start at the nearest keyframe, so it'll start a couple seconds earlier than the given timestamp",
        )
        em.add_field(
            name="**Syntax**",
            value="k.fastclip <url> <start time> <end time> <filename>",
        )
        em.add_field(
            name="**Example**",
            value="k.fastclip https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:00:52 00:01:05 filename",
        )
        await ctx.send(embed=em)

    @help.command()
    async def fastclipsub(self, ctx):
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
            value="k.fastclipsub https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:00:52 00:01:05 filename",
        )
        await ctx.send(embed=em)

    @help.command()
    async def download(self, ctx):
        em = disnake.Embed(
            title="Download a YT Video", description="Download a YouTube of your choice"
        )
        em.add_field(name="**Syntax**", value="k.download <url>")
        await ctx.send(embed=em)

    @help.command()
    async def botansneeze(self, ctx):
        em = disnake.Embed(
            title="Botan Sneeze", description="because fuck you, have a botan sneeze"
        )
        em.add_field(name="**Syntax**", value="k.botansneeze [loop]")
        await ctx.send(embed=em)

    @help.command()
    async def boom(self, ctx):
        em = disnake.Embed(
            title="Vine Boom SFX", description="plays the funni boom sfx in vc"
        )
        await ctx.send(embed=em)

    @help.command(aliases=["ogei"])
    async def ogey(self, ctx):
        em = disnake.Embed(title="Ogey...", description="Plays Pekora's ogey in VC.")
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command()
    async def rrat(self, ctx):
        em = disnake.Embed(title="Rrat!", description="Plays Pekora's rrat in VC.")
        await ctx.send(embed=em)

    @help.command()
    async def fart(self, ctx):
        em = disnake.Embed(
            title="Reverb fart sfx", description="Plays funni fart sound in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    async def mogumogu(self, ctx):
        em = disnake.Embed(
            title="Mogu mogu!", description="Plays okayu's mogu mogu in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    async def bababooey(self, ctx):
        em = disnake.Embed(title="Bababooey!", description="Plays bababooey in VC.")
        await ctx.send(embed=em)

    @help.command()
    async def dog(self, ctx):
        em = disnake.Embed(
            title="What the dog doin?", description="Plays 'what da dog doin' in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    async def totsugeki(self, ctx):
        em = disnake.Embed(
            title="TOTSUGEKI!!!", description="Plays May's Totsugeki in VC."
        )
        await ctx.send(embed=em)

    @help.command(aliases=["bong"])
    async def tacobell(self, ctx):
        em = disnake.Embed(
            title="Taco Bell bong sfx",
            description="Plays the funny taco bell sound effect in VC.",
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command(aliases=["amogus"])
    async def amongus(self, ctx):
        em = disnake.Embed(
            title="AMONGUS!", description="Plays the guy yelling amongus in VC."
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command(aliases=["classtrial"])
    async def danganronpa(self, ctx):
        em = disnake.Embed(
            title="Class trial time!",
            description="Plays '議論 -HEAT UP-' from Danganronpa in VC.",
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command()
    async def join(self, ctx):
        em = disnake.Embed(title="Join VC", description="Sus bot will enter the VC.")
        await ctx.send(embed=em)

    @help.command()
    async def stop(self, ctx):
        em = disnake.Embed(
            title="STOP!",
            description="Sus bot will stop playing if it's playing something in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def stoploop(self, ctx):
        em = disnake.Embed(
            title="STOP THE LOOP!",
            description="Sus bot will stop playing if it's playing something in VC that has loop mode enabled.",
        )
        em.add_field(name="**How loop???**", value="k.commandname loop")
        await ctx.send(embed=em)

    @help.command()
    async def leave(self, ctx):
        em = disnake.Embed(
            title="Sayonara...", description="Sus bot will leave the VC."
        )
        await ctx.send(embed=em)

    @help.command()
    async def stream(self, ctx):
        em = disnake.Embed(
            title="YouTube Stream Time Embed",
            description="Sends an embed of a YouTube stream with its start time.",
        )
        em.add_field(name="**Syntax**", value="k.stream https://youtu.be/wNMW87foNAI")
        await ctx.send(embed=em)

    @help.command()
    async def water(self, ctx):
        em = disnake.Embed(
            title="Water and Water and Water Water",
            description="Plays 'Water and Water and Water Water'in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def necoarc(self, ctx):
        em = disnake.Embed(title="Neco arc", description="Plays neco arc in VC.")
        await ctx.send(embed=em)

    @help.command()
    async def vsauce(self, ctx):
        em = disnake.Embed(
            title="Vsauce music", description="Plays the vsauce music in VC."
        )
        await ctx.send(embed=em)

    @help.command()
    async def gigachad(self, ctx):
        em = disnake.Embed(
            title="Gigachad",
            description="Plays a bit of 'Can You Feel My Heart' in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def bruh(self, ctx):
        em = disnake.Embed(
            title="Rushia Bruh SFX",
            description="Plays Rushia saying bruh in VC.",
        )
        await ctx.send(embed=em)

    @help.command()
    async def believeit(self, ctx):
        em = disnake.Embed(
            title="Naruto - Believe it!",
            description='Plays Naruto saying "Believe it!" in VC. 82 variations.',
        )
        await ctx.send(embed=em)

    @help.command()
    async def pikamee(self, ctx):
        em = disnake.Embed(
            title="pikamee is insane",
            description='Plays a clip of Pikamee saying "Pikamee, how are you doing? I feel awesome. I killed everyone but I feel awesome."',
        )
        await ctx.send(embed=em)

    @help.command(aliases=["hellskitchen", "violin"])
    async def waterphone(self, ctx):
        em = disnake.Embed(
            title="Hell's Kitchen SFX",
            description="Plays the Hell's Kitchen sound effect.",
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command(aliases=["boo-womp"])
    async def boowomp(self, ctx):
        em = disnake.Embed(
            title="Boo-womp!",
            description="Plays the boo-womp sound effect that they play on Spongebob when something sad happens.",
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command()
    async def pet(self, ctx):
        em = disnake.Embed(
            title="Pet user",
            description="Sends a gif of the mentioned user being petted.",
        )
        em.add_field(
            name="**Syntax**", value="k.pet <mentioned user>\nk.pet <image url>"
        )
        await ctx.send(embed=em)

    @help.command(aliases=["findsauce", "getsauce"])
    async def sauce(self, ctx):
        em = disnake.Embed(
            title="Get sauce", description="Uses Saucenao API to find sauce."
        )
        em.add_field(
            name="**Syntax**",
            value="k.sauce <url>\nUpload image with k.sauce\nReply to a message with k.sauce ",
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command()
    async def clipaudio(self, ctx):
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
            value="k.clipaudio https://www.youtube.com/watch?v=UIp6_0kct_U 00:00:56 00:01:05 poger mp3",
        )
        await ctx.send(embed=em)

    @help.command()
    async def ping(self, ctx):
        em = disnake.Embed(
            title="Ping",
            description="Pings the bot. What else would this be lol.",
        )
        await ctx.send(embed=em)

    @help.command(aliases=["flip"])
    async def coinflip(self, ctx):
        em = disnake.Embed(
            title="Coin Flip",
            description="Flips a coin. That's it",
        )
        em.add_field(name="**Syntax**", value="k.coinflip  heads\nk.coinflip tails")
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command(aliases=["shitify", "pixelize"])
    async def lowqual(self, ctx):
        em = disnake.Embed(
            title="Low quality-ify",
            description="Aggressively downscales video or photo to 36x20px :sunglasses:",
        )
        em.add_field(
            name="**Syntax**",
            value="k.lowqual <url>\nUpload video/photo with k.lowqual\nReply to a video/photo message with k.lowqual ",
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command()
    async def when(self, ctx):
        em = disnake.Embed(
            title="When?",
            description="Tells you exactly when a YT video has been uploaded, or when a stream has started and ended",
        )
        em.add_field(name="**Syntax**", value="k.when <yt_url>")
        await ctx.send(embed=em)

    @help.command()
    async def checkcomment(self, ctx):
        em = disnake.Embed(
            title="YT Comment Checker",
            description="Give it a YT comment link and it will keep checking if it exists for the next 5 minutes. If it doesn't exist before then, it will ping you.",
        )
        em.add_field(name="**Syntax**", value="k.checkcomment <yt_comment_url>")
        await ctx.send(embed=em)

    @help.command(aliases=["akasupa", "supacha"])
    async def superchat(self, ctx):
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
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command(aliases=["oldakasupa", "oldsupacha"])
    async def oldsuperchat(self, ctx):
        em = disnake.Embed(
            title="Superchat! (OLD)",
            description="Old ver. of k.superchat. It just goes to a [site](https://ytsc.leko.moe/) that creates the image for you. ",
        )
        em.add_field(
            name="**Syntax**",
            value="k.oldsuperchat <amount with currency> <message>",
        )
        em.add_field(
            name="**Example**",
            value="k.oldsuperchat $100 poggers",
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command(aliases=["vid2gif", "gifify"])
    async def gif(self, ctx):
        em = disnake.Embed(
            title="Video to Gif",
            description="Converts a video to GIF. Doesn't work with YouTube URLs yet.",
        )
        em.add_field(
            name="**Syntax**",
            value="k.gif <video_url>\nUpload video with k.gif\nReply to a video with k.gif ",
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command(aliases=["vid2gif2", "gifify2"])
    async def gif2(self, ctx):
        em = disnake.Embed(
            title="Video to Gif 2",
            description="k.gif but higher quality and slower",
        )
        em.add_field(
            name="**Syntax**",
            value="k.gif2 <video_url>\nUpload video with k.gif2\nReply to a video with k.gif2 \n\nOptional: you can add include quality (1-100) at the end of the command. Default: 70",
        )
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        await ctx.send(embed=em)

    @help.command()
    async def resize(self, ctx):
        em = disnake.Embed(
            title="Resize image",
            description="Resizes an image to a given resolution",
        )
        em.add_field(
            name="**Syntax**",
            value="k.resize <width> <height> <link>\nYou can also leave <link> blank and just upload or reply to an image.",
        )
        await ctx.send(embed=em)

    def paginate(self, lines, chars=4096):
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

    @help.command()
    async def mgr(self, ctx):
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
        for root, dirs, files in os.walk("sounds/mgr/", topdown=False):
            for name in dirs:
                mgr_list += f"**{name}:**\n"
                mgr_list += '\n'.join([f"- {x.split('.')[0]}" for x in os.listdir(f"sounds/mgr/{name}")])
                mgr_list += '\n\n'   
        embed = disnake.Embed()
        for index, message in enumerate(self.paginate(mgr_list)):
            if index == 0:
                embed.title = "Sounds (you can enter a part of the name)"
            else:
                embed.title = ""
            embed.description = "".join(message)
            await ctx.send(embed=embed)        

    @help.command(aliases=["us"])
    async def uploadsticker(self, ctx):
        em = disnake.Embed(
            title="Upload sticker",
            description="Uploads an image as a sticker.",
        )
        em.add_field(name="**Syntax**", value="k.uploadsticker <name> <emoji as text> <url>\nUpload image with k.uploadsticker <name> <emoji as text>\nReply to a message with k.uploadsticker <name> <emoji as text>",inline=False)
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        em.add_field(
            name="**Example**",
            value="k.uploadsticker agony cry https://cdn.discordapp.com/attachments/812666551051747369/983132328945680434/IMG_1963.jpg",
        )        
        await ctx.send(embed=em)

    @help.command(aliases=["uploademoji","ue"])
    async def uploademote(self, ctx):
        em = disnake.Embed(
            title="Upload emote",
            description="Uploads an image as an emote.",
        )
        em.add_field(name="**Syntax**", value="k.uploademote <name> <url\emote ID>\nUpload image with k.uploademote <name>\nReply to a message with k.uploademote <name>",inline=False)
        em.add_field(name="**Aliases**", value=",".join(ctx.command.aliases))
        em.add_field(
            name="**Example**",
            value="k.uploademote stuff https://cdn.discordapp.com/attachments/809247468084133898/985504342461280306/stuff.png",
        )        
        await ctx.send(embed=em)
        
def setup(client):
    client.add_cog(Help(client))

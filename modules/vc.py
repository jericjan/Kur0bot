# followed this https://gist.github.com/15696/a1b10f044fbd658ce76ab1f862a1bda2
# client becomes self.client

from disnake.ext import commands
import disnake
import random
import os

may_sounds = ["sounds/totsugeki_7UWR0L4.mp3", "sounds/totsugeki-may-2.mp3"]


class Vc(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def vcplay(self, ctx, a, loop=None, isRandom=None):
   
        voicestate = ctx.author.voice
        if voicestate:
            voice_channel = ctx.author.voice.channel

        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voicestate != None:

            if voice == None:
                voice = await voice_channel.connect()
            if loop == "loop":

                    def loop():
                      if isRandom == True:
                        b = random.choice(a)  
                        voice.play(
                            disnake.FFmpegPCMAudio(source=b), after=lambda e: loop()
                        )                        
                      else:
                        
                        voice.play(
                            disnake.FFmpegPCMAudio(source=a), after=lambda e: loop()
                        )

                    loop()
            else:
                if isRandom == True:
                  a = random.choice(a)                  
                voice.play(disnake.FFmpegPCMAudio(source=a))

        else:
            # await ctx.send(f"{ctx.author.name} is not in a channel.")
            await ctx.send(
                f"{ctx.author.name} is not in a VC. Sending file instead...",
                delete_after=3,
            )

            if isRandom == True:
              a = random.choice(a)         
            print(f"playing {a}")
            print(f"filename is: {a.split('/')[-1]}")              
            await ctx.send(file=disnake.File(a, filename=a.split("/")[-1]))
        # Delete command after the audio is done playing.
        await ctx.message.delete()

    @commands.command()
    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
        await ctx.send("Sus bot has joined the call.", delete_after=3.0)
        await ctx.message.delete()

    @commands.command()
    async def stop(self, ctx):
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
    async def stoploop(self, ctx):
        await ctx.guild.voice_client.disconnect()
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
        await ctx.send("The loop has been stopped.", delete_after=3.0)
        await ctx.message.delete()

    @commands.command()
    async def letsgo(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/vibez-lets-go.mp3", loop)

    @commands.command()
    async def vtubus(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/vtubus.mp3", loop)

    @commands.command()
    async def giorno(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/giorno theme.mp3", loop)

    @commands.command()
    async def ding(self, ctx, loop=None):
        await self.vcplay(
            ctx, "sounds/DING DING DING DING DING DING DING DI DI DING.mp3", loop
        )

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:  # If the bot is in a voice channel
            await ctx.guild.voice_client.disconnect()  # Leave the channel
            await ctx.send("Sus bot has left the call.", delete_after=3.0)
            #  await asyncio.sleep(0.3)
            await ctx.message.delete()
        else:  # But if it isn't
            await ctx.send(
                "I'm not in a voice channel, use the join command to make me join",
                delete_after=3.0,
            )
        # await ctx.message.delete()

    @commands.command()
    async def yodayo(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/Nakiri Ayame's yo dayo_.mp3", loop)

    @commands.command()
    async def yodazo(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/Yo Dazo!.mp3", loop)

    @commands.command()
    async def jonathan(self, ctx, loop=None):
        await self.vcplay(
            ctx, "sounds/Jonathan's theme but its only the BEST part.mp3", loop
        )

    @commands.command()
    async def joseph(self, ctx, loop=None):
        await self.vcplay(
            ctx, "sounds/Joseph's theme but only the good part (1).mp3", loop
        )

    @commands.command()
    async def jotaro(self, ctx, loop=None):
        await self.vcplay(
            ctx, "sounds/Jotaro’s theme but it’s only the good part.mp3", loop
        )

    @commands.command()
    async def josuke(self, ctx, loop=None):
        await self.vcplay(
            ctx, "sounds/Josuke theme but it's only the good part.mp3", loop
        )

    @commands.command()
    async def kira(self, ctx, loop=None):
        await self.vcplay(
            ctx,
            "sounds/Killer (Yoshikage Kira's Theme) - Jojo's Bizarre Adventure Part 4_ Diamond Is Unbreakable.mp3",
            loop,
        )

    @commands.command()
    async def pillarmen(self, ctx, loop=None):
        await self.vcplay(
            ctx, "sounds/Jojo's Bizarre Adventure- Awaken(Pillar Men Theme).mp3", loop
        )

    @commands.command()
    async def boom(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/boom.mp3", loop)

    @commands.command(aliases=["ogei"])
    async def ogey(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/ogey.mp3", loop)

    @commands.command()
    async def rrat(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/rrat.mp3", loop)

    @commands.command()
    async def fart(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/fart.mp3", loop)

    @commands.command()
    async def mogumogu(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/mogu.mp3", loop)

    @commands.command()
    async def bababooey(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/bababooey.mp3", loop)

    @commands.command()
    async def dog(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/dog.mp3", loop)

    @commands.command()
    async def totsugeki(self, ctx, loop=None):
        await self.vcplay(ctx, may_sounds, loop, True)      

    @commands.command(aliases=["bong"])
    async def tacobell(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/tacobell.mp3", loop)

    @commands.command(aliases=["amogus"])
    async def amongus(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/amongus.mp3", loop)

    @commands.command(aliases=["classtrial"])
    async def danganronpa(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/danganronpa.mp3", loop)

    @commands.command()
    async def botansneeze(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/botansneeze.mp3", loop)

    @commands.command()
    async def water(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/water.mp3", loop)

    @commands.command()
    async def necoarc(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/necoarc.mp3", loop)

    @commands.command()
    async def vsauce(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/vsauce.mp3", loop)

    @commands.command()
    async def gigachad(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/gigachad.mp3", loop)

    @commands.command()
    async def bruh(self, ctx, loop=None):
        await self.vcplay(ctx, "sounds/rushiabruh.mp3", loop)

    @commands.command()
    async def believeit(self, ctx, loop=None):
        believeit_files = os.listdir('sounds/believeit/')
        believeit_files = [f"sounds/believeit/{x}" for x in believeit_files]
        await self.vcplay(ctx, believeit_files, loop, True)
def setup(client):
    client.add_cog(Vc(client))

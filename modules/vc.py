# followed this https://gist.github.com/15696/a1b10f044fbd658ce76ab1f862a1bda2
# client becomes self.client

from discord.ext import commands
import discord
import random

may_sounds = ["sounds/totsugeki_7UWR0L4.mp3", "sounds/totsugeki-may-2.mp3"]


class Vc(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def vcplay(self, ctx, a, loop=None):
        voice_channel = ctx.author.voice.channel
        channel = None
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice_channel != None:
            channel = voice_channel.name
            if voice == None:
                vc = await voice_channel.connect()
                if loop == "loop":

                    def loop():
                        vc.play(
                            discord.FFmpegPCMAudio(source=a), after=lambda e: loop()
                        )

                    loop()
                else:
                    vc.play(discord.FFmpegPCMAudio(source=a))
            else:
                if loop == "loop":

                    def loop2():
                        voice.play(
                            discord.FFmpegPCMAudio(source=a), after=lambda e: loop2()
                        )

                    loop2()
                else:
                    voice.play(discord.FFmpegPCMAudio(source=a))
        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")
        # Delete command after the audio is done playing.
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
        await self.vcplay(ctx, random.choice(may_sounds), loop)

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


def setup(client):
    client.add_cog(Vc(client))

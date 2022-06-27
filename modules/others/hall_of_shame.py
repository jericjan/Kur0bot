from disnake.ext import commands
import disnake
import json

class Hall_Of_Shame(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hallofshame(self, ctx, channel=None):
        hall_of_shame_json = json.load(open("modules/others/hall_of_shame_ids.json"))
        if channel == None:
            await ctx.send("Give the channel ID for the hall of shame.")
            return     
        elif channel == "remove" or channel == "delete":
            await ctx.send(f"<#{hall_of_shame_json[str(ctx.guild.id)]}> removed.")
            hall_of_shame_json.pop(str(ctx.guild.id))             
        else:
            converter = commands.TextChannelConverter()
            try:
                channel = await converter.convert(ctx, channel)
            except commands.ChannelNotFound:
                await ctx.send(f"Dawg. {channel} ain't a channel.")
                return   
            em = disnake.Embed(
                title="The Hall Of Shame",
                description="These are the 10 recent players who have committed the cringe AKA playing league."
            )
            new_embed = await channel.send(embed=em)      
            hall_of_shame_json[str(ctx.guild.id)] = {}
            hall_of_shame_json[str(ctx.guild.id)]['channel-id'] = channel.id      
            hall_of_shame_json[str(ctx.guild.id)]['embed-id'] = new_embed.id      
            await ctx.send(f"<#{channel.id}> is now the Hall Of Shame!")
        with open(f"modules/others/hall_of_shame_ids.json", 'w') as f:
            f.write(json.dumps(hall_of_shame_json))    
        
    # @commands.command()
    # async def getfields(self, ctx, msg: disnake.Message):
        # embed = msg.embeds[0]
        # fields = embed.fields
        # name_list = [i.name for i in fields]
        # for i in fields:
            # await ctx.send(i.name)
    
    # @commands.command()
    # async def removefield(self, ctx, msg: disnake.Message, index):
        # embed = msg.embeds[0]
        # embed.remove_field(int(index))
        # await msg.edit(embed=embed)
    
    # @commands.command()
    # async def editdesc(self, ctx, msg: disnake.Message, new_desc):    
        # embed = msg.embeds[0]
        # embed.description = new_desc
        # await msg.edit(embed=embed)
    
def setup(client):
    client.add_cog(Hall_Of_Shame(client))

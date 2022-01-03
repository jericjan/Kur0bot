from discord.ext import commands, pages
import discord
import asyncio
from saucenao_api import SauceNao
import os
import re


class Sauce(commands.Cog):
    @commands.command(aliases=["findsauce", "sauce"])
    async def getsauce(self, ctx, link=None):

        if link == None:
            print(ctx.message.attachments)  # a list
            print(ctx.message.reference)
            if ctx.message.attachments:  # message has images
                print("is attachment")
                link = ctx.message.attachments[0].url
            elif ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                if msg.attachments:  # if replied has image
                    link = msg.attachments[0].url
                elif msg.embeds:  # if replied has link
                    link = msg.embeds[0].url

                # print("embmeds: {0}".format(msg.embeds))
                # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
                #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
                # link= msg.attachments[0].url
                else:
                    await ctx.send("the message you replied to has no image, baka!")
            else:
                await ctx.send("you did something wrong. brug. try again.")
                return
            print(link)

        msg = await ctx.send("Getting sauce...")
        sauce = SauceNao(os.getenv("SAUCENAO_KEY"))
        try:
            results = sauce.from_url(link)  # or from_file()
            print(f"30S: {results.short_remaining}")
            print(f"24H: {results.long_remaining}")
            await msg.edit(
                content=f"30s limit: {results.short_remaining} request(s) left\n24h limit: {results.long_remaining} request(s) left",
                delete_after=5,
            )
        except Exception as e:
            await msg.edit(f"I fail. Reason:\n{e}")
            return
        print(f"{len(results)} results!")
        result_count = len(results)
        results_dict = {}
        embed_dict = {}
        i = 0
        while i < result_count:
            results_dict[i] = results[i]
            i += 1
            print(len(results_dict))
        for i in range(len(results_dict)):
            # await ctx.send(results_dict[i].title)
            try:
                site_name = re.search(r"(?<=https:\/\/)[^\/]*", results_dict[i].urls[0])
                embed_dict[i] = discord.Embed(
                    title=results_dict[i].title,
                    description=f"{results_dict[i].similarity}% accurate",
                    url=results_dict[i].urls[0],
                )
                embed_dict[i].set_author(name=results_dict[i].author)
                embed_dict[i].set_image(url=results_dict[i].thumbnail)
                embed_dict[i].set_footer(text=site_name[0])
            except IndexError:
                embed_dict[i] = discord.Embed(
                    title=results_dict[i].title,
                    description=f"{results_dict[i].similarity}% accurate",
                )
                embed_dict[i].set_author(name=results_dict[i].author)
                embed_dict[i].set_image(url=results_dict[i].thumbnail)
            #  embed_dict[i].set_footer(text="{0}/{1}".format(i+1,result_count))
            except Exception as e:
                print(e)
            # try:
            #   await msg.delete()
            # except:
            #   pass
            # button1 = Button(label="Previous")
            # button2 = Button(label="Next")

            # async def prev_callback(interaction):
            #   await interaction.response.send_message() #i want it to send outside_var

            # button1.callback = prev_callback()
            # view= View()
            # view.add_item(button1)
            # view.add_item(button2)
        paginator = pages.Paginator(pages=embed_dict)
        await paginator.send(ctx)
        # await ctx.send(embed=embed_dict[i],view=view)
        # await buttons.send(
        # channel = ctx.channel.id,
        # content = None,
        # embed = embed_dict[i],
        # components = [
        # ActionRow([
        # Button(
        #   style = ButtonType().Secondary,
        #   label = "Previous",
        #   custom_id = "previous"
        #       ),
        # Button(
        #   style = ButtonType().Secondary,
        #   label = "Next",
        #   custom_id = "next"
        #       )
        # ])
        # ])

        # await ctx.send(embed = e)


def setup(client):
    client.add_cog(Sauce(client))

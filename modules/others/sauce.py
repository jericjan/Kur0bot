import os
import re
from typing import Any, Optional

import aiohttp
import disnake
from disnake.ext import commands
from saucenao_api import SauceNao  # type: ignore
from saucenao_api.containers import BasicSauce  # type: ignore
from myfunctions import msg_link_grabber

from ..paginator import ButtonPaginator


class Sauce(commands.Cog):
    @commands.command()
    async def altsauce(self, ctx: commands.Context[Any], link: Optional[str]=None):
        link = await msg_link_grabber.grab_link(ctx, link)
        print(link)
        api_key = os.getenv("SAUCENAO_KEY")
        api_url = f"https://saucenao.com/search.php?api_key={api_key}&db=999&output_type=2&numres=6&url={link}"
        msg = await ctx.send("Getting sauce...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as resp:
                    sauce_json = await resp.json()
            short_remaining = sauce_json["header"]["short_remaining"]
            long_remaining = sauce_json["header"]["long_remaining"]
            status = sauce_json["header"]["status"]
            status_meaning = ""
            if status == 0:
                status_meaning = "Success!"
            elif status > 0:
                status_meaning = "Server-side error!"
            elif status < 0:
                status_meaning = "Client-side error!"
            print(f"30S: {short_remaining}")
            print(f"24H: {long_remaining}")
            await msg.edit(
                content=f"Status ({status}): {status_meaning}\n"
                f"30s limit: {short_remaining} request(s) left\n"
                f"24h limit: {long_remaining} request(s) left",
                delete_after=5,
            )
        except Exception as e:
            await msg.edit(f"I fail. Reason:\n{e}")
            return
        results = sauce_json["results"]
        print(f"{len(results)} results!")
        embed_dict: dict[int, disnake.Embed] = {}
        for idx, val in enumerate(results):
            print(f"this thing is:\n{val}")
            title = val["data"]["title"]
            description = f"{val['header']['similarity']}% accurate"
            try:
                author = val["data"]["author_name"]
            except:
                author = val["data"]["member_name"]
            image = val["header"]["thumbnail"]
            try:
                urls = val["data"]["ext_urls"][0]
                site_name = re.search(r"(?<=https:\/\/)[^\/]*", urls)
                embed_dict[idx] = disnake.Embed(
                    title=title,
                    description=description,
                    url=urls,
                )
                embed_dict[idx].set_author(name=author)
                embed_dict[idx].set_image(url=image)
                embed_dict[idx].set_footer(text="" if site_name is None else site_name[0])
            except Exception as e:
                print(e)

        embed_list = list(embed_dict.values())

        paginator = ButtonPaginator(segments=embed_list)
        await paginator.send(ctx)

    @commands.command(aliases=["findsauce", "getsauce"])
    async def sauce(self, ctx: commands.Context[Any], link: Optional[str]=None):

        link = await msg_link_grabber.grab_link(ctx, link)
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
            await msg.edit(f"I fail. Reason:\n{e}\n\nTrying other option...")
            await self.altsauce(ctx, link)
            return
        print(f"{len(results)} results!")
        result_count = len(results)
        results_dict: dict[int, BasicSauce] = {}
        embed_dict: dict[int, disnake.Embed] = {}
        i = 0
        while i < result_count:
            results_dict[i] = results[i]
            i += 1
            print(len(results_dict))
        for i in range(len(results_dict)):
            try:
                site_name = re.search(r"(?<=https:\/\/)[^\/]*", results_dict[i].urls[0])
                embed_dict[i] = disnake.Embed(
                    title=results_dict[i].title,
                    description=f"{results_dict[i].similarity}% accurate",
                    url=results_dict[i].urls[0],
                )
                embed_dict[i].set_author(name=results_dict[i].author)
                embed_dict[i].set_image(url=results_dict[i].thumbnail)
                embed_dict[i].set_footer(text="" if site_name is None else site_name[0])
            except IndexError:
                embed_dict[i] = disnake.Embed(
                    title=results_dict[i].title,
                    description=f"{results_dict[i].similarity}% accurate",
                )
                embed_dict[i].set_author(name=results_dict[i].author)
                embed_dict[i].set_image(url=results_dict[i].thumbnail)
            except Exception as e:
                print(e)

        embed_list = list(embed_dict.values())

        paginator = ButtonPaginator(segments=embed_list)
        await paginator.send(ctx)


def setup(client: commands.Bot):
    client.add_cog(Sauce(client))

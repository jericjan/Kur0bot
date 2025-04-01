import aiohttp
from disnake.ext import commands
import disnake
import os
from modules.paginator import ButtonPaginator
from typing import Any

class GoogleSearch(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def google(self, ctx: commands.Context[Any], *, search_query):
        api_key = os.getenv("CUSTOM_SEARCH_KEY")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://customsearch.googleapis.com/customsearch/v1?cx=8277c214a2b6a4b56&q={search_query}&key={api_key}"
            ) as resp:
                response = await resp.json()
                if resp.status != 200:
                    await ctx.send(response)
                    return
        items = response.get("items")
        desc = [
            f"[{x.get('title')}]({x.get('link')})\n{x.get('snippet')}" for x in items
        ]

        split_into = 2
        desc_splitted = [
            desc[i : i + split_into] for i in range(0, len(desc), split_into)
        ]

        embed_list = [
            disnake.Embed(
                title="le google",
                description="\n".join(desc),
            )
            for desc in desc_splitted
        ]
        paginator = ButtonPaginator(segments=embed_list)
        await paginator.send(ctx)
        # await ctx.send(embed=em)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def image(self, ctx: commands.Context[Any], *, search_query):
        api_key = os.getenv("SERPAPI_KEY")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://serpapi.com/search.json?q={search_query}&engine=google_images&ijn=0&api_key={api_key}"
            ) as resp:
                response = await resp.json()
                if resp.status != 200:
                    await ctx.send(response)
                    return
        img_results = response.get("images_results")
        links = [x.get("link") for x in img_results]
        thumbnails = [x.get("thumbnail") for x in img_results]
        titles = [x.get("title") for x in img_results]

        def embed_with_img(embed, img_url):
            embed.set_image(url=img_url)
            return embed

        embed_list = [
            embed_with_img(
                disnake.Embed(
                    title="le images",
                    description=f"[{title}]({link})",
                ),
                thumb,
            )
            for link, thumb, title in zip(links, thumbnails, titles)
        ]
        paginator = ButtonPaginator(segments=embed_list)
        await paginator.send(ctx)


def setup(client: commands.Bot):
    client.add_cog(GoogleSearch(client))

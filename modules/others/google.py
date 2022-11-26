import aiohttp
from disnake.ext import commands
import disnake
import os
from modules.paginator import ButtonPaginator


class GoogleSearch(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def google(self, ctx, *, search_query):
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


def setup(client):
    client.add_cog(GoogleSearch(client))

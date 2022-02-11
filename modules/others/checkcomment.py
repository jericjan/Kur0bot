from disnake.ext import commands
import time
import re
import requests
import os
import asyncio


class CheckComment(commands.Cog):
    @commands.command()
    async def checkcomment(self, ctx, link):
        comment_start_time = time.time()
        comment_end_time = comment_start_time + (60 * 5)

        if re.search(r"https:\/\/www.youtube.com\/watch\?v=.+&lc=.+(\..+)?", link):
            id = re.search(
                r"(?<=https:\/\/www.youtube.com\/watch\?v=.{11}&lc=).+(\..+)?", link
            ).group(0)
        else:
            await ctx.send("Not a YT comment link!", delete_after=3.0)
            return
        print(id)

        params = {
            "part": "snippet",
            "key": os.getenv("YT_API_KEY"),
            "id": id,
        }
        url = "https://youtube.googleapis.com/youtube/v3/comments"
        msg = await ctx.send("Searching...")
        while time.time() < comment_end_time:
            r = requests.get(url, headers=None, params=params)
            time_passed = time.time() - comment_start_time
            if r.status_code == 200:
                try:
                    name = r.json()["items"][0]["snippet"][
                        "authorDisplayName"
                    ]  # DON'T REMOVE
                    comment_content = r.json()["items"][0]["snippet"][
                        "textOriginal"
                    ]  # DON'T REMOVE
                    print(f"{name}: {comment_content[:15]}...")
                    await msg.edit(
                        content=f"{time_passed:.2f}s: We're good! ({r.status_code})"
                    )
                except:
                    await msg.edit(
                        content=f"{time_passed:.2f}s: FAIL! {ctx.author.mention}"
                    )
                    return
            else:
                await msg.edit(
                    content=f"{time_passed:.2f}s: FAIL! ({r.status_code}) {ctx.author.mention}"
                )
                return
            await asyncio.sleep(10)
        await msg.edit(content=f"{time_passed:.2f} seconds passed and it's still up!")


def setup(client):
    client.add_cog(CheckComment(client))

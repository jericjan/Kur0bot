import os
from typing import Any, Optional

import aiohttp
import dateutil.parser as dp
import disnake
from disnake.ext import commands

from myfunctions import msg_link_grabber


class When(commands.Cog):
    async def grab_msg_time(self, msg: disnake.Message | disnake.DeletedReferencedMessage | None):
        if not isinstance(msg, disnake.Message):
            return "Message not found or deleted."
        time = msg.created_at
        return time.strftime("%b %-d, %Y - %I:%M:%S.%f %p %Z")

    @commands.command()
    async def when(self, ctx: commands.Context[Any], link: Optional[str]=None):
        try:
            link = await msg_link_grabber.grab_link(ctx, link)
        except:
            pass
        print(link)
        if link:
            if link.startswith("https://youtu.be"):
                idd = link.split("/")[-1].split("?")[0]
            elif link.startswith("https://www.youtube.com/"):
                idd = link.split("=")[1].split("&")[0]
            else:
                await ctx.send("Not a YT link!", delete_after=3.0)
                if ctx.message.reference:
                    await ctx.send(
                        "Gonna get time message was posted tho cuz yes...",
                        delete_after=3.0,
                    )
                    time = await self.grab_msg_time(ctx.message.reference.resolved)
                    await ctx.send(time)
                return
        else:
            if ctx.message.reference:
                await ctx.send(
                    "You replied to a message & it has no link, getting time message posted instead...",
                    delete_after=3.0,
                )
                time = await self.grab_msg_time(ctx.message.reference.resolved)
                await ctx.send(time)
            return
        
        if (yt_api_key := os.getenv("YT_API_KEY")) is None:
            await ctx.send(
                "YouTube API key not set. Please set the YT_API_KEY environment variable."
            )
            return

        params: dict[str, str] = {
            "part": "snippet,liveStreamingDetails",
            "key": yt_api_key,
            "id": idd,
        }
        url = "https://www.googleapis.com/youtube/v3/videos"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                r = await resp.json()
        publish_time = r["items"][0]["snippet"]["publishedAt"]
        epoch_time = dp.parse(publish_time).timestamp()
        await ctx.send(f"Video was published at <t:{epoch_time:.0f}:F>")
        if "liveStreamingDetails" in r["items"][0].keys():
            stream_details = r["items"][0]["liveStreamingDetails"]

            if "actualStartTime" in stream_details.keys():
                stream_start = stream_details["actualStartTime"]
                epoch_stream_start = (
                    f"<t:{dp.parse(stream_start).timestamp():.0f}:F>"
                )
            else:
                epoch_stream_start = "**Not started yet.**"
            if "actualEndTime" in stream_details.keys():
                stream_end = stream_details["actualEndTime"]
                epoch_stream_end = f"<t:{dp.parse(stream_end).timestamp():.0f}:F>"
            else:
                epoch_stream_end = "**Not ended yet.**"

            if "scheduledStartTime" in stream_details.keys():
                stream_schedule = stream_details["scheduledStartTime"]
                epoch_stream_schedule = (
                    f"<t:{dp.parse(stream_schedule).timestamp():.0f}:F>"
                )
            else:
                epoch_stream_schedule = "**No scheduled start time**"
            await ctx.send(
                f"Stream started at {epoch_stream_start}\nStream ended at {epoch_stream_end}\nStream was schedule to start at {epoch_stream_schedule}"
            )

def setup(client: commands.Bot):
    client.add_cog(When(client))

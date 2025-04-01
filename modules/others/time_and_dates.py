from datetime import datetime, timedelta
from typing import Any

import disnake
import pytz
from disnake.ext import commands


class TimeAndDates(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    def remove_dupes(self, x):
        return list(set(x))

    def get_current_days(self, show_date=True):
        self.last_tz = datetime.now(pytz.timezone("Etc/GMT+12"))
        self.first_tz = datetime.now(pytz.timezone("Etc/GMT-14"))
        other_tz = datetime.now(
            pytz.timezone("Etc/GMT-12")
        )  # signs are opposite btw (this is UTC+12)

        tz_str_list = [
            self.last_tz,
            self.first_tz,
            other_tz,
        ]
        tz_day_list = self.remove_dupes(
            [x.strftime("%b %-d (%A)" if show_date else "%A") for x in tz_str_list]
        )
        return tz_day_list

    def get_date_boundary(self, mode, weekday=None):
        """
        bad code but pls run get_current_days() first to update those vars
        """
        days = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]

        if weekday and weekday not in days:
            raise Exception("invalid weekday given")

        addend = ((days.index(weekday) - self.last_tz.weekday()) % 7) if weekday else 1
        addend = timedelta(days=addend)
        if mode == "end":  # UTC-12
            return (self.last_tz + addend).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        #           return datetime(
        #               self.last_tz.year,
        #               self.last_tz.month,
        #               self.last_tz.day + addend,
        #               tzinfo=pytz.timezone("Etc/GMT+12"),
        #           )
        elif mode == "start":  # UTC+14
            return (self.first_tz + addend).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        #           return datetime(
        #               self.first_tz.year,
        #               self.first_tz.month,
        #               self.first_tz.day + addend,
        #               tzinfo=pytz.timezone("Etc/GMT-14"),
        #           )
        else:
            raise Exception("wrong mode given!")

    def tz_to_discord_timestamp(self, tz):
        return f"<t:{int(tz.timestamp())}:R>"

    @commands.command()
    async def day(self, ctx: commands.Context[Any]):
        tz_day_list = self.get_current_days()
        day_ends = self.get_date_boundary("end")
        day_starts = self.get_date_boundary("start")

        last_day = self.last_tz.strftime("%b %-d")
        day_ends_epoch = self.tz_to_discord_timestamp(day_ends)

        first_day = day_starts.strftime("%b %-d")
        day_starts_epoch = self.tz_to_discord_timestamp(day_starts)

        await ctx.send(
            f"It is currently {' and '.join(tz_day_list)}\n"
            f"{last_day} leaves the world {day_ends_epoch}\n"
            f"{first_day} enters the world {day_starts_epoch}"
        )


def setup(client: commands.Bot):
    client.add_cog(TimeAndDates(client))

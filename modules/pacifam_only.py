import io
import json
import os
import re
from ftplib import FTP
from typing import Any

import disnake
from disnake.ext import commands
from mcrcon import MCRcon  # type: ignore


class PacifamOnly(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def addoffline(self, ctx: commands.Context[Any], username: str):
        avi_guild = self.client.get_guild(938255956247183451)
        while avi_guild is None:
            pass
        admin = disnake.utils.get(avi_guild.roles, name="Admin")
        moderator = disnake.utils.get(avi_guild.roles, name="Moderator")
        avilon = disnake.utils.get(avi_guild.roles, name="Aweelom")
        roles = [admin, moderator, avilon]
        if not isinstance(ctx.author, disnake.Member):
            await ctx.send(f"You can't use this command in DMs!")
            return
        if (
            any(role in roles for role in ctx.author.roles)
            or ctx.author.id == 216830153441935360
        ):
            await ctx.send(f"Adding {username} to list of offline users...")

            ftp = FTP(host="us28.pebblehost.com")
            if (email := os.getenv("PEBBLE_EMAIL")) is None or (passwd := os.getenv("PEBBLE_PASS")) is None:
                await ctx.send("Pebblehost credentials missing.")
                return
            
            ftp.login(user=email, passwd=passwd)
            r = io.BytesIO()
            ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
            config = json.loads(r.getvalue())
            if username.lower() in config["main"]["forcedOfflinePlayers"]:
                await ctx.send(f"{username} is alreading in the list!")
                return
            config["main"]["forcedOfflinePlayers"].append(username.lower())
            print(config["main"]["forcedOfflinePlayers"])
            dump = json.dumps(config, indent=2).encode("utf-8")
            ftp.storbinary("STOR /mods/EasyAuth/config.json", io.BytesIO(dump))

            with MCRcon("51.81.142.14", str(os.getenv("RCON_PASS")), 8082) as mcr:
                resp = mcr.command("/auth reload")  # type: ignore
                print(resp)
            await ctx.send("Done!")

        else:
            await ctx.send("Only Admins/Mods can use this command")

    @commands.command()
    async def viewoffline(self, ctx: commands.Context[Any]):
        avi_guild = self.client.get_guild(938255956247183451)
        while avi_guild is None:
            pass
        admin = disnake.utils.get(avi_guild.roles, name="Admin")
        moderator = disnake.utils.get(avi_guild.roles, name="Moderator")
        avilon = disnake.utils.get(avi_guild.roles, name="Aweelom")
        roles = [admin, moderator, avilon]
        if not isinstance(ctx.author, disnake.Member):
            await ctx.send(f"You can't use this command in DMs!")
            return        
        if (
            any(role in roles for role in ctx.author.roles)
            or ctx.author.id == 216830153441935360
        ):

            ftp = FTP(host="us28.pebblehost.com")
            if (email := os.getenv("PEBBLE_EMAIL")) is None or (passwd := os.getenv("PEBBLE_PASS")) is None:
                await ctx.send("Pebblehost credentials missing.")
                return            
            ftp.login(user=email, passwd=passwd)
            r = io.BytesIO()
            ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
            config = json.loads(r.getvalue())
            print(config["main"]["forcedOfflinePlayers"])
            await ctx.send(
                f"Players added to the offline list are: "
                f"{', '.join(config['main']['forcedOfflinePlayers'])}"
            )
        else:
            await ctx.send("Only Admins/Mods can use this command")

    @commands.command()
    async def removeoffline(self, ctx: commands.Context[Any], username: str):
        avi_guild = self.client.get_guild(938255956247183451)
        while avi_guild is None:
            pass
        admin = disnake.utils.get(avi_guild.roles, name="Admin")
        moderator = disnake.utils.get(avi_guild.roles, name="Moderator")
        avilon = disnake.utils.get(avi_guild.roles, name="Aweelom")
        roles = [admin, moderator, avilon]
        if not isinstance(ctx.author, disnake.Member):
            await ctx.send(f"You can't use this command in DMs!")
            return        
        if (
            any(role in roles for role in ctx.author.roles)
            or ctx.author.id == 216830153441935360
        ):
            await ctx.send(f"Removing {username} from list of offline users...")

            ftp = FTP(host="us28.pebblehost.com")
            if (email := os.getenv("PEBBLE_EMAIL")) is None or (passwd := os.getenv("PEBBLE_PASS")) is None:
                await ctx.send("Pebblehost credentials missing.")
                return            
            ftp.login(user=email, passwd=passwd)
            r = io.BytesIO()
            ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
            config = json.loads(r.getvalue())
            if username.lower() in config["main"]["forcedOfflinePlayers"]:
                config["main"]["forcedOfflinePlayers"].remove(username.lower())
            else:
                await ctx.send(f"{username} isn't in the list!")
                return
            print(config["main"]["forcedOfflinePlayers"])
            dump = json.dumps(config, indent=2).encode("utf-8")
            ftp.storbinary("STOR /mods/EasyAuth/config.json", io.BytesIO(dump))

            with MCRcon("51.81.142.14", str(os.getenv("RCON_PASS")), 8082) as mcr:
                resp = mcr.command("/auth reload")  # type: ignore
                print(resp)
            await ctx.send("Done!")

        else:
            await ctx.send("Only Admins/Mods can use this command")

    @commands.command()
    async def viewmods(self, ctx: commands.Context[Any]):
        if ctx.guild is None or ctx.guild.id != 938255956247183451:
            await ctx.send("This command can only be used in the pacifam server.")
            return
        ftp = FTP(host="us28.pebblehost.com")
        if (email := os.getenv("PEBBLE_EMAIL")) is None or (passwd := os.getenv("PEBBLE_PASS")) is None:
            await ctx.send("Pebblehost credentials missing.")
            return            
        ftp.login(user=email, passwd=passwd)
        modlist = list(ftp.mlsd("/mods/"))
        clean_modlist: list[str] = []
        for i in modlist:
            filename = i[0]
            if filename.endswith(".jar"):
                modname = re.findall(r"[\w-]+(?=-)(?=\d)?|[\w-]+(?=\.)", filename)[
                    0
                ]
                clean_modlist.append(modname)
        await ctx.send("\n".join(clean_modlist))


def setup(client: commands.Bot):
    client.add_cog(PacifamOnly(client))

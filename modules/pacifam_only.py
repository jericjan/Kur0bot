from disnake.ext import commands
import disnake
from ftplib import FTP
import os
import json
import io
import re

from mcrcon import MCRcon


class PacifamOnly(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addoffline(self, ctx, username):
        avi_guild = self.client.get_guild(603147860225032192)
        while avi_guild == None:
            pass
        else:
            admin = disnake.utils.get(avi_guild.roles, name="Admin")
            moderator = disnake.utils.get(avi_guild.roles, name="Moderator")
            avilon = disnake.utils.get(avi_guild.roles, name="Aweelom")
        roles = [admin, moderator, avilon]
        if (
            any(role in roles for role in ctx.author.roles)
            or ctx.author.id == 216830153441935360
        ):
            await ctx.send(f"Adding {username} to list of offline users...")

            ftp = FTP(host="us28.pebblehost.com")
            ftp.login(user=os.getenv("PEBBLE_EMAIL"), passwd=os.getenv("PEBBLE_PASS"))
            r = io.BytesIO()
            ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
            config = json.loads(r.getvalue())
            if username.lower() in config["main"]["forcedOfflinePlayers"]:
                await ctx.send(f"{username} is alreading in the list!")
                return
            else:
                config["main"]["forcedOfflinePlayers"].append(username.lower())
            print(config["main"]["forcedOfflinePlayers"])
            dump = json.dumps(config, indent=2).encode("utf-8")
            ftp.storbinary("STOR /mods/EasyAuth/config.json", io.BytesIO(dump))

            with MCRcon("51.81.142.14", str(os.getenv("RCON_PASS")), 8082) as mcr:
                resp = mcr.command("/auth reload")
                print(resp)
            await ctx.send("Done!")

        else:
            await ctx.send("Only Avi/Admins/Mods can use this command")

    @commands.command()
    async def viewoffline(self, ctx):
        avi_guild = self.client.get_guild(603147860225032192)
        while avi_guild == None:
            pass
        else:
            admin = disnake.utils.get(avi_guild.roles, name="Admin")
            moderator = disnake.utils.get(avi_guild.roles, name="Moderator")
            avilon = disnake.utils.get(avi_guild.roles, name="Aweelom")
        roles = [admin, moderator, avilon]
        if (
            any(role in roles for role in ctx.author.roles)
            or ctx.author.id == 216830153441935360
        ):

            ftp = FTP(host="us28.pebblehost.com")
            ftp.login(user=os.getenv("PEBBLE_EMAIL"), passwd=os.getenv("PEBBLE_PASS"))
            r = io.BytesIO()
            ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
            config = json.loads(r.getvalue())
            print(config["main"]["forcedOfflinePlayers"])
            await ctx.send(
                f"Players added to the offline list are: {', '.join(config['main']['forcedOfflinePlayers'])}"
            )
        else:
            await ctx.send("Only Avi/Admins/Mods can use this command")

    @commands.command()
    async def removeoffline(self, ctx, username):
        avi_guild = self.client.get_guild(603147860225032192)
        while avi_guild == None:
            pass
        else:
            admin = disnake.utils.get(avi_guild.roles, name="Admin")
            moderator = disnake.utils.get(avi_guild.roles, name="Moderator")
            avilon = disnake.utils.get(avi_guild.roles, name="Aweelom")
        roles = [admin, moderator, avilon]
        if (
            any(role in roles for role in ctx.author.roles)
            or ctx.author.id == 216830153441935360
        ):
            await ctx.send(f"Removing {username} from list of offline users...")

            ftp = FTP(host="us28.pebblehost.com")
            ftp.login(user=os.getenv("PEBBLE_EMAIL"), passwd=os.getenv("PEBBLE_PASS"))
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
                resp = mcr.command("/auth reload")
                print(resp)
            await ctx.send("Done!")

        else:
            await ctx.send("Only Avi/Admins/Mods can use this command")

    @commands.command()
    async def viewmods(self, ctx):
        if ctx.guild.id == 603147860225032192:
            ftp = FTP(host="us28.pebblehost.com")
            ftp.login(user=os.getenv("PEBBLE_EMAIL"), passwd=os.getenv("PEBBLE_PASS"))
            modlist = list(ftp.mlsd("/mods/"))
            clean_modlist = []
            for i in modlist:
                filename = i[0]
                if filename.endswith(".jar"):
                    modname = re.findall(r"[\w-]+(?=-)(?=\d)?|[\w-]+(?=\.)", filename)[
                        0
                    ]
                    clean_modlist.append(modname)
            await ctx.send("\n".join(clean_modlist))
        else:
            await ctx.send("Only usable in the pacifam server")


def setup(client):
    client.add_cog(PacifamOnly(client))

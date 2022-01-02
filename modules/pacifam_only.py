from discord.ext import commands
import discord
import asyncio
from ftplib import FTP
import os
import json
import io

# from aiomcrcon import Client as mcrconClient
from mcrcon import MCRcon

# from rcon import rcon


class PacifamOnly(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addoffline(self, ctx, username):
        avi_guild = self.client.get_guild(603147860225032192)
        while avi_guild == None:
            pass
        else:
            admin = discord.utils.get(avi_guild.roles, name="Admin")
            moderator = discord.utils.get(avi_guild.roles, name="Moderator")
            avilon = discord.utils.get(avi_guild.roles, name="Aweelom")
        roles = [admin, moderator, avilon]
        if (
            any(role in roles for role in ctx.author.roles)
            or ctx.author.id == 216830153441935360
        ):
            await ctx.send("Adding " + str(username) + " to list of offline users...")

            ftp = FTP(host="us01.pebblehost.com")
            ftp.login(user=os.getenv("PEBBLE_EMAIL"), passwd=os.getenv("PEBBLE_PASS"))
            # ftp.cwd('mods')
            # ftp.cwd('EasyAuth')
            r = io.BytesIO()
            ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
            config = json.loads(r.getvalue())
            if username.lower() in config["main"]["forcedOfflinePlayers"]:
                await ctx.send(str(username) + " is alreading in the list!")
                return
            else:
                config["main"]["forcedOfflinePlayers"].append(username.lower())
            print(config["main"]["forcedOfflinePlayers"])
            dump = json.dumps(config, indent=2).encode("utf-8")
            # print(dump)
            ftp.storbinary("STOR /mods/EasyAuth/config.json", io.BytesIO(dump))
            # print(ftp.retrlines('LIST'))
            # coms = ["mcrcon", "-H", "51.81.142.14", "--password", str(os.getenv("RCON_PASS")), "-w", "1", "auth reload"]

            # out = await asyncio.create_subprocess_exec(*coms,
            #          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # stdout, stderr = await out.communicate()
            # print(stdout.decode())
            # print(stderr)
            # mc_client = mcrconClient("51.81.142.14", 25575, str(os.getenv("RCON_PASS")))
            # await mc_client.connect()

            # response = await mc_client.send_cmd("/say a")
            # print(response)
            # await mc_client.close()

            with MCRcon("51.81.142.14", str(os.getenv("RCON_PASS")), 8082) as mcr:
                resp = mcr.command("/auth reload")
                print(resp)
            await ctx.send("Done!")

            # response = await rcon('/say a',host='51.81.142.14', port=25575, passwd=str(os.getenv("RCON_PASS")))
            # print(response)
        else:
            await ctx.send("Only Avi/Admins/Mods can use this command")

    @commands.command()
    async def viewoffline(self, ctx):
        avi_guild = self.client.get_guild(603147860225032192)
        while avi_guild == None:
            pass
        else:
            admin = discord.utils.get(avi_guild.roles, name="Admin")
            moderator = discord.utils.get(avi_guild.roles, name="Moderator")
            avilon = discord.utils.get(avi_guild.roles, name="Aweelom")
        roles = [admin, moderator, avilon]
        if (
            any(role in roles for role in ctx.author.roles)
            or ctx.author.id == 216830153441935360
        ):

            ftp = FTP(host="us01.pebblehost.com")
            ftp.login(user=os.getenv("PEBBLE_EMAIL"), passwd=os.getenv("PEBBLE_PASS"))
            r = io.BytesIO()
            ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
            config = json.loads(r.getvalue())
            print(config["main"]["forcedOfflinePlayers"])
            await ctx.send(
                "Players added to the offline list are: "
                + ", ".join(config["main"]["forcedOfflinePlayers"])
            )
        else:
            await ctx.send("Only Avi/Admins/Mods can use this command")

    @commands.command()
    async def removeoffline(self, ctx, username):
        avi_guild = self.client.get_guild(603147860225032192)
        while avi_guild == None:
            pass
        else:
            admin = discord.utils.get(avi_guild.roles, name="Admin")
            moderator = discord.utils.get(avi_guild.roles, name="Moderator")
            avilon = discord.utils.get(avi_guild.roles, name="Aweelom")
        roles = [admin, moderator, avilon]
        if (
            any(role in roles for role in ctx.author.roles)
            or ctx.author.id == 216830153441935360
        ):
            await ctx.send(
                "Removing " + str(username) + " from list of offline users..."
            )

            ftp = FTP(host="us01.pebblehost.com")
            ftp.login(user=os.getenv("PEBBLE_EMAIL"), passwd=os.getenv("PEBBLE_PASS"))
            # ftp.cwd('mods')
            # ftp.cwd('EasyAuth')
            r = io.BytesIO()
            ftp.retrbinary("RETR /mods/EasyAuth/config.json", r.write)
            config = json.loads(r.getvalue())
            if username.lower() in config["main"]["forcedOfflinePlayers"]:
                config["main"]["forcedOfflinePlayers"].remove(username.lower())
            else:
                await ctx.send(str(username) + " isn't in the list!")
                return
            print(config["main"]["forcedOfflinePlayers"])
            dump = json.dumps(config, indent=2).encode("utf-8")
            # print(dump)
            ftp.storbinary("STOR /mods/EasyAuth/config.json", io.BytesIO(dump))
            # print(ftp.retrlines('LIST'))
            # coms = ["mcrcon", "-H", "51.81.142.14", "--password", str(os.getenv("RCON_PASS")), "-w", "1", "auth reload"]

            # out = await asyncio.create_subprocess_exec(*coms,
            #          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # stdout, stderr = await out.communicate()
            # print(stdout.decode())
            # print(stderr)
            # mc_client = mcrconClient("51.81.142.14", 25575, str(os.getenv("RCON_PASS")))
            # await mc_client.connect()

            # response = await mc_client.send_cmd("/say a")
            # print(response)
            # await mc_client.close()

            with MCRcon("51.81.142.14", str(os.getenv("RCON_PASS")), 8082) as mcr:
                resp = mcr.command("/auth reload")
                print(resp)
            await ctx.send("Done!")

            # response = await rcon('/say a',host='51.81.142.14', port=25575, passwd=str(os.getenv("RCON_PASS")))
            # print(response)
        else:
            await ctx.send("Only Avi/Admins/Mods can use this command")


def setup(client):
    client.add_cog(PacifamOnly(client))

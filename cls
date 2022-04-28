[33mcommit a06aeb69b1a3c0f8155e95088673e1aee9df5ae7[m[33m ([m[1;31morigin/master[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Author: Jeric Jan Jan <38642145+jericjan@users.noreply.github.com>
Date:   Sat Apr 16 08:46:31 2022 +0000

    rs

[1mdiff --git a/modules/commands.json b/modules/commands.json[m
[1mindex acb8d49..50fcdcc 100644[m
[1m--- a/modules/commands.json[m
[1m+++ b/modules/commands.json[m
[36m@@ -109,6 +109,7 @@[m
     "reload",[m
     "unload",[m
     "checkhelp",[m
[31m-    "ytbypass"[m
[32m+[m[32m    "ytbypass",[m
[32m+[m[32m    "rs"[m
   ][m
 }[m
\ No newline at end of file[m
[1mdiff --git a/modules/others/resize.py b/modules/others/resize.py[m
[1mindex aa68896..ae24077 100644[m
[1m--- a/modules/others/resize.py[m
[1m+++ b/modules/others/resize.py[m
[36m@@ -87,6 +87,40 @@[m [mclass Resize(commands.Cog):[m
         bruh.close()[m
         await message.delete()[m
 [m
[32m+[m[32m    @commands.command()[m
[32m+[m[32m    async def rs(self, ctx, link=None):[m
[32m+[m[32m        if link == None:[m
[32m+[m[32m            print(ctx.message.attachments)  # a list[m
[32m+[m[32m            print(ctx.message.reference)[m
[32m+[m[32m            if ctx.message.attachments:  # message has images[m
[32m+[m[32m                print("is attachment")[m
[32m+[m[32m                link = ctx.message.attachments[0].url[m
[32m+[m[32m            elif ctx.message.reference is not None:  # message is replying[m
[32m+[m[32m                print("is reply")[m
[32m+[m[32m                id = ctx.message.reference.message_id[m
[32m+[m[32m                msg = await ctx.channel.fetch_message(id)[m
[32m+[m[32m                if msg.attachments:  # if replied has image[m
[32m+[m[32m                    link = msg.attachments[0].url[m
[32m+[m[32m                elif msg.embeds:  # if replied has link[m
[32m+[m[32m                    link = msg.embeds[0].url[m
[32m+[m
[32m+[m[32m                # print("embmeds: {0}".format(msg.embeds))[m
[32m+[m[32m                # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):[m
[32m+[m[32m                #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0][m
[32m+[m[32m                # link= msg.attachments[0].url[m
[32m+[m[32m                else:[m
[32m+[m[32m                    await ctx.send("the message you replied to has no image, baka!")[m
[32m+[m[32m            else:[m
[32m+[m[32m                await ctx.send("you did something wrong. brug. try again.")[m
[32m+[m[32m                return[m
[32m+[m[32m            print(link)[m
[32m+[m[32m        message = await ctx.send("Resizing...")[m
[32m+[m[32m        bruh = await self.foo(link, 1600, 720)[m
[32m+[m[32m        bruh.seek(0)[m
[32m+[m[32m        filename = link.split("/")[-1][m
[32m+[m[32m        await ctx.send(file=disnake.File(bruh, filename=filename))[m
[32m+[m[32m        bruh.close()[m
[32m+[m[32m        await message.delete()[m
 [m
 def setup(client):[m
     client.add_cog(Resize(client))[m

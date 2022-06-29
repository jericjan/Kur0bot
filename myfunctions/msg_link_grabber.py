        
        
async def grab_link(ctx, link):        
        if link == None:
            print(ctx.message.attachments)  # a list
            print(ctx.message.reference)
            if ctx.message.attachments:  # message has images
                print("is attachment")
                link = ctx.message.attachments[0].url
            elif ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                if msg.attachments:  # if replied has image
                    link = msg.attachments[0].url
                elif msg.embeds:  # if replied has link
                    link = msg.embeds[0].url

                # print("embmeds: {0}".format(msg.embeds))
                # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
                #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
                # link= msg.attachments[0].url
                else:
                    # await ctx.send("the message you replied to has no image, baka!")
                    raise Exception("the message you replied to has no image, baka!")
            else:
                # await ctx.send("you did something wrong. brug. try again.")
                raise Exception("you did something wrong. brug. try again.")
        return link
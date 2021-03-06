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

            else:
                raise Exception("the message you replied to has no image, baka!")
        else:
            raise Exception("you did something wrong. brug. try again.")
    return link

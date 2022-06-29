from disnake.ext import commands
import disnake
import cv2
import numpy as np
import uuid
import requests
import os
import asyncio
import subprocess
from shlex import join as shlexjoin
import shutil
import time
import myfunctions.msg_link_grabber as msg_link_grabber

class Vergil(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def quickvergil(self, ctx, link=None):    
        start_time = time.time()
        link = await msg_link_grabber.grab_link(ctx,link)
        print(link)
            
        # open up video
        vergil_status = await ctx.send("Getting motivated...")
        cap = cv2.VideoCapture("videos/vergil_greenscreen/vergil_%06d.png",cv2.CAP_IMAGES)
        # cap = ffmpegcv.VideoCapture("videos/vergil_greenscreen/vergil_%06d.png",cv2.CAP_IMAGES)
        url_response = requests.get(link)
        user_image = cv2.imdecode(np.array(bytearray(url_response.content), dtype=np.uint8), -1)

        # grab one frame
        _, frame = cap.read()
        h,w = frame.shape[:2]

        # videowriter 
        res = (w, h);
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        random_uuid = uuid.uuid4()
        os.makedirs(f'videos/vergil_greenscreen/{random_uuid}/', exist_ok=True)
        out = cv2.VideoWriter(f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4',fourcc, 30.0, res)
        # out = ffmpegcv.VideoWriter(f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4','h264', 30.0, res)

        # loop
        done = False
        while not done:
            # get frame
            ret, img =  cap.read()
            if not ret:
                done = True
                continue

            # resize
            vergil = cv2.resize(img, res)
            image = cv2.resize(user_image, res)            
            # extract alpha channel from foreground image as mask and make 3 channels
            image = image[:, :, :3]
            alpha_channel = vergil[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
            overlay_colors = vergil[:, :, :3]
            
            alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
            
            h, w = vergil.shape[:2]
            background_subsection = image[0:h, 0:w]
            composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask
            image[0:h, 0:w] = composite
            # save
            out.write(image);
        # close caps
        cap.release();
        out.release();  
        await vergil_status.edit(content="Obtaining more power!")
        vid1 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4'
        vid1_h264 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1_h264.mp4'
        vid1_ts = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.ts'
        vid2 = f'videos/vergil_greenscreen/vergil_smol.mp4'
        vid2_ts = f'videos/vergil_greenscreen/vergil_smol.ts'
        vid3 = f'videos/vergil_greenscreen/{random_uuid}/vergil_3.mp4'
        vid4 = f'videos/vergil_greenscreen/{random_uuid}/vergil_4.mp4'
        vid5 = f'videos/vergil_greenscreen/{random_uuid}/vergil_5.mp4'
        vergil_audio =  f'videos/vergil_greenscreen/vergil_full.m4a'
        coms = ["ffmpeg" ,"-i", vid1, "-vcodec", "h264", vid1_h264] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate()            
        coms = ["ffmpeg" ,"-i", vid1_h264, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", vid1_ts] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate()      
        print(stdout.decode('utf-8'))
        if not os.path.exists(vid2_ts):
            coms = ["ffmpeg" ,"-i", vid2, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", vid2_ts] 
            print(shlexjoin(coms))
            out = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )        
            stdout, stderr = await out.communicate()      
            print(stdout.decode('utf-8'))           
        await vergil_status.edit(content="Becoming the reclaimer of my name...")    
        coms = ['ffmpeg', '-i', f'concat:{vid1_ts}|{vid2_ts}',"-c", "copy", "-bsf:a", "aac_adtstoasc", vid3]  
        # coms = ["ffmpeg" ,"-i", vid1_fixed, "-i", vid2, "-i", vergil_audio, \
                # "-filter_complex", "[0:v] [1:v] concat=n=2:v=1 [vv]", \
                # "-map", "[vv]", "-map", "2:a:0", vid3] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate() 
        print(stdout.decode('utf-8'))
        coms = ['ffmpeg', '-i', vid3,'-i',vergil_audio,"-c", "copy", "-map", "0:v:0", "-map", "1:a:0", vid4]  
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate() 
        print(stdout.decode('utf-8'))
        coms = ['ffmpeg', '-i', vid4,"-c", "copy", vid5]  
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate() 
        print(stdout.decode('utf-8'))        
        await vergil_status.edit(content="Approaching...")    
        await vergil_status.edit(content="",file=disnake.File(vid5, filename="vergil status.mp4"))
        end = time.time() - start_time
        await ctx.send(f"Vergil arrived in {end:.2f} seconds")
        shutil.rmtree(f'videos/vergil_greenscreen/{random_uuid}/')
        
        
        #not needed anymore
    # @commands.command()
    # async def smallvergil(self, ctx, link=None):    
        # if link == None:
            # print(ctx.message.attachments)  # a list
            # print(ctx.message.reference)
            # if ctx.message.attachments:  # message has images
                # print("is attachment")
                # link = ctx.message.attachments[0].url
            # elif ctx.message.reference is not None:  # message is replying
                # print("is reply")
                # id = ctx.message.reference.message_id
                # msg = await ctx.channel.fetch_message(id)
                # if msg.attachments:  # if replied has image
                    # link = msg.attachments[0].url
                # elif msg.embeds:  # if replied has link
                    # link = msg.embeds[0].url

                # # print("embmeds: {0}".format(msg.embeds))
                # # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
                # #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
                # # link= msg.attachments[0].url
                # else:
                    # await ctx.send("the message you replied to has no image, baka!")
            # else:
                # await ctx.send("you did something wrong. brug. try again.")
                # return
            # print(link)   
            
        # # open up video
        # cap = cv2.VideoCapture("videos/vergil_greenscreen/vergil_%06d.png",cv2.CAP_IMAGES)
        # url_response = requests.get(link)
        # user_image = cv2.imdecode(np.array(bytearray(url_response.content), dtype=np.uint8), -1)

        # # grab one frame
        # _, frame = cap.read()
        # h,w = frame.shape[:2]

        # # videowriter 
        # res = (w, h);
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # random_uuid = uuid.uuid4()
        # os.makedirs(f'videos/vergil_greenscreen/{random_uuid}/', exist_ok=True)
        # out = cv2.VideoWriter(f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4',fourcc, 30.0, res)

        # # loop
        # done = False
        # while not done:
            # # get frame
            # ret, img =  cap.read()
            # if not ret:
                # done = True
                # continue

            # # resize
            # vergil = cv2.resize(img, res)
            # image = cv2.resize(user_image, res)            
            # # extract alpha channel from foreground image as mask and make 3 channels
            # image = image[:, :, :3]
            # alpha_channel = vergil[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
            # overlay_colors = vergil[:, :, :3]
            
            # alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
            
            # h, w = vergil.shape[:2]
            # background_subsection = image[0:h, 0:w]
            # composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask
            # image[0:h, 0:w] = composite
            # # save
            # out.write(image);
        # # close caps
        # cap.release();
        # out.release();  
        # vid1 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4'
        # vid1_h264 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1_h264.mp4'
        # vid1_ts = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.ts'
        # vid2 = f'videos/vergil_greenscreen/vergil_after_full.mp4'
        # vid2_ts = f'videos/vergil_greenscreen/vergil_after_full.ts'
        # vid3 = f'videos/vergil_greenscreen/{random_uuid}/vergil_3.mp4'
        # vid4 = f'videos/vergil_greenscreen/{random_uuid}/vergil_4.mp4'
        # vergil_audio =  f'videos/vergil_greenscreen/vergil_full.m4a'
        # coms = ["ffmpeg" ,"-i", vid1, "-vcodec", "h264", vid1_h264] 
        # print(shlexjoin(coms))
        # out = await asyncio.create_subprocess_exec(
            # *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        # )        
        # stdout, stderr = await out.communicate()             
        # coms = ["ffmpeg" ,"-i", vid1_h264, "-i", vid2, "-i", vergil_audio, \
                # "-filter_complex", "[0:v] [1:v] concat=n=2:v=1 [vv]", \
                # "-map", "[vv]", "-map", "2:a:0", vid3] 
        # print(shlexjoin(coms))
        # out = await asyncio.create_subprocess_exec(
            # *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        # )        
        # stdout, stderr = await out.communicate() 
        # print(stdout.decode('utf-8'))
        
        # await ctx.send(file=disnake.File(vid3, filename="vergil status.mp4"))
        # shutil.rmtree(f'videos/vergil_greenscreen/{random_uuid}/')
        
    @commands.command()
    async def vergil(self, ctx, link=None):    
        debug_mode = False
        start_time = time.time()
        link = await msg_link_grabber.grab_link(ctx,link)
        print(link)
            
        #unique uuid    
        random_uuid = uuid.uuid4()    
            
        # open up video
        vergil_status = await ctx.send("Getting motivated...")
        # vergil_status = await self.send(ctx,random_uuid,"Getting motivated...")
        cap = cv2.VideoCapture("videos/vergil_greenscreen/vergil_%06d.png",cv2.CAP_IMAGES)
        # cap = ffmpegcv.VideoCapture("videos/vergil_greenscreen/vergil_%06d.png",cv2.CAP_IMAGES)
        url_response = requests.get(link)
        user_image = cv2.imdecode(np.array(bytearray(url_response.content), dtype=np.uint8), -1)

        # grab one frame
        _, frame = cap.read()
        h,w = frame.shape[:2]

        # videowriter 
        res = (w, h);
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        os.makedirs(f'videos/vergil_greenscreen/{random_uuid}/', exist_ok=True)
        out = cv2.VideoWriter(f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4',fourcc, 30.0, res)
        # out = ffmpegcv.VideoWriter(f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4','h264', 30.0, res)
        

        image = cv2.resize(user_image, res)
        pre_filtered_image = image.copy()
        #cut remnant/cracked effect
        remnant = cv2.imread('videos/vergil_greenscreen/vergil_remnant.png',cv2.IMREAD_UNCHANGED)
        image = image[:, :, :3]                
        alpha_channel = remnant[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
        overlay_colors = remnant[:, :, :3]                               
        alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
        h, w = remnant.shape[:2]
        background_subsection = image[0:h, 0:w]
        composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask                
        image[0:h, 0:w] = composite     
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)                   
        post_filtered_image = image.copy()
        
        frame = 0
        done = False
        shift = 10
        saved_position = 0
        blue = 5   
        log = ""
        # log+= f"Pre stuff: {time.time()-start_time:.2f} seconds passed\n"
        if debug_mode:
            log += f'Pre stuff:\t{time.time()-start_time:.2f}\n'
        mid_time = time.time()
        greenscreen_time = mid_time
        # loop
        while not done:
            # print(f"Frame: {frame}")
            # get frame
            ret, img =  cap.read()
            if not ret:
                done = True
                continue

            # resize
            vergil = cv2.resize(img, res)
            

  
            #cut the image
            if frame < 16:
                image = pre_filtered_image.copy()
            else:
                image = post_filtered_image.copy()
                #creating blue
                blue_img  = np.full((480,854,4), (blue,0,0,255), np.uint8)    
                #eases in blue                
                if blue < 50:
                    blue +=5
                #converts to RGBA            
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
                #adding blue
                image  = cv2.add(image,blue_img)
                # The number of pixels    
                num_rows, num_cols = image.shape[:2]               
          
                #right side
                right_mask = cv2.imread('videos/vergil_greenscreen/imagecut_right.png',0)
                right_cut = cv2.bitwise_and(image,image,mask = right_mask)
                
                saved_position = saved_position+shift
                # Creating a translation matrix
                translation_matrix = np.float32([ [1,0,saved_position], [0,1,saved_position] ])
                # Image translation
                img_left = cv2.warpAffine(right_cut, translation_matrix, (num_cols,num_rows))      

                #left side
                left_mask = cv2.imread('videos/vergil_greenscreen/imagecut_left.png',0)
                left_cut = cv2.bitwise_and(image,image,mask = left_mask)
                # Creating a translation matrix 
                translation_matrix = np.float32([ [1,0,-saved_position], [0,1,-saved_position] ])
                # Image translation
                img_right = cv2.warpAffine(left_cut, translation_matrix, (num_cols,num_rows))       
                
                shift-= 0.25
                 
                start_point = (0, 0)
                end_point = (854, 480)
                   
                # Black color in BGR
                color = (63, 57, 54)
                thickness = -1
                solid_background = cv2.rectangle(image, start_point, end_point, color, thickness)                
                
                #combines the two sliced images
                cuts = cv2.addWeighted(img_left, 1, img_right, 1, 0.0)
                
                #adding the background
                # try:    
                    # image = previous_frame[:, :, :3]
                # except:
                    # image = solid_background[:, :, :3]
                image = solid_background[:, :, :3]    
                alpha_channel = cuts[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
                overlay_colors = cuts[:, :, :3]                               
                alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

                h, w = cuts.shape[:2]
                background_subsection = image[0:h, 0:w]
                composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask                
                image[0:h, 0:w] = composite                
            #adds vergil
            # extract alpha channel from foreground image as mask and make 3 channels
            image = image[:, :, :3]
            alpha_channel = vergil[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
            overlay_colors = vergil[:, :, :3]
            
            alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
            
            h, w = vergil.shape[:2]
            background_subsection = image[0:h, 0:w]
            composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask
            image[0:h, 0:w] = composite
            # save

            out.write(image); 
            # if (time.time() - greenscreen_time) > 1.1:                
                # percent = f"{((frame/94)*100):.2f}%"
                # print(f"motivated at {percent}")
                # await vergil_status.edit(content=f"Getting motivated... ({percent})")
                # greenscreen_time = time.time()
            frame += 1
        print(f"Reached {frame} frames")    
        
        # log+= f"Green screening done: {time.time()-mid_time:.2f} seconds passed\n"
        if debug_mode:
            log += f'Green screening done:\t{time.time()-mid_time:.2f}\n'
        mid_time = time.time()
        # close caps
        cap.release();
        out.release();  
        await vergil_status.edit(content="<:motivated1:991217157100818534><:motivated2:991217292761382912><:motivated3:991217345345368074>\nApproaching...")
        vid1 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4'
        vid1_h264 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1_h264.mp4'
        vid1_ts = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.ts'
        vid2 = f'videos/vergil_greenscreen/vergil_smol.mp4'
        vid2_ts = f'videos/vergil_greenscreen/vergil_smol.ts'
        vid3 = f'videos/vergil_greenscreen/{random_uuid}/vergil_3.mp4'
        vid4 = f'videos/vergil_greenscreen/{random_uuid}/vergil_4.mp4'
        vergil_audio =  f'videos/vergil_greenscreen/vergil_full.m4a'
        # vcodec = "libx264"
        vcodec = "h264"
        coms = ["ffmpeg" ,"-i", vid1, "-vcodec", vcodec, "-preset", "veryfast", "-crf", "28",vid1_h264] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate()        
        # log+= f"Converted to H264: {time.time()-mid_time:.2f} seconds passed\n"
        if debug_mode:
            log += f'Converted to H264:\t{time.time()-mid_time:.2f}\n'
        mid_time = time.time()
        print(f"\033[;32m{stdout.decode('utf-8')}\033[0m")
        try:
            print(f"\033[;31m{stderr.decode('utf-8')}\033[0m")
        except:
            pass              
        coms = ["ffmpeg" ,"-i", vid1_h264, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", vid1_ts] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate()      
        print(f"\033[;32m{stdout.decode('utf-8')}\033[0m")
        try:
            print(f"\033[;31m{stderr.decode('utf-8')}\033[0m")
        except:
            pass    
        # log+= f"(1) Converted to MPEG-TS: {time.time()-mid_time:.2f} seconds passed\n"
        if debug_mode:
            log += f'Converted to MPEG-TS:\t{time.time()-mid_time:.2f}\n'
        mid_time = time.time()
        print(f"\033[;32m{stdout.decode('utf-8')}\033[0m")
        try:
            print(f"\033[;31m{stderr.decode('utf-8')}\033[0m")
        except:
            pass        
        if not os.path.exists(vid2_ts):
            coms = ["ffmpeg" ,"-i", vid2, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", vid2_ts] 
            print(shlexjoin(coms))
            out = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )        
            stdout, stderr = await out.communicate()     
            log+= f"(2) Converted to MPEG-TS: {time.time()-mid_time:.2f} seconds passed\n"
            mid_time = time.time()
            print(stdout.decode('utf-8'))                   
        coms = ['ffmpeg', '-i', f'concat:{vid1_ts}|{vid2_ts}',"-c", "copy", "-bsf:a", "aac_adtstoasc", vid3]  
        # coms = ["ffmpeg" ,"-i", vid1_fixed, "-i", vid2, "-i", vergil_audio, \
                # "-filter_complex", "[0:v] [1:v] concat=n=2:v=1 [vv]", \
                # "-map", "[vv]", "-map", "2:a:0", vid3] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate() 
        # log+= f"Concatenatted vods: {time.time()-mid_time:.2f} seconds passed\n"
        if debug_mode:
            log += f'Concatenatted vods:\t{time.time()-mid_time:.2f}\n'
        mid_time = time.time()
        print(f"\033[;32m{stdout.decode('utf-8')}\033[0m")
        try:
            print(f"\033[;31m{stderr.decode('utf-8')}\033[0m")
        except:
            pass            
        coms = ['ffmpeg', '-i', vid3,'-i',vergil_audio,"-c", "copy", "-map", "0:v:0", "-map", "1:a:0", vid4]  
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate()
        # log+= f"Added audio: {time.time()-mid_time:.2f} seconds passed\n"     
        if debug_mode:        
            log += f'Added audio:\t{time.time()-mid_time:.2f}\n'
        mid_time = time.time()
        print(f"\033[;32m{stdout.decode('utf-8')}\033[0m")
        try:
            print(f"\033[;31m{stderr.decode('utf-8')}\033[0m")
        except:
            pass                     
        await vergil_status.edit(content="",file=disnake.File(vid4, filename="vergil status.mp4"))
        if debug_mode:
            log += f'Sent file:\t{time.time()-mid_time:.2f}\n'
        # log += f"Total:\t{time.time()-start_time:.2f}\n"
        log += f"Vergil arrived in {time.time()-start_time:.2f} seconds\n"
        # await ctx.send(f"Took {time.time() - start_time:.2f} seconds")
        await ctx.send(log)
        shutil.rmtree(f'videos/vergil_greenscreen/{random_uuid}/')        
        
    #SCRAPPED. SLOWER
    # @commands.command()
    # async def vergiltest(self, ctx, link=None):    
        # start_time = time.time()
        # if link == None:
            # print(ctx.message.attachments)  # a list
            # print(ctx.message.reference)
            # if ctx.message.attachments:  # message has images
                # print("is attachment")
                # link = ctx.message.attachments[0].url
            # elif ctx.message.reference is not None:  # message is replying
                # print("is reply")
                # id = ctx.message.reference.message_id
                # msg = await ctx.channel.fetch_message(id)
                # if msg.attachments:  # if replied has image
                    # link = msg.attachments[0].url
                # elif msg.embeds:  # if replied has link
                    # link = msg.embeds[0].url

                # # print("embmeds: {0}".format(msg.embeds))
                # # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
                # #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
                # # link= msg.attachments[0].url
                # else:
                    # await ctx.send("the message you replied to has no image, baka!")
                    # return
            # else:
                # await ctx.send("you did something wrong. brug. try again.")
                # return
            # print(link)   
            
        # # open up video
        # vergil_status = await ctx.send("Getting motivated...")
        # cap = cv2.VideoCapture("videos/vergil_greenscreen/vergil_%06d.png",cv2.CAP_IMAGES)
        # # cap = ffmpegcv.VideoCapture("videos/vergil_greenscreen/vergil_%06d.png",cv2.CAP_IMAGES)
        # url_response = requests.get(link)
        # user_image = cv2.imdecode(np.array(bytearray(url_response.content), dtype=np.uint8), -1)

        # # grab one frame
        # _, frame = cap.read()
        # h,w = frame.shape[:2]

        # # videowriter 
        # res = (w, h);
        # fourcc = cv2.VideoWriter_fourcc(*'avc1')
        # random_uuid = uuid.uuid4()
        # os.makedirs(f'videos/vergil_greenscreen/{random_uuid}/', exist_ok=True)
        # # out = cv2.VideoWriter(f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4',fourcc, 30.0, res)
        # out = ffmpegcv.VideoWriter(f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4','h264', 30.0, res)
        

        # image = cv2.resize(user_image, res)
        # pre_filtered_image = image.copy()
        # #cut remnant/cracked effect
        # remnant = cv2.imread('videos/vergil_greenscreen/vergil_remnant.png',cv2.IMREAD_UNCHANGED)
        # image = image[:, :, :3]                
        # alpha_channel = remnant[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
        # overlay_colors = remnant[:, :, :3]                               
        # alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
        # h, w = remnant.shape[:2]
        # background_subsection = image[0:h, 0:w]
        # composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask                
        # image[0:h, 0:w] = composite     
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)                   
        # post_filtered_image = image.copy()
        
        # frame = 0
        # done = False
        # shift = 10
        # saved_position = 0
        # blue = 5   
        # log = ""
        # # log+= f"Pre stuff: {time.time()-start_time:.2f} seconds passed\n"
        # log += f'{time.time()-start_time:.2f}\n'
        # mid_time = time.time()
        # # loop
        # while not done:
            # print(f"Frame: {frame}")
            # # get frame
            # ret, img =  cap.read()
            # if not ret:
                # done = True
                # continue

            # # resize
            # vergil = cv2.resize(img, res)
            

  
            # #cut the image
            # if frame < 16:
                # image = pre_filtered_image.copy()
            # else:
                # image = post_filtered_image.copy()
                # #creating blue
                # blue_img  = np.full((480,854,4), (blue,0,0,255), np.uint8)    
                # #eases in blue                
                # if blue < 50:
                    # blue +=5
                # # The number of pixels                
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
                # #adding blue
                # image  = cv2.add(image,blue_img)
                # num_rows, num_cols = image.shape[:2]               
          
                # #right side
                # right_mask = cv2.imread('videos/vergil_greenscreen/imagecut_right.png',0)
                # right_cut = cv2.bitwise_and(image,image,mask = right_mask)

                # # Creating a translation matrix
                # saved_position = saved_position+shift
                # translation_matrix = np.float32([ [1,0,saved_position], [0,1,saved_position] ])
                # # Image translation
                # img_left = cv2.warpAffine(right_cut, translation_matrix, (num_cols,num_rows))      

                # #left side
                # left_mask = cv2.imread('videos/vergil_greenscreen/imagecut_left.png',0)
                # left_cut = cv2.bitwise_and(image,image,mask = left_mask)
                # # Creating a translation matrix 
                # translation_matrix = np.float32([ [1,0,-saved_position], [0,1,-saved_position] ])
                # # Image translation
                # img_right = cv2.warpAffine(left_cut, translation_matrix, (num_cols,num_rows))       
                
                # shift-= 0.25
                 
                # start_point = (0, 0)
                # end_point = (854, 480)
                   
                # # Black color in BGR
                # color = (63, 57, 54)
                # thickness = -1
                # solid_background = cv2.rectangle(image, start_point, end_point, color, thickness)                
                
                # #combines the two sliced images
                # cuts = cv2.addWeighted(img_left, 1, img_right, 1, 0.0)
                
                # #adding the background
                # # try:    
                    # # image = previous_frame[:, :, :3]
                # # except:
                    # # image = solid_background[:, :, :3]
                # image = solid_background[:, :, :3]    
                # alpha_channel = cuts[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
                # overlay_colors = cuts[:, :, :3]                               
                # alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

                # h, w = cuts.shape[:2]
                # background_subsection = image[0:h, 0:w]
                # composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask                
                # image[0:h, 0:w] = composite                
            # #adds vergil
            # # extract alpha channel from foreground image as mask and make 3 channels
            # image = image[:, :, :3]
            # alpha_channel = vergil[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
            # overlay_colors = vergil[:, :, :3]
            
            # alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
            
            # h, w = vergil.shape[:2]
            # background_subsection = image[0:h, 0:w]
            # composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask
            # image[0:h, 0:w] = composite
            # # save

            # out.write(image); 
            # frame += 1
        # print(f"Reached {frame} frames")    
        
        # # log+= f"Green screening done: {time.time()-mid_time:.2f} seconds passed\n"
        # log += f'{time.time()-mid_time:.2f}\n'
        # mid_time = time.time()
        # # close caps
        # cap.release();
        # out.release();  
        # await vergil_status.edit(content="Obtaining more power!")
        # vid1 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4'
        # vid1_h264 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1_h264.mp4'
        # vid1_ts = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.ts'
        # vid2 = f'videos/vergil_greenscreen/vergil_after_full.mp4'
        # vid2_ts = f'videos/vergil_greenscreen/vergil_after_full.ts'
        # vid3 = f'videos/vergil_greenscreen/{random_uuid}/vergil_3.mp4'
        # vid4 = f'videos/vergil_greenscreen/{random_uuid}/vergil_4.mp4'
        # vergil_audio =  f'videos/vergil_greenscreen/vergil_full.m4a'
        # # coms = ["ffmpeg" ,"-i", vid1, "-vcodec", "h264", vid1_h264] 
        # # print(shlexjoin(coms))
        # # out = await asyncio.create_subprocess_exec(
            # # *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        # # )        
        # # stdout, stderr = await out.communicate()        
        # # log+= f"Converted to H264: {time.time()-mid_time:.2f} seconds passed\n"
        # # mid_time = time.time()
        # # print(stdout.decode('utf-8'))
        # # try:
            # # print(stderr.decode('utf-8'))
        # # except:
            # # pass              
        # # coms = ["ffmpeg" ,"-i", vid1_h264, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", vid1_ts] 
        # mpegts_success = False
        # while mpegts_success != True:
            # coms = ["ffmpeg-git/ffmpeg" ,"-i", vid1, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", "-movflags", "faststart", vid1_ts] 
            # print(shlexjoin(coms))
            # out = await asyncio.create_subprocess_exec(
                # *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            # )        
            # stdout, stderr = await out.communicate()      
            # if "Invalid data found when processing input" not in stdout.decode('utf-8'):
                # mpegts_success = True
        # # log+= f"(1) Converted to MPEG-TS: {time.time()-mid_time:.2f} seconds passed\n"
        # log += f'{time.time()-mid_time:.2f}\n'
        # mid_time = time.time()
        # print(f"\033[;32m{stdout.decode('utf-8')}\033[0m")
        # try:
            # print(f"\033[;31m{stderr.decode('utf-8')}\033[0m")
        # except:
            # pass        
        # if not os.path.exists(vid2_ts):
            # coms = ["ffmpeg" ,"-i", vid2, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", vid2_ts] 
            # print(shlexjoin(coms))
            # out = await asyncio.create_subprocess_exec(
                # *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            # )        
            # stdout, stderr = await out.communicate()     
            # log+= f"(2) Converted to MPEG-TS: {time.time()-mid_time:.2f} seconds passed\n"
            # mid_time = time.time()
            # print(stdout.decode('utf-8'))           
        # await vergil_status.edit(content="Becoming the reclaimer of my name...")    
        # coms = ['ffmpeg', '-i', f'concat:{vid1_ts}|{vid2_ts}',"-c", "copy", "-bsf:a", "aac_adtstoasc", vid3]  
        # # coms = ["ffmpeg" ,"-i", vid1_fixed, "-i", vid2, "-i", vergil_audio, \
                # # "-filter_complex", "[0:v] [1:v] concat=n=2:v=1 [vv]", \
                # # "-map", "[vv]", "-map", "2:a:0", vid3] 
        # print(shlexjoin(coms))
        # out = await asyncio.create_subprocess_exec(
            # *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        # )        
        # stdout, stderr = await out.communicate() 
        # # log+= f"Concatenatted vods: {time.time()-mid_time:.2f} seconds passed\n"
        # log += f'{time.time()-mid_time:.2f}\n'
        # mid_time = time.time()
        # print(f"\033[;32m{stdout.decode('utf-8')}\033[0m")
        # try:
            # print(f"\033[;31m{stderr.decode('utf-8')}\033[0m")
        # except:
            # pass            
        # coms = ['ffmpeg', '-i', vid3,'-i',vergil_audio,"-c", "copy", "-map", "0:v:0", "-map", "1:a:0", vid4]  
        # print(shlexjoin(coms))
        # out = await asyncio.create_subprocess_exec(
            # *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        # )        
        # stdout, stderr = await out.communicate()
        # # log+= f"Added audio: {time.time()-mid_time:.2f} seconds passed\n"        
        # log += f'{time.time()-mid_time:.2f}\n'
        # print(f"\033[;32m{stdout.decode('utf-8')}\033[0m")
        # try:
            # print(f"\033[;31m{stderr.decode('utf-8')}\033[0m")
        # except:
            # pass             
        # await vergil_status.edit(content="Approaching...")    
        # await vergil_status.edit(content="",file=disnake.File(vid4, filename="vergil status.mp4"))
        # end = time.time() - start_time
        # await ctx.send(f"Took {end:.2f} seconds")
        # await ctx.send(log)
        # shutil.rmtree(f'videos/vergil_greenscreen/{random_uuid}/')        
        
def setup(client):
    client.add_cog(Vergil(client))

Kur0 sus bot
==============
<img alt="" src="https://img.shields.io/github/repo-size/jericjan/Kur0bot" />

[![Made with Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://python.org)
[![Hosted with GH Pages](https://img.shields.io/badge/Hosted_with-DigitalOcean-blue?logo=digitalocean&logoColor=white)](https://replit.com/@JericJanJan/Kur0bot)

-----
My sussy discord bot.

Invite the bot:\
[![Invite - Bot](https://img.shields.io/badge/Invite-Bot-2ea44f?style=for-the-badge)](https://discord.com/api/oauth2/authorize?client_id=850336994299215892&permissions=3758615616&scope=bot)

It *might* require more permissions than the one above, and it won't tell you that it's missing permissions cuz bad coding, use this if that ever happens:\
[![Invite - Bot as admin](https://img.shields.io/badge/Invite-Bot_as_admin-2ea44f?style=for-the-badge)](https://discord.com/api/oauth2/authorize?client_id=850336994299215892&permissions=8&scope=bot)\
(or just give the bot admin permission through Discord)

To do list:
- new help menu with discord select menus
- k.id command compresss feature
- k.supacha colers
- k.addaudio
- k.demotivate
- k.mgr replace audio with videos
- make the webhook imitate user thing a custom function
- replace synchronous requests with asyncio w/ aiohttp.ClientSession()
- use asynchronous database for storing user data

# Environment variables:
- `TOKEN`: Discord bot token
- `YT_API_KEY`: YouTube API key
- `PEBBLE_EMAIL`: Pebblehost email
- `PEBBLE_PASS`: Pebblehost pass
- `RCON_PASS`: Minecraft RCON thing
- `ENCRYPTPASSPHRASE`: Passphrase for encrypting cookies
- `SAUCENAO_KEY`: SauceNAO API key
- `PORT`: Port used for the mini Flask server that temporarily hosts files that are too large to send via Discord
- `OSU_ID`: osu! client ID
- `OSU_SECRET`: osu! client secret
- `MONGO_DB_PASS`: MongoDB connection pass (You should prolly also change the rest of the connection url in `myfunctions/motor.py`)
- `CUSTOM_SEARCH_KEY`: Google customsearch API key
- `PYTHONASYNCIODEBUG`: Asyncio debug mode (1 or 0)
- `SERPAPI_KEY`: Serpapi API key

# Docker instructions
1. Build the image `docker build -t image-name-here .`
2. Change the `image` in `docker-compose.yml` to match your chosen image name
3. Create an `.env` file in the project folder and fill it in with those env vars (good luck)
3. Run `docker-compose run -d map-files`
import threading
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import requests
import json
import ipc
from pricewatch import pricewatch
from random import randrange
import datetime
from captcha.image import ImageCaptcha
import math
import re
import hashlib
import asyncio
from websockets.sync.client import connect

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX')


bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all(), description="BTC Bot")
def ipc_loop(og_loop):
	loop = asyncio.new_event_loop()
	task = loop.create_task(ipc.listen(bot, og_loop))
	asyncio.set_event_loop(loop)
	loop.run_forever()

@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))
	print(discord.__version__)
	if(os.getenv('ENABLE_TIPS') == "1"):
		og_loop = asyncio.get_event_loop()
		thread = threading.Thread(target=ipc_loop, args=[og_loop])
		thread.start()
		
	watcher = pricewatch()
	await watcher.watch(bot)
	
@bot.event
async def setup_hook() -> None:
	cogs = [i for i in os.listdir("cogs") if i.endswith(".py")]
	for cog in cogs:
		cog_name = cog.split(".py")[0]
		await bot.load_extension("cogs.{0}".format(cog_name))

@bot.event
async def on_message(message):
	#handle public channels
	if(str(message.channel.type) != "private"):
		if(message.channel.name == "new-joins"):
			if os.getenv('ENABLE_BAN_PATTERNS'):
				for pattern in os.getenv('BAN_PATTERNS'):
					print(re.search(pattern, message.author.name))
					if(re.search(pattern, message.author.name) != None):
						await message.channel.send("banned " + message.author.name)
						await message.author.ban()
		#remove blacklisted content
		if os.getenv('ENABLE_BLACKLIST') == "1":
			if hasattr(message.author, 'roles') and not any(role.name == os.getenv('MOD_ROLE') or role.name == os.getenv('') for role in message.author.roles):
				blacklist = list(filter(None, os.getenv('BLACKLIST').split(",")))
				if len(blacklist) != 0:
					for item in blacklist:
						if message.content.lower().find(item) != -1:
							print("Deleting Message: " + message.author.name + " " + message.author.mention + " - "+ message.content)
							await message.delete()
		#remove disallowed content from image only channels
		if os.getenv('ENABLE_IMAGEONLY') == "1" and hasattr(message.channel, 'name') and message.channel.name == os.getenv('IMAGEONLY_CHANNEL'):
			if hasattr(message.author, 'roles') and not any(role.name == "mod" for role in message.author.roles):
				if message.content.find("tenor.com") != -1 or message.content.find("youtube.com") != -1 or message.content.find("reddit.com") != -1 or message.content.find("youtu.be.com") != -1:
					print("whitelsit meme")
					await bot.process_commands(message)
				else:
					imageFound = True
					for a in message.attachments:
						if not isinstance(a.width, int):
							imageFound = False
							break
					try:
						if(len(message.attachments) < 1 or not imageFound ):
							await message.delete()
					except:
						await message.delete()
		#remove stickers
		if os.getenv('ENABLE_DELETE_STICKERS') == 1 and len(message.stickers) > 0:
			await message.delete()

		#add easter eggs
		if os.getenv('ENABLE_EASTER_EGG') == 1 and message.content.find(os.getenv('EASTER_EGG_TRIGGER')) != -1 and randrange(100) <= int(os.getenv('EASTER_EGG_PERCENT_CHANCE')):
			await message.channel.send(os.getenv('EASTER_EGG'))
	#handle DM's
	elif os.getenv('ENABLE_ANTI_BOT') == "1" and message.author.name != bot.user.name:
		member = message.author
		#look for possible captcha response
		if message.content.upper() == str(hashlib.sha256(str(round(math.sqrt(int(member.id)/int(os.getenv('SALT1')) + int(os.getenv('SALT2'))))).encode("utf-8")).hexdigest())[:8].upper():
			for guild in bot.guilds:
				role = discord.utils.get(guild.roles, id=int(os.getenv('USER_ROLE')))
				if role == None:
					print("can't find role in " + guild.name)
					continue
				member = guild.get_member(message.author.id)
				await member.add_roles(role)
			await message.channel.send("Thank you, welcome to the chat.")

	await bot.process_commands(message)

@bot.event
async def on_member_join(member):
	if os.getenv('ENABLE_ANTI_BOT') == "1" and os.getenv('NEW_USER_MSG') != "":
		await member.send(os.getenv('NEW_USER_MSG'))
		await member.send("Please complete the following captcha:")
		image = ImageCaptcha()
		data = image.generate(str(hashlib.sha256(str(round(math.sqrt(int(member.id)/int(os.getenv('SALT1')) + int(os.getenv('SALT2'))))).encode("utf-8")).hexdigest())[:8].upper())
		await member.send(file=discord.File(data, 'captcha.png'))

@bot.event
async def on_message_delete(message):
	if os.getenv('ENABLE_DELETE_LOG') == "1":
		for guild in bot.guilds:
					for channel in guild.channels:
						if channel.name == os.getenv('REPORT_CHANNEL'):
							msg = "new message deleted: " + message.content + " " + "-" + message.author.mention
							await channel.send(msg)




# Disables the default help command from discord.py
bot.remove_command('help')
bot.run(TOKEN)


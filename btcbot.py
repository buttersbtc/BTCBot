import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import requests
import json
from pricewatch import pricewatch
from random import randrange
import datetime
from captcha.image import ImageCaptcha
import math

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX')

bot = commands.Bot(command_prefix=PREFIX, description="BTC Bot")

@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))
	print(discord.__version__)
	watcher = pricewatch()
	await watcher.watch(bot)

# Loads all commands from the cogs directory
cogs = [i for i in os.listdir("cogs") if i.endswith(".py")]

for cog in cogs:
	cog_name = cog.split(".py")[0]
	bot.load_extension("cogs.{0}".format(cog_name))

#URL blacklist
@bot.event
async def on_message(message):
	#handle public channels
	if(str(message.channel.type) != "private"):
		#remove blacklisted content
		if os.getenv('ENABLE_BLACKLIST') == "1":
			if hasattr(message.author, 'roles') and not any(role.name == os.getenv('MOD_ROLE') for role in message.author.roles):
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
	elif message.author != bot.user and os.getenv('ENABLE_ANTI_BOT') == 1:
		print(bot.user.name)
		member = message.author
		#look for possible captcha response
		print('captcha : ' + str(round(math.sqrt(int(member.id)/int(os.getenv('SALT1')) + int(os.getenv('SALT2'))))))
		if message.content == str(round(math.sqrt(int(member.id)/int(os.getenv('SALT1')) + int(os.getenv('SALT2'))))):
			#give perms if they dont have already
			if not hasattr(message.author, 'roles') or not any(role.name == os.getenv('USER_ROLE') for role in message.author.roles):
				await member.add_roles(os.getenv('USER_ROLE'))
				await member.send("Thank you, welcome to the chat.")

		else:
			if message.content[0:1] != os.getenv('BOT_PREFIX'):
				await member.send(os.getenv('ERROR'))
				USER_ARR.append(member.id)
				#rate limit

	await bot.process_commands(message)

@bot.event
async def on_member_join(member):
	print("new join: " + member.mention)
	if os.getenv('ENABLE_ANTI_BOT') == "1" and os.getenv('NEW_USER_MSG') != "":
		await member.send(os.getenv('NEW_USER_MSG'))
		await member.send("Please complete the following captcha:")
		image = ImageCaptcha()
		data = image.generate(str(round(math.sqrt(int(ctx.message.author.id)/int(os.getenv('SALT1')) + int(os.getenv('SALT2'))))))
		await member.send(file=discord.File(data, 'captcha.png'))


# Disables the default help command from discord.py
bot.remove_command('help')
bot.run(TOKEN)


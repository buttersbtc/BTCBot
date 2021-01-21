import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import requests
import json
from pricewatch import pricewatch
from random import randrange

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
	if os.getenv('ENABLE_BLACKLIST') == "1" and not any(role.name == "mod" for role in message.author.roles):
		blacklist = list(filter(None, os.getenv('BLACKLIST').split(",")))
		if len(blacklist) == 0:
			return

		for item in blacklist:
			if message.content.lower().find(item) != -1:
				print("Deleting Message: " + message.author.mention + " - "+ message.content)
				await message.delete()
	if os.getenv('ENABLE_IMAGEONLY') == "1" and message.channel.name == os.getenv('IMAGEONLY_CHANNEL') and not any(role.name == "mod" for role in message.author.roles):
		if message.content.find("https://tenor.com") != -1 or message.content.find("https://youtube.com") != -1 or message.content.find("reddit.com") != -1 or message.content.find("https://youtu.be.com") != -1 or message.content.find("https://m.youtube.com") != -1:
			await bot.process_commands(message)
			return
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
	if message.content.find(os.getenv('EASTER_EGG_TRIGGER')) != -1 and randrange(100) <= int(os.getenv('EASTER_EGG_PERCENT_CHANCE')):
		await message.channel.send(os.getenv('EASTER_EGG'))

	await bot.process_commands(message)

# Disables the default help command from discord.py
bot.remove_command('help')
# bot.run(username, password, bot=False)
bot.run(TOKEN)


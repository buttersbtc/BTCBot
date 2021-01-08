import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import requests
import json

class pricewatch():
	async def watch(self, bot):
		while(1):
			await asyncio.sleep(5)
			try:
				api = "http://preev.com/pulse/units:btc+usd/sources:bitstamp+kraken"

				r = requests.get(api)
				data = json.loads(r.text)

				price = data["btc"]["usd"]["bitstamp"]["last"]
				price = round(float(price),2)
				price = "${:,.2f} USD".format(float(price))

				await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=price))
			except:
				print("pricew watch fail")
	def __init__(self):
		print("Started Price Watch")

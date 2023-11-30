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
				api = "https://api.coincap.io/v2/assets/bitcoin"

				r = requests.get(api, timeout=5)
				data = json.loads(r.text)

				price = data["data"]["priceUsd"]
				price = round(float(price),2)
				price = "${:,.2f} USD".format(float(price))

				await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=price))
			except:
				print("price watch fail")
	def __init__(self):
		print("Started Price Watch")

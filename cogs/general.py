import discord
from discord.ext import commands
import requests
import json
from random import randrange

class General(commands.Cog):
	"""General commands"""
	def __init__(self, bot):
		self.bot = bot

	async def on_ready(self):
		print("General commands loaded")

	# Price - All currencies enabled by the APi are automatically supported. Add a currency formatting string to change the way a given currency is displayed
	#To add a new item to the price call make a new entry in the itemDic with the cost and formatStr, the key being the string  used to call that item
	@commands.command()
	async def price(self, ctx, arg="noargs"):
		#Price string details
		currencyFormatDic = {
			"default":"${:,.2f} ",
			"gbp":"£{:,.2f} GBP",
			"eur":"€{:,.2f} EUR",
			"brl":"R${:,.2f} BRL",
			"vef":"B${:,.0f} Venezuelan Bolívar",
			"jpy":"¥{:,.0f} JPY",
			"cny":"¥{:,.0f} CNY",
			"ils":"₪{:,.0f} ILS",
			"inr":"₹{:,.2f} INR",
			"zar":"R{:,.2f} ZAR",
			"rub":"₽{:,.2f} RUB"
			}
		itemDic = {
			"mac": {"cost": 5.71, "formatStr":"**1 Bitcoin** is worth **:hamburger: {:.2f} Big Macs**"},
			"mcr": {"cost": 4.29, "formatStr":"**1 Bitcoin** is worth **:pig2: {:.2f} McRibs**"},
			"cru": {"cost": 2.99, "formatStr":"**1 Bitcoin** is worth **:taco: {:.2f} Crunchwraps Supreme**"},
			"but": {"cost": 0.5, "formatStr":"**1 Bitcoin** is worth **:butter: {:.2f} Sticks of Butter**"},
			"lam": {"cost": 521465, "formatStr":"**:race_car: 1 Lamborghini Aventador SVJ** costs **{:.2f} Bitcoin**"},
			"coldcards": {"cost": 119.27, "formatStr":"**1 Bitcoin** is worth **{:.2f} Coldcards"}
			}

		arg = arg.lower()

		#route to other func if exists
		func = getattr(self, arg , None)
		if(callable(func)):
			await func(ctx)
			return

		#handle items first, fallback to currencies
		isItem = arg in itemDic
		item = ""
		if isItem:
			item = arg

		if arg == "noargs" or isItem:
			arg = "usd"
		
		try:
			api = "http://preev.com/pulse/units:btc+" + arg + "/sources:bitstamp+kraken"
			r = requests.get(api)
			data = json.loads(r.text)
		except:
			return

		price = data["btc"]["usd"]["bitstamp"]["last"]
		if arg != "usd":
			conversion = data[arg]["usd"]["other"]["last"]
			price = float(price)/float(conversion)
		if isItem:
			if itemDic[item]["cost"] < float(price):
				price = float(price)/itemDic[item]["cost"]
			else:
				price = itemDic[item]["cost"]/float(price)

		currencyStr = ""
		if arg in currencyFormatDic:
			currencyStr = currencyFormatDic[arg]
		elif isItem:
			currencyStr = itemDic[item]["formatStr"]
		else:
			currencyStr = currencyFormatDic["default"] + arg.upper()
		
		price = currencyStr.format(float(price))
		message_string = ""
		if isItem:
			message_string = price
		else:
			message_string = "**1 Bitcoin** is worth **" + price + "**"
		
		await ctx.send(message_string)

	# Bitcoin is a btc
	@commands.command()
	async def btc(self, ctx):
		message_string = "**1 Bitcoin** is worth **1 Bitcoin**"
		await ctx.send(message_string)
	

	# Fetches price in cats
	@commands.command()
	async def cat(self, ctx):
		message_string = "**:black_cat: stop trying to price cats!"
		await ctx.send(message_string)

	# Fetches price in Strong
	@commands.command()
	async def strong(self, ctx):
		if randrange(25) == 1:
			await ctx.send("oh. that guy.")
		else:
			await ctx.send("who?")

def setup(bot):
	bot.add_cog(General(bot))
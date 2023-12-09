from constants import ITEM_DICT, CURRENCY_FORMAT_DICT, BLACKLIST
from operator import truediv
import os
import discord
from discord.ext import commands
import numpy
import requests
import json
from random import randrange
import math
import datetime

class General(commands.Cog):
	"""General commands"""
	def __init__(self, bot):
		self.bot = bot

	async def on_ready(self):
		print("General commands loaded")

	# Price - All currencies enabled by the APi are automatically supported. Add a currency formatting string to change the way a given currency is displayed
	#To add a new item to the price call make a new entry in the itemDic with the cost and formatStr, the key being the string  used to call that item
	@commands.command()
	async def price(self, ctx, *args):
		if len(args) == 0:
			arg="noargs"
		else:
			arg = args[0].lower()

		if len(args) >= 2:
			arg = args[0].lower()
			arg2 = args[1].lower()
		else:
			arg2 = "noarg"

		if arg in BLACKLIST:
			return

		if arg =="sats":
			await ctx.channel.send("**1 Bitcoin** is equal to **100,000,000 Satoshis**")
			return
			
		if arg == "help":
			await ctx.channel.send("**Currency Eamples**: !p gbp, !p cad, !p xau")
			keys = ""
			for k in ITEM_DICT.keys():
				keys += k + ", "
			keys = keys[0:len(keys)-2]
			await ctx.channel.send("**Other Supported Items**: " + keys)
			await ctx.channel.send("**!p <item> sats** will give you the cost of the item in satoshis")
			return

		#route to other func if exists
		func = getattr(self, arg , None)
		if(callable(func)):
			await func(ctx)
			return

		#handle items first, fallback to currencies
		isItem = arg in ITEM_DICT
		item = ""
		if isItem:
			item = arg

		if arg == "noargs" or isItem:
			arg = "usd"
		#call the api for our currency
		try:
			api = "https://api.coincap.io/v2/assets/bitcoin"
			r = requests.get(api, timeout=10)
			data = json.loads(r.text)

			api_rates = "https://api.coincap.io/v2/rates/"
			r_rates = requests.get(api_rates, timeout=10)
			data_rates = json.loads(r_rates.text)

		except:
			await ctx.send("Price APi is currently slow to respond. Try again later.")
			return

		price = data["data"]["priceUsd"]
		skipConvert = False

		#convert if necessary or do item calcs.
		found_currency = False

		if arg != "usd" and not skipConvert:
		
			for i in data_rates["data"]:
				if i["symbol"] == arg.upper():
					found_currency = True
					price = float(price) / float(i["rateUsd"])
		
		if found_currency == False:
			arg = "USD"
		
		if isItem:
			if ITEM_DICT[item]["single"] == False:
				if ITEM_DICT[item]["cost"] < float(price) and arg2=="sats":
					price = ITEM_DICT[item]["cost"]/float(price) * 100000000
				else:
					price = float(price)/ITEM_DICT[item]["cost"]
					if arg2 == "sats":
						price = price * 100000000

			else:
				price = ITEM_DICT[item]["cost"]/float(price)
				if arg2 == "sats":
					price = price * 100000000
		else:
			if arg2 == "sats":
				price = 100000000/float(price)



		currencyStr = ""
		if arg in CURRENCY_FORMAT_DICT:
			if arg2 == "sats":
				currencyStr = "**1 " + arg.upper()  + "** is **" + "{:,.0f} Satoshis**"
			else:
				currencyStr = CURRENCY_FORMAT_DICT[arg]

		elif isItem:
			if ITEM_DICT[item]["single"] == False:
				if arg2 == "sats":
					currencyStr = "**" + ITEM_DICT[item]["emoji"] + " 1 " + ITEM_DICT[item]["name"] + "**" + " costs **" + "{:,.0f}" + " Satoshis**"
				else:
					currencyStr = "**1 Bitcoin** is worth **" + ITEM_DICT[item]["emoji"] + " {:,.0f}" + " " + ITEM_DICT[item]["name"] + "**"
			else:
				if arg2 == "sats":
					currencyStr = "**" + ITEM_DICT[item]["emoji"] + " 1 " + ITEM_DICT[item]["name"] + "**" + " costs **" + "{:,.0f}" + " Satoshis**"
				else:
					currencyStr = "**" + ITEM_DICT[item]["emoji"] + " 1 " + ITEM_DICT[item]["name"] + "**" + " costs **" + "{:,.2f}" + " Bitcoin**"
		else:
			if arg2 == "sats":
				currencyStr = "**1 " + arg.upper()  + "** is **" + "{:,.0f} Satoshis**"
			else:
				currencyStr = CURRENCY_FORMAT_DICT["default"] + arg.upper()

		
		price = currencyStr.format(float(price))
		
		message_string = ""
		if isItem:
			message_string = price
		else:
			if arg2 == "sats":
				message_string = price
			else:	
				message_string = "**1 Bitcoin** is worth **" + price + "**"
		
		await ctx.send(message_string)

	# price synonym
	@commands.command()
	async def p(self, ctx, *args):
		await General(self).price(self, ctx, *args)

	# Bitcoin is a btc
	@commands.command()
	async def btc(self, ctx):
		message_string = "**1 Bitcoin** is worth **1 Bitcoin**"
		await ctx.send(message_string)

	# Fetches price in cats
	@commands.command()
	async def cat(self, ctx):
		message_string = "**:black_cat:** stop trying to price cats!"
		await ctx.send(message_string)

	# Fetches hours worked for a bitcoin at a rate.
	@commands.command()
	async def wage(self, ctx, *args):

		if len(args) != 2:
			await ctx.send("To use wage include the amount earned in the wage and a currency. ex. !wage 15.00 USD")
			return

		arg = args[1].lower()
		wage = args[0]

		try:
			api = "https://api.coincap.io/v2/assets/bitcoin"
			r = requests.get(api)
			data = json.loads(r.text)

			api_rates = "https://api.coincap.io/v2/rates/"
			r_rates = requests.get(api_rates)
			data_rates = json.loads(r_rates.text)

		except:
			await ctx.send("The price API is currently unavailable")
			return
		price = data["data"]["priceUsd"]
		if arg != "usd":
			for currency in data_rates["data"]:
				if currency["symbol"].lower() == arg:
					conversion = currency["rateUsd"]
					price = float(price)/float(conversion)

		price = float(price)/float(wage)
		message_string = "**1 Bitcoin** costs **{:,.0f}** hours".format(float(price))

		await ctx.send(message_string)
		
	# Fetches Bitcoin all time high (ATH) price
	@commands.command()
	async def ath(self, ctx):
		api = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin&order=market_cap_desc&per_page=100&page=1&sparkline=false"
		r = requests.get(api)
		data = json.loads(r.text)
		price = data[0]["ath"]
		message_string = "**Bitcoin ATH** is currently **${:,.2f}**".format(float(price))
		await ctx.send(message_string)

	@commands.command()
	async def ff(self, ctx, *args):
		fun_facts = ["**Fun Fact:** Bitcoin is the first decentralized digital currency",
					 "**Fun Fact:** Bitcoin was created by Satoshi Nakamoto in 2009",
					 "**Fun Fact:** Bitcoin is the first cryptocurrency",
					 "**Fun Fact:** Bitcoin is the first cryptocurrency to use blockchain technology",
					 "**Fun Fact:** Bitcoin is the first cryptocurrency to use proof of work",
					 "**Fun Fact:** Bitcoin is the first cryptocurrency to use a distributed ledger",
					 "**Fun Fact:** Bitcoin is the first cryptocurrency to use a peer-to-peer network",
					 "**Fun Fact:** Bitcoin is the first cryptocurrency to use a SHA-256 hash function",
					 "**Fun Fact:** The smallest unit of Bitcoin is called a Satoshi, worth one hundred millionth of a single Bitcoin.",
					 "**Fun Fact:** In 2021, El Salvador became the first country to adopt Bitcoin as legal tender.",
					 "**Fun Fact:** At one point, the FBI was one of the world’s largest owners of Bitcoin, due to seizures from the Silk Road, an online black market.",
					 "**Fun Fact:** The world's first Bitcoin ATM was installed in Vancouver, Canada, in 2013.",
					 "**Fun Fact:** The first Bitcoin transaction was made by Satoshi Nakamoto to Hal Finney in 2009.",
					 "**Fun Fact:** It’s estimated that around 20% of all Bitcoins are lost or inaccessible, mainly due to forgotten passwords or broken hard drives.",
					 "**Fun Fact:** The first real-world transaction using Bitcoin was in 2010, when a programmer named Laszlo Hanyecz bought two pizzas for 10,000 Bitcoins.",
					 "**Fun Fact:** In 2010, a vulnerability in the Bitcoin protocol was exploited, creating billions of Bitcoins. The bug was quickly fixed, and the extra Bitcoins were erased.",
					 "**Fun Fact:** Bitcoin is the first cryptocurrency to use a distributed timestamp server to verify transactions.",
					 "**Fun Fact:** Bitcoin operates on a decentralized network, meaning it isn’t controlled by any single entity or government.",
					 "**Fun Fact:** Bitcoins are created through a process called mining, which involves using computer power to solve complex mathematical problems.",
					 "**Fun Fact:** Approximately every four years, the reward for Bitcoin mining halves, an event known as “halving.” This reduces the rate at which new Bitcoins are created.",
					 "**Fun Fact:** There will only ever be 21 million Bitcoins in existence, making it a deflationary currency."
					 ]

		message_string = fun_facts[randrange(len(fun_facts))]
		await ctx.send(message_string)

	# convert between two currencies
	@commands.command()
	async def convert(self, ctx, *args):
		if len(args) < 3:
			await ctx.send("To use convert use the format: !convert 15.00 USD BTC or !convert 10000 sat mBTC")
			return
		sourceCurrencyRate = 0
		comparisons = []
		_args = []
		sat = False
		for arg in args:
			if(arg.upper() == "SAT"):
				sat = True
				_args.append("BTC")
				continue
			_args.append(arg.upper())
		api_rates = "https://api.coincap.io/v2/rates/"
		r_rates = requests.get(api_rates, timeout=10)
		data_rates = json.loads(r_rates.text)
		sourceCurrency = _args[1].upper()
		message_string = _args[0] + " " + _args[1] + " is equal to:"
		_args.remove(_args[1])
		for currency in data_rates['data']:
			if currency['symbol'].upper() == sourceCurrency:
				sourceCurrencyRate = currency['rateUsd']
			if currency['symbol'].upper() in _args:
				print(sat)
				print(currency['symbol'].upper())
				if sat and currency['symbol'].upper() == "BTC":
					comparisons.append(["SAT", float(currency['rateUsd'])/100000000])
				else:
					comparisons.append([currency['symbol'], currency['rateUsd']])
		print(comparisons)
		if len(comparisons) != len(args) - 2:
			print("something fucky in here")
		for comparison in comparisons:
			val = (float(sourceCurrencyRate) * float(_args[0])) / float(comparison[1]) 
			if val > 0.01:
				message_string += " " + '{:,.2f}'.format(val) + " " + comparison[0] + ","
			else:
				message_string += " " + '{:,.8f}'.format(val) + " " + comparison[0] + ","

		message_string = message_string[:len(message_string)-1]

		await ctx.send(message_string)

	@commands.command()
	async def help(self, ctx, *args):
		message_string = "Commands this bot accepts:"
		sorted_cmd = sorted(self.bot.commands, key=lambda cmd: cmd.name)
		for cmd in sorted_cmd:
			message_string +=  " " + os.getenv('BOT_PREFIX') + f"{cmd},"
		await ctx.send(message_string[:len(message_string)-1])

async def setup(bot):
	await bot.add_cog(General(bot))

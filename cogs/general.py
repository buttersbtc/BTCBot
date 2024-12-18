import hashlib
import math
import random

import BitcoinAPI as api
from constants import ITEM_DICT, CURRENCY_FORMAT_DICT, BLACKLIST, BITCOIN_IN_SATS, FUN_FACTS, REMOVE_HELP, CHART_TYPES
from operator import truediv
import os
from discord.ext import commands
import requests
import json
from random import randrange

class General(commands.Cog):
	"""General commands"""
	def __init__(self, bot):
		self.bot = bot
		self.fact_generator = self.get_fact()

	async def on_ready(self):
		print("General commands loaded")

	# Price - All currencies enabled by the APi are automatically supported. Add a currency formatting string to change the way a given currency is displayed
	#To add a new item to the price call make a new entry in the itemDic with the cost and formatStr, the key being the string  used to call that item
	# @commands.command()
	# async def price(self, ctx, *args):
	# 	if len(args) == 0:
	# 		arg = "usd"
	# 		args = ["usd"]
	# 	else:
	# 		arg = args[0]

	# 	arg = arg.lower()

	# 	if arg == "help":
	# 		await ctx.channel.send("**Currency Examples**: !p gbp, !p cad, !p xau")
	# 		keys = ""
	# 		for k in ITEM_DICT.keys():
	# 			keys += k + ", "
	# 		keys = keys[0:len(keys)-2]
	# 		await ctx.channel.send("**Other Supported Items**: " + keys)
	# 		await ctx.channel.send("**!p <item> sats** will give you the cost of the item in satoshis")
	# 		return
	# 	if arg in ITEM_DICT:
	# 		await self.price_item(ctx, args)
	# 		return
	# 	if arg == "sats":
	# 		await self.price_sats(ctx, arg)
	# 		return
	# 	await self.price_currency(ctx, args)

	# async def price_sats(self, ctx, *args):
	# 	await ctx.channel.send("**1 bitcoin** is equal to **100,000,000 satoshis**")

	# async def price_currency(self, ctx, currencies):
	# 	currency = currencies[0]
	# 	price, error = api.get_current_price()
	# 	if error:
	# 		await ctx.channel.send("Price API is currently slow to respond. Try again later.")
	# 		return
	# 	price, _, error = api.get_current_price_in_currency(currency)
	# 	if error:
	# 		await ctx.channel.send("Unable to find currency code: " + currency)
	# 		return
	# 	index = "default"
	# 	prefix = "**1 bitcoin** is worth "
	# 	suffix = " " + currency.upper()
	# 	if currency in CURRENCY_FORMAT_DICT:
	# 		index = currency
	# 		suffix = ""
	# 	if "sats" in currencies or "sat" in currencies:
	# 		price = 100000000 / price
	# 		await ctx.channel.send("**1 "+ currency.upper() +"** is worth **" + "{:,.0f}".format(price) + " satoshi**")
	# 	else:
	# 		price = prefix + "**" + CURRENCY_FORMAT_DICT[index].format(price) + suffix +"**"
	# 		await ctx.channel.send(price)

	# async def price_item(self, ctx, items):
	# 	item = items[0]
	# 	if not item in ITEM_DICT:
	# 		await ctx.channel.send("Item not supported")
	# 		return
	# 	price, error = api.get_current_price()
	# 	if error:
	# 		await ctx.channel.send("Price API is currently slow to respond. Try again later.")
	# 		return
	# 	item_map = ITEM_DICT[item]
	# 	emoji = item_map["emoji"]
	# 	name = item_map["name"]
	# 	suffix = "bitcoin"
	# 	if "sats" in items or "sat" in items:
	# 		price = price / 100000000
	# 		price = ITEM_DICT[item]["cost"] / price
	# 		await ctx.channel.send(f"**1 {emoji} {name}** is worth **{price:,.0f} satoshi**")
	# 	elif item_map["single"]:
	# 		price = item_map["cost"] / price
	# 		await ctx.channel.send(f"**1 {emoji} {name}** is worth **{price:,.2f} bitcoin**")
	# 	else:
	# 		price = price / ITEM_DICT[item]["cost"]
	# 		await ctx.channel.send(f"**1 bitcoin** is worth **{price:,.2f} {emoji} {name}**")
	# 	return

	# price synonym
	# @commands.command()
	# async def p(self, ctx, *args):
	# 	await self.price(self, ctx, *args)
		# await General(self).price(self, ctx, *args)

	# Bitcoin is a btc
	# @commands.command()
	# async def btc(self, ctx):
	# 	message_string = "**1 Bitcoin** is worth **1 Bitcoin**"
	# 	await ctx.send(message_string)

	# Fetches price in cats
	# @commands.command()
	# async def cat(self, ctx):
	# 	message_string = "**:black_cat:** stop trying to price cats!"
	# 	await ctx.send(message_string)

	# Fetches hours worked for a bitcoin at a rate.
	# @commands.command()
	# async def wage(self, ctx, *args):
	# 	if len(args) != 2 or not args[0].isdigit() or math.floor(int(args[0])) == 0:
	# 		await ctx.send("To use wage include the amount earned in the wage and a currency. ex. !wage 15.00 USD")
	# 		return

	# 	arg = args[1].lower()
	# 	wage = float(args[0])
	# 	format_string = "**1 Bitcoin** costs **{:,.0f}** hours"

	# 	if arg == "usd":
	# 		price, error = api.get_current_price()
	# 		if error:
	# 			return await ctx.send("The price API is currently unavailable")

	# 		return await ctx.send(format_string.format(price/wage))

	# 	if arg == "sats":
	# 		return await ctx.send(format_string.format(BITCOIN_IN_SATS/wage))
	# 	price, _, error = api.get_current_price_in_currency(arg)
	# 	if error:
	# 		return await ctx.send(error)

	# 	await ctx.send(format_string.format(price/wage))

	# Fetches Bitcoin all time high (ATH) price
	# @commands.command()
	# async def ath(self, ctx, *args):
	# 	if(len(args) == 0):
	# 		ath, error = api.get_bitcoin_ath("usd")
	# 	else:
	# 		ath, error = api.get_bitcoin_ath(args[0].lower())
	# 	if error:
	# 		return await ctx.send(error)

	# 	message_string = f"**Bitcoin ATH** is currently **{ath}**"
	# 	await ctx.send(message_string)

	# @staticmethod
	# def get_fact():
	# 	while True:
	# 		random.shuffle(FUN_FACTS)
	# 		for fact in FUN_FACTS:
	# 			yield fact

	# @commands.command()
	# async def ff(self, ctx):
	# 	await ctx.send(next(self.fact_generator))

	@commands.command()
	async def sha256(self, ctx, *args):
		if(len(args) == 0) or args[0] == "help" or len(args) < 3:
			return await ctx.send("To use sha256 use the format: `!sha256 <ENT> <base> <entropy>` where base is b (binary) or h (hexadecimal) and ENT is 128, 160, 192, 224, or 256")
		m = hashlib.sha256()
		supported_entropy = ["128", "160", "192", "224", "256"]
		supported_base = ["b", "h"]
		ENT, BASE, ENTROPY = args
		if BASE not in supported_base:
			return await ctx.send("base must be b (binary) or h (hexadecimal)")
		if ENT not in supported_entropy:
			return await ctx.send("entropy must be 128, 160, 192, 224, or 256")
		try:
			if BASE == "b":
				if len(ENTROPY) != int(ENT):
					return await ctx.send(f"entropy length must be {ENT}")
				m.update(bytes.fromhex(self.bin_to_hex(ENTROPY)))
				return await ctx.send("0x" + m.hexdigest())
			else:
				ENT = int(ENT)
				if len(ENTROPY) != ENT / 4:
					return await ctx.send("entropy length must be " + str(int(ENT / 4)))
				m.update(bytes.fromhex(ENTROPY))
				return await ctx.send("0x" + m.hexdigest())
		except ValueError as _:
			return await ctx.send(f"entropy must be a valid {ENT} bit {BASE} number")

	# convert between two currencies
	@commands.command()
	async def convert(self, ctx, *args):
		if len(args) < 3:
			await ctx.send("To use convert use the format: !convert 15.00 USD BTC or !convert 10000 sat mBTC")
			return

		sourceCurrencyRate = 0
		comparisons = []
		_args = []
		btcUnits = [["MSAT",100000000, "msat"], ["SAT",100000000, "sat"], ["SATS", 100000000, "sats"], ["ΜBTC", 1000000, "μBTC"], ["UBTC", 1000000, "μBTC"], ["MBTC", 1000, "mBTC"], ["CBTC", 100, "cBTC"], ["DBTC", 10, "dBTC"], ["BTC", 1, "BTC"]]
		bitcoinRate = 0
		btcUnitConversions = []

		for arg in args:
			for unit in btcUnits:
				if(arg.upper() == unit[0]):
					btcUnitConversions.append(unit)
					continue
			_args.append(arg.upper())

		api_rates = "https://api.coincap.io/v2/rates/"
		r_rates = requests.get(api_rates, timeout=10)
		data_rates = json.loads(r_rates.text)
		sourceCurrency = _args[1]
		arg1Formatted = _args[1]
		for unit in btcUnitConversions:
			if _args[1] == unit[0]:
				arg1Formatted = unit[2]

		message_string = _args[0] + " " + arg1Formatted + " is equal to:"
		_args.remove(_args[1])
		for currency in data_rates['data']:
			if currency['symbol'].upper() == "BTC":
				bitcoinRate = float(currency['rateUsd'])
			if currency['symbol'].upper() == sourceCurrency.upper():
				sourceCurrencyRate = float(currency['rateUsd'])
			if currency['symbol'].upper() in _args and currency['symbol'].upper() != "BTC":
				comparisons.append([currency['symbol'], float(currency['rateUsd'])])

		for unit in btcUnits:
			if unit[0] == sourceCurrency:
				sourceCurrencyRate = bitcoinRate / unit[1]
			elif unit in btcUnitConversions:
				comparisons.append([unit[2], bitcoinRate / unit[1]])
		for item in ITEM_DICT:
			if item.upper() == sourceCurrency.upper():
				sourceCurrencyRate = ITEM_DICT[item]["cost"]
				message_string = _args[0] + " " + ITEM_DICT[item]["name"] + " " + ITEM_DICT[item]["emoji"] + " is equal to:"
			elif item.upper() in _args:
				comparisons.append([ITEM_DICT[item]["name"] + " " + ITEM_DICT[item]["emoji"], ITEM_DICT[item]["cost"]])

		for comparison in comparisons:
			val = sourceCurrencyRate * float(_args[0]) / comparison[1]
			if val > 0.01:
				message_string += " " + '{:,.2f}'.format(val) + " " + comparison[0] + ","
			else:
				message_string += " " + '{:,.8f}'.format(val) + " " + comparison[0] + ","

		message_string = message_string[:len(message_string)-1]

		if len(comparisons) == 0:
			message_string = "Unable to find the requested currencies for conversion."

		await ctx.send(message_string)

	@commands.command()
	async def chart(self, ctx, *args):
		if len(args) != 2:
			return await ctx.send('''Please use the chart command in the format `'''+os.getenv('BOT_PREFIX')+'''chart chartname timespan` where chartname is one of: 
```
''' + ", ".join(CHART_TYPES) + '''
```
and timespan is in the format #days, #weeks, #months, #years etc. ex. `'''+os.getenv('BOT_PREFIX')+'''chart median-confirmation-time 10weeks`

''')
		name = args[0]
		timespan = args[1]

		if name in CHART_TYPES :
			file, err = api.get_chart(name, timespan)
		if err != None:
			print(err)
			return await ctx.send("There was an error creating your chart. Make sure your chart name was correct and your timespan had no spaces - ex. `"+os.getenv('BOT_PREFIX')+"chart median-confirmation-time 10weeks`")
		await ctx.send(files=[file])


	@commands.command()
	async def help(self, ctx, *args):
		message_string = "Commands this bot accepts:"
		sorted_cmd = sorted(self.bot.commands, key=lambda cmd: cmd.name)
		for cmd in sorted_cmd:
			if f"{cmd}" not in REMOVE_HELP:
				message_string +=  " " + os.getenv('BOT_PREFIX') + f"{cmd},"
		message_string = message_string[:len(message_string)-1]
		message_string += ". For bot support inquire at <http://bitcointech.help> or in the issues at <https://github.com/buttersbtc/BTCBot/issues>"
		await ctx.send(message_string)

async def setup(bot):
	await bot.add_cog(General(bot))

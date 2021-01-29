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
			"gbp":"£{:,.2f} British Pounds",
			"eur":"€{:,.2f} Euros",
			"brl":"R${:,.2f} Brazillian Reais",
			"vef":"B${:,.0f} Venezuelan Bolívar",
			"jpy":"¥{:,.0f} Japanese Yen",
			"cny":"¥{:,.0f} Chinese Renminbi",
			"ils":"₪{:,.0f} Israeli Shekalim",
			"inr":"₹{:,.2f} Indian Rupees",
			"zar":"R{:,.2f} South African Rands",
			"rub":"₽{:,.2f} Russian Rubles",
			"xau":"{:,.2f} ounces of gold",
			"xag":"{:,.2f} ounces of silver"
			}
		itemDic = {
			"mac": {"cost": 5.71, "formatStr":"**1 Bitcoin** is worth **:hamburger: {:,.0f} Big Macs**"},
			"mcr": {"cost": 4.29, "formatStr":"**1 Bitcoin** is worth **:pig2: {:,.0f} McRibs**"},
			"cru": {"cost": 2.99, "formatStr":"**1 Bitcoin** is worth **:taco: {:,.0f} Crunchwraps Supreme**"},
			"but": {"cost": 0.5, "formatStr":"**1 Bitcoin** is worth **:butter: {:,.0f} Sticks of Butter**"},
			"lam": {"cost": 521465, "formatStr":"**:race_car: 1 Lamborghini Aventador SVJ** costs **{:.2f} Bitcoin**"},
			"coldcards": {"cost": 119.27, "formatStr": "**1 Bitcoin** is worth **:pager: {:.0f} Coldcards**"},
			"egg": {"cost": 0.1208333, "formatStr": "**1 Bitcoin** is worth **:egg: {:,.0f} Large Eggs**"},
			"f40": {"cost": 1350000, "formatStr": "**:race_car: 1 Ferrari F40** costs **{:.2f} Bitcoin**"},
			"420": {"cost": 200, "formatStr": "**1 Bitcoin** is worth **:maple_leaf: {:,.0f} ounces of Marijuana**"},
			"rbx": {"cost": 0.0125, "formatStr": "**1 Bitcoin** is worth **:bricks: {:,.0f} Robux**"},
			"thc": {"cost": 40,
					"formatStr": "**1 Bitcoin** is worth **:maple_leaf: {:,.0f} THC distillate cartridges (1 gram)**"},
			"pod": {"cost": 5.2475, "formatStr": "**1 Bitcoin** is worth **:smoking: {:,.0f} JUUL pods**"},
			"tm3": {"cost": 37990, "formatStr": "**:red_car: 1 Tesla Model 3** costs **{:.2f} Bitcoin**"},
			"rtx": {"cost": 1499, "formatStr": "**1 Bitcoin** is worth **:desktop_computer: {:,.0f} RTX 3090's**"},
			"gum": {"cost": 8.37,
					"formatStr": "**1 Bitcoin** is worth **:teddy_bear: {:,.0f} kilograms of Gummie Bears**"}
		}
	blacklist = {
		"xdg": True,
		"ltc": True,
		"eth": True,
		"xrp": True,
		"bch": True
	}

	arg = arg.lower()

	if arg in blacklist:
		return

	# route to other func if exists
	func = getattr(self, arg, None)
	if (callable(func)):
		await func(ctx)
		return

	# handle items first, fallback to currencies
	isItem = arg in itemDic
	item = ""
	if isItem:
		item = arg

	if arg == "noargs" or isItem:
		arg = "usd"
	# call the api for our currency
	try:
		api = "http://preev.com/pulse/units:btc+" + arg + "/sources:bitstamp+kraken"
		r = requests.get(api)
		data = json.loads(r.text)
	except:
		return
	# look through the response for anything we can use, thanks for the consistent response format preev
	skipConvert = False
	try:
		price = data["btc"]["usd"]["bitstamp"]["last"]
	except:
		try:
			price = data["btc"][arg]["bitstamp"]["last"]
			skipConvert = True
		except:
			price = data["btc"][arg]["kraken"]["last"]
			skipConvert = True

	# convert if necessary or do item calcs.
	if arg != "usd" and not skipConvert:
		conversion = data[arg]["usd"]["other"]["last"]
		price = float(price) / float(conversion)
	if isItem:
		if itemDic[item]["cost"] < float(price):
			price = float(price) / itemDic[item]["cost"]
		else:
			price = itemDic[item]["cost"] / float(price)

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

# price synonym


@commands.command()
async def p(self, ctx, arg="noargs"):
	await General(self).price(self, ctx, arg)


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


# Fox got bear's tail
@commands.command()
async def fox(self, ctx):
	message_string = "**:fox:** 1 Fox is worth 1 Tail of a bear :polar_bear:"
	await ctx.send(message_string)


# old ester egg spam
@commands.command()
async def strong(self, ctx):
	await ctx.message.delete()


# Fetches hours worked for a bitcoin at a rate.
@commands.command()
async def wage(self, ctx, *args):
	if len(args) != 2:
		return

	arg = args[1].lower()
	wage = args[0]

	try:
		api = "http://preev.com/pulse/units:btc+" + arg + "/sources:bitstamp+kraken"
		r = requests.get(api)
		data = json.loads(r.text)
	except:
		return
	skipConvert = False
	try:
		price = data["btc"]["usd"]["bitstamp"]["last"]
	except:
		try:
			price = data["btc"][arg]["bitstamp"]["last"]
			skipConvert = True
		except:
			price = data["btc"][arg]["kraken"]["last"]
			skipConvert = True
	if arg != "usd":
		conversion = data[arg]["usd"]["other"]["last"]
		price = float(price) / float(conversion)

	price = float(price) / float(wage)
	message_string = "**1 Bitcoin** costs **{:,.0f}** hours".format(float(price))

	await ctx.send(message_string)


def setup(bot):
	bot.add_cog(General(bot))
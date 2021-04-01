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
			"mac": {"cost": 5.71, "formatStr":"**1 Bitcoin** is worth **:hamburger: {:,.0f} Big Macs**","single":False},
			"mcr": {"cost": 4.29, "formatStr":"**1 Bitcoin** is worth **:pig2: {:,.0f} McRibs**","single":False},
			"cru": {"cost": 2.99, "formatStr":"**1 Bitcoin** is worth **:taco: {:,.0f} Crunchwraps Supreme**","single":False},
			"but": {"cost": 0.5, "formatStr":"**1 Bitcoin** is worth **:butter: {:,.0f} Sticks of Butter**","single":False},
			"coldcards": {"cost": 119.27, "formatStr":"**1 Bitcoin** is worth **:pager: {:.0f} Coldcards**","single":False},
			"egg": {"cost": 0.1208333, "formatStr":"**1 Bitcoin** is worth **:egg: {:,.0f} Large Eggs**","single":False},
			"420": {"cost": 200, "formatStr":"**1 Bitcoin** is worth **:maple_leaf: {:,.0f} ounces of Marijuana**","single":False},
			"gum": {"cost": 8.37, "formatStr":"**1 Bitcoin** is worth **:teddy_bear: {:,.0f} kilograms of Gummie Bears**","single":False},
			"rbx": {"cost": 0.0125, "formatStr":"**1 Bitcoin** is worth **:bricks: {:,.0f} Robux**","single":False},
			"thc": {"cost": 40, "formatStr":"**1 Bitcoin** is worth **:maple_leaf: {:,.0f} THC distillate cartridges (1 gram)**","single":False},
			"pod": {"cost": 5.2475, "formatStr":"**1 Bitcoin** is worth **:smoking: {:,.0f} JUUL pods**","single":False},
			"furby": {"cost": 300, "formatStr":"**1 Bitcoin** is worth **:owl: {:,.0f} Rare Furbies**","single":False},
			"avo": {"cost": 10, "formatStr":"**1 Bitcoin** is worth **:avocado: {:,.0f} Serves of Avocado Toast**","single":False},
			"chicken": {"cost": 2.85, "formatStr":"**1 Bitcoin** is worth **:chicken: {:,.0f} Rhode Island Red Chickens**","single":False},
			"nana": {"cost": 0.23, "formatStr":"**1 Bitcoin** is worth **:banana: {:,.0f} Bananas**","single":False},
			"bez": {"cost": 74598.083, "formatStr":"**1 Bitcoin** is worth **:man_office_worker: {:,.2f} minutes of Jeff Bezos' time**","single":False},

			# Seperating out items that should be displayed as cost for a single item
			"act": {"cost": 32410, "formatStr":"**:student: Average College Tuition (4 years)** costs **{:,.2f} Bitcoin**","single":True},
			"lam": {"cost": 521465, "formatStr":"**:race_car: 1 Lamborghini Aventador SVJ** costs **{:.2f} Bitcoin**","single":True},
			"lar": {"cost": 259000, "formatStr":"**:race_car: 1 McLaren 600LT 2020** costs **{:.2f} Bitcoin**","single":True},
			"tm3": {"cost": 36990, "formatStr":"**:red_car: 1 Tesla Model 3** costs **{:.2f} Bitcoin**","single":True},
			"rds": {"cost": 200000, "formatStr":"**:race_car: 1 Tesla Roadster 2020** costs **{:.2f} Bitcoin**","single":True},
			"f40": {"cost": 1350000, "formatStr":"**:race_car: 1 Ferrari F40** costs **{:.2f} Bitcoin**","single":True},
			"tay": {"cost": 232904, "formatStr":"**:red_car: 1 Porche Taycan Turbo S** costs **{:.2f} Bitcoin**","single":True},
			"mus": {"cost": 75000, "formatStr":"**:blue_car: 1 Ford Mustang Shelby GT500 2020** costs **{:.2f} Bitcoin**","single":True},
			"fc9": {"cost": 62000000, "formatStr":"**:rocket: 1 SpaceX Falcon 9 Launch** costs **{:,.2f} Bitcoin**","single":True},
			"trn": {"cost": 139900, "formatStr":"**:race_car: 1 Audi RS e-tron GT 2022** costs **{:.2f} Bitcoin**","single":True},
			"bug": {"cost": 2990000, "formatStr":"**:race_car: 1 Bugatti Chiron 2020** costs **{:.2f} Bitcoin**","single":True},
			"gef": {"cost": 1499, "formatStr":"**:desktop_computer: 1 Nvidia GEFORCE RTX 3090** costs **{:.2f} Bitcoin**","single":True},
			"rov": {"cost": 2725000000, "formatStr":"**:robot: :rocket: 1 trip to Mars + rover/drone/skycrane package** costs **{:,.2f} Bitcoin**","single":True}
			}
		satDict = {
			"milk": {"cost": 3.59, "formatStr":"**:milk: 1 Gallon of Milk** costs **{:,.0f} Satoshis**","single":True},
			"cru": {"cost": 2.99, "formatStr":"**:taco: 1 Crunchwrap Supreme** costs **{:,.0f} Satoshis**","single":True},
			"egg": {"cost": 0.1208333, "formatStr":"**:egg: 1 egg** costs **{:,.0f} Satoshis**","single":True},
			"420": {"cost": 200, "formatStr":"**:maple_leaf: 1 Ounce of Weed** costs **{:,.0f} Satoshis**","single":True},
			"iph": {"cost": 999, "formatStr":"**:telephone: 1 iPhone 12 pro** costs **{:,.0f} Satoshis**","single":True},
			"furby": {"cost": 300, "formatStr":"**:owl: 1 Rare Furby** costs **{:,.0f} Satoshis**","single":True},
			"avo": {"cost": 10, "formatStr":"**:avocado: 1 avocado toast** costs **{:,.0f} Satoshis**","single":True},
			"chicken": {"cost": 2.85, "formatStr":"***:chicken: 1 Rhode Island Red Chicken** costs **{:,.0f} Satoshis**","single":True},
			"nana": {"cost": 0.23, "formatStr":"**:banana: 1 banana** costs **{:,.0f} satoshis**","single":True},
			"mac": {"cost": 5.71, "formatStr":"**:hamburger: 1 Big Mac** costs **{:,.0f} Satoshis*","single":True},
			"mcr": {"cost": 4.29, "formatStr":"**:pig2: 1 McRib Sandwich** costs**{:,.0f} Satoshi**","single":True},
			"bez": {"cost": 74598.083, "formatStr":"**:man_office_worker: 1 minute of Jeff Bezos' time** costs **{:,.0f} Satoshis**","single":True},
			}
		blacklist = {
			"xdg":True,
			"ltc":True,
			"eth":True,
			"xrp":True,
			"bch":True
			}

		arg = arg.lower()

		if arg in blacklist:
			return
		
		if arg == "help":
			await ctx.channel.send("**Currency Eamples**: !p gbp, !p cad, !p xau")
			keys = ""
			for k in itemDic.keys():
				keys += k + ", "
			keys = keys[0:len(keys)-2]
			await ctx.channel.send("**Other Supported Items**: " + keys)
			return

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
		#call the api for our currency
		try:
			api = "http://preev.com/pulse/units:btc+" + arg + "/sources:bitstamp+kraken"
			r = requests.get(api)
			data = json.loads(r.text)
		except:
			return
		#look through the response for anything we can use, thanks for the consistent response format preev
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

		#convert if necessary or do item calcs.
		if arg != "usd" and not skipConvert:
			conversion = data[arg]["usd"]["other"]["last"]
			price = float(price)/float(conversion)
		if isItem:
			if itemDic[item]["cost"] < float(price) and itemDic[item]["single"] == False:
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
			price = float(price)/float(conversion)

		price = float(price)/float(wage)
		message_string = "**1 Bitcoin** costs **{:,.0f}** hours".format(float(price))

		await ctx.send(message_string)
		
	#fetches sats for items
	@commands.command()
	async def sat(self, ctx, arg):

		#handle items and call API
		isItem = arg in satDict
		item = ""
		if isItem:
			item = arg
		
		if arg == "noargs" or isItem:
			return
		
		try:
			api = "http://preev.com/pulse/units:btc+" + "usd" + "/sources:bitstamp+kraken"
			r = requests.get(api)
			data = json.loads(r.text)
		except:
			return
			
		#item calcs
		skipConvert = False
		try:
			price = data["btc"]["usd"]["bitstamp"]["last"]
		except:
			try:
				price = data["btc"]["usd"]["bitstamp"]["last"]
				skipConvert = True
			except:
				price = data["btc"]["usd"]["kraken"]["last"]
				skipConvert = True
				
		price = satDic[item]["cost"]/float(price)*100000000

				
		currencyStr = ""
			currencyStr = satDic[item]["formatStr"]

		price = currencyStr.format(float(price))
		message_string = ""
		message_string = price

		
		await ctx.send(message_string)
		
def setup(bot):
	bot.add_cog(General(bot))

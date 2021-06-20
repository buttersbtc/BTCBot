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
	async def price(self, ctx, *args):
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
			"mac":{"cost": 5.71,"name":"Big Macs","emoji":":hamburger:","single":False},
			"mcr":{"cost": 4.29,"name":"McRibs","emoji":":pig2:","single":False},
			"cru":{"cost": 2.99,"name":"Crunchwraps Supreme","emoji":":taco:","single":False},
			"but":{"cost": .5,"name":"Sticks of Butter","emoji":":butter:","single":False},
			"coldcards":{"cost": 119.27,"name":"Coldcards","emoji":":pager:","single":False},
			"egg":{"cost": 0.1208333,"name":"Large Eggs","emoji":":egg:","single":False},
			"420":{"cost": 200,"name":"Ounces of Marijuana","emoji":":maple_leaf:","single":False},
			"gum":{"cost": 8.37,"name":"Kilograms of Gummie Bears","emoji":":teddy_bear:","single":False},
			"rbx":{"cost": 0.0125,"name":"Robux","emoji":":bricks:","single":False},
			"thc":{"cost": 40,"name":"THC distillate cartridges (1 gram)","emoji":":maple_leaf:","single":False},
			"pod":{"cost": 5.2475,"name":"JUUL pods","emoji":":smoking:","single":False},
			"furby":{"cost": 300,"name":"Rare Furbies", "emoji":":owl:","single":False},
			"avo":{"cost": 10,"name":"Serves of Avocado Toast","emoji":":avocado:","single":False},
			"chicken":{"cost": 2.85,"name":"Rhode Island Red Chickens","emoji":":chicken:","single":False},
			"nana":{"cost": 0.23,"name":"Bananas","emoji":":banana:","single":False},
			"bez":{"cost": 74598.083,"name":"minutes of Jeff Bezos' time","emoji":":man_office_worker:","single":False},

			# Seperating out items that should be displayed as cost for a single item
			"lam":{"cost": 521465,"name":"Lamborghini Aventador SVJ","emoji":":race_car:","single":True},
			"act":{"cost": 32410,"name":"Average College Tuition (4 years)","emoji":":student:","single":True},
			"lar":{"cost": 259000,"name":"McLaren 600LT 2020","emoji":":race_car:","single":True},
			"tm3":{"cost": 36990,"name":"Tesla Model 3","emoji":":red_car:","single":True},
			"rds":{"cost": 200000,"name":"Tesla Roadster 2020","emoji":":race_car:","single":True},
			"f40":{"cost": 1350000,"name":"Ferrari F40","emoji":":race_car:","single":True},
			"tay":{"cost": 232904,"name":"Porche Taycan Turbo S","emoji":":red_car:","single":True},
			"mus":{"cost": 75000,"name":"Ford Mustang Shelby GT500 2020","emoji":":blue_car:","single":True},
			"fc9":{"cost": 62000000,"name":"SpaceX Falcon 9 Launch","emoji":":rocket:","single":True},
			"trn":{"cost": 139900,"name":"Audi RS e-tron GT 2022","emoji":":race_car:","single":True},
			"bug":{"cost": 2990000,"name":"Bugatti Chiron 2020","emoji":":race_car:","single":True},
			"nev":{"cost": 2440000,"name":"Rimac Nevera","emoji":":race_car:","single":True},
			"gef":{"cost": 1499,"name":"Nvidia GEFORCE RTX 3090","emoji":":desktop_computer:","single":True},
			"rov":{"cost": 2725000000,"name":"trip to Mars + rover/drone/skycrane package","emoji":":robot: :rocket:","single":True}
			}
		blacklist = {
			"xdg":True,
			"ltc":True,
			"eth":True,
			"xrp":True,
			"bch":True
			}

		if len(args) == 0:
			arg="noargs"
		else:
			arg = args[0].lower()

		if len(args) >= 2:
			arg = args[0].lower()
			arg2 = args[1].lower()
		else:
			arg2 = "noarg"

		if arg in blacklist:
			return

		if arg == "help":
			await ctx.channel.send("**Currency Eamples**: !p gbp, !p cad, !p xau")
			keys = ""
			for k in itemDic.keys():
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
			if itemDic[item]["single"] == False:
				if itemDic[item]["cost"] < float(price) and arg2=="sats":
					price = itemDic[item]["cost"]/float(price) * 100000000
				else:
					price = float(price)/itemDic[item]["cost"]
					if arg2 == "sats":
						price = price * 100000000

			else:
				price = itemDic[item]["cost"]/float(price)
				if arg2 == "sats":
					price = price * 100000000


		currencyStr = ""
		if arg in currencyFormatDic:
			currencyStr = currencyFormatDic[arg]
		elif isItem:
			if itemDic[item]["single"] == False:
				if arg2 == "sats":
					currencyStr = "**" + itemDic[item]["emoji"] + " 1 " + itemDic[item]["name"] + "**" + " costs **" + "{:,.0f}" + " Satoshis**"
				else:
					currencyStr = "**1 Bitcoin** is worth **" + itemDic[item]["emoji"] + " {:,.0f}" + " " + itemDic[item]["name"] + "**"
			else:
				if arg2 == "sats":
					currencyStr = "**" + itemDic[item]["emoji"] + " 1 " + itemDic[item]["name"] + "**" + " costs **" + "{:,.0f}" + " Satoshis**"
				else:
					currencyStr = "**" + itemDic[item]["emoji"] + " 1 " + itemDic[item]["name"] + "**" + " costs **" + "{:.2f}" + " Bitcoin**"
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

def setup(bot):
	bot.add_cog(General(bot))

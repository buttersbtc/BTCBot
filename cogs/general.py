from operator import truediv
import discord
from discord.ext import commands
import requests
import json
from random import randrange
import math
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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
			"beer":{"cost": 4.75,"name":"Pints of Beer","emoji":":beer:","single":False},
			"but":{"cost": .75,"name":"Sticks of Butter","emoji":":butter:","single":False},
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
			"bre":{"cost": 2.04,"name":"Loaves of bread","emoji":":bread:","single":False},

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
			"rov":{"cost": 2725000000,"name":"trip to Mars + rover/drone/skycrane package","emoji":":robot: :rocket:","single":True},
			"bez":{"cost": 74598,"name":"One minute of Jeff Bezos' time","emoji":":man_office_worker:","single":True},
			"kid":{"cost": 200000,"name":"black market kidney","emoji":":detective: :aubergine:","single":True},
			"ukb":{"cost": 850000000000,"name":"British banking bailout","emoji":":flag_gb: :bank:","single":True}
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

		if arg =="sats":
			await ctx.channel.send("**1 Bitcoin** is equal to **100,000,000 Satoshis**")
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
			api = "https://api.coincap.io/v2/assets/bitcoin"
			r = requests.get(api)
			data = json.loads(r.text)

			api_rates = "https://api.coincap.io/v2/rates/"
			r_rates = requests.get(api_rates)
			data_rates = json.loads(r_rates.text)

		except:
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
		else:
			if arg2 == "sats":
				price = 100000000/float(price)



		currencyStr = ""
		if arg in currencyFormatDic:
			if arg2 == "sats":
				currencyStr = "**1 " + arg.upper()  + "** is **" + "{:,.0f} Satoshis**"
			else:
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
					currencyStr = "**" + itemDic[item]["emoji"] + " 1 " + itemDic[item]["name"] + "**" + " costs **" + "{:,.2f}" + " Bitcoin**"
		else:
			if arg2 == "sats":
				currencyStr = "**1 " + arg.upper()  + "** is **" + "{:,.0f} Satoshis**"
			else:
				currencyStr = currencyFormatDic["default"] + arg.upper()

		
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
		
	# Fetches Bitcoin all time high (ATH) price
	@commands.command()
	async def ath(self, ctx):
		api = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin&order=market_cap_desc&per_page=100&page=1&sparkline=false"
		r = requests.get(api)
		data = json.loads(r.text)
		price = data[0]["ath"]
		message_string = "**Bitcoin ATH** is currently **${:,.2f}**".format(float(price))
		await ctx.send(message_string)

	# Fetches Bitcoin TX by hash
	@commands.command()
	async def tx(self, ctx, *args):
		api = "https://blockstream.info/api/tx/" + args[0]
		r = requests.get(api)
		try:
			data = json.loads(r.text)
		except:
			await ctx.send("Invalid argument, please provide a valid tx hash")
			return
		confirmed = "Unconfirmed"
		block = ""
		time = ""
		if data["status"]["confirmed"]:
			confirmed = "Confirmed"
			block = '{:,.0f}'.format(data["status"]["block_height"])
			time = datetime.datetime.utcfromtimestamp(data["status"]["block_time"]).strftime("%d/%m/%Y, %H:%M:%S") + " UTC"
		amount = 0
		for vout in data["vout"]:
			amount+=vout["value"]
		fee = data["fee"]
		size = data["weight"]/4
		feerate = fee/size
		feepercent = fee/amount*100
		inputs = len(data["vin"])
		outputs = len(data["vout"])

		

		message_string = '''```TX {txid}
{confirmed} {block} {time}
Sent {amount} sat for {fee} sat fee ({feerate} sat/vbtye, {feepercent}%)
{inputs} inputs, {outputs} outputs, {size} vbytes
```'''.format(txid=data["txid"], confirmed=confirmed, block=block, time=time, amount='{:,.0f}'.format(amount), fee='{:,.0f}'.format(fee), feerate='{:,.2f}'.format(feerate), feepercent='{:,.2f}'.format(feepercent), inputs=inputs, outputs=outputs, size='{:,.2f}'.format(size))
		await ctx.send(message_string)


	# Fetches Bitcoin address info
	@commands.command()
	async def address(self, ctx, *args):
		api = "https://blockstream.info/api/address/" + args[0]
		r = requests.get(api)
		try:
			data = json.loads(r.text)
		except:
			await ctx.send("Invalid argument, please provide a valid address")
			return
		balance = data["chain_stats"]["funded_txo_sum"] - data["chain_stats"]["spent_txo_sum"]
		mempoolAmt = data["mempool_stats"]["funded_txo_sum"] - data["mempool_stats"]["spent_txo_sum"]

		message_string = '''```Address {address}
Balance is {balance} sat
Received {receivedCount} TXO for {receivedAmt} sat
Sent {sentCount} TXO for {sentAmt} sat
{mempoolCount} TX in mempool for {mempoolAmt} sat
```'''.format(address=data["address"], balance='{:,.0f}'.format(balance), receivedCount='{:,.0f}'.format(data["chain_stats"]["funded_txo_count"]), receivedAmt='{:,.0f}'.format(data["chain_stats"]["funded_txo_sum"]), sentCount='{:,.0f}'.format(data["chain_stats"]["spent_txo_count"]), sentAmt='{:,.0f}'.format(data["chain_stats"]["spent_txo_sum"]), mempoolCount='{:,.0f}'.format(data["mempool_stats"]["tx_count"]), mempoolAmt='{:,.0f}'.format(mempoolAmt))
		await ctx.send(message_string)

	# Fetches Bitcoin mempool info from blockstreams mempool
	@commands.command()
	async def mempool(self, ctx, *args):
		api = "https://blockstream.info/api/mempool"
		r = requests.get(api)
		try:
			data = json.loads(r.text)
		except:
			await ctx.send("Unable to parse mempool data. Try again later.")
			return
		
		brackets = [[0, 1000000], [1000000, 4000000], [4000000, 12000000], [12000000, 36000000]]
		n=0
		pendingVsize = 0
		for entry in data["fee_histogram"]:
			if n > len(brackets) - 1:
				break
			fee = entry[0]
			vsize = entry[1]
			if len(brackets[n]) <= 2:
				brackets[n].append(fee)
			sizeRange = brackets[n][1] - brackets[n][0]
			if vsize + pendingVsize >= sizeRange:
				brackets[n].append(fee)
				brackets[n].append(vsize + pendingVsize)
				n+=1
				pendingVsize = vsize + pendingVsize - sizeRange
			else:
				pendingVsize+=vsize

			res = stats.cumfreq(data["fee_histogram"], numbins=4,
                    defaultreallimits=(1.5, 5))
			
		message_string = '''```Mempool has {count} TX and is {size} MB
Total fees in mempool are {fees} BTC
The tip of the mempool ({range01}MB) ranges between {range0bottomMB} sat/vbyte and {range0topMB} sat/vbyte
{range10}MB- {range11}MB = {range1bottomMB}-{range1topMB} sat/vbyte
{range20}MB- {range21}MB = {range2bottomMB}-{range2topMB} sat/vbyte
{range30}MB- {range31}MB  = {range3bottomMB}-{range3topMB} sat/vbyte
```'''.format(count='{:,.0f}'.format(data["count"]), size='{:,.2f}'.format(data["vsize"]/1000000), fees='{:,.2f}'.format(data["total_fee"]/100000000), 
			  range01='{:,.0f}'.format(brackets[0][1]/1000000), range0bottomMB='{:,.0f}'.format(brackets[0][3]), range0topMB='{:,.0f}'.format(brackets[0][2]), 
			  range10='{:,.0f}'.format(brackets[1][0]/1000000), range11='{:,.0f}'.format(brackets[1][1]/1000000), range1bottomMB='{:,.0f}'.format(brackets[1][3]), range1topMB='{:,.0f}'.format(brackets[1][2]),
			  range20='{:,.0f}'.format(brackets[2][0]/1000000), range21='{:,.0f}'.format(brackets[2][1]/1000000), range2bottomMB='{:,.0f}'.format(brackets[2][3]), range2topMB='{:,.0f}'.format(brackets[2][2]),
			  range30='{:,.0f}'.format(brackets[3][0]/1000000), range31='{:,.0f}'.format(brackets[3][1]/1000000), range3bottomMB='{:,.0f}'.format(brackets[3][3]), range3topMB='{:,.0f}'.format(brackets[3][2]))
		await ctx.send(message_string)


async def setup(bot):
	await bot.add_cog(General(bot))

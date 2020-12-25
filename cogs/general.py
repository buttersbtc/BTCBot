import discord
from discord.ext import commands
import requests
import json

class General(commands.Cog):
	"""General commands"""
	def __init__(self, bot):
		self.bot = bot

	async def on_ready(self):
		print("General commands loaded")


	# Fetch Bitcoin price
	@commands.command()
	async def btc(self, ctx):
		api = "http://preev.com/pulse/units:btc+usd/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		price = round(float(price),2)
		price = "${:,.2f} USD".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"		
		await ctx.send(message_string)
	
	# price also fetches USD
	@commands.command()
	async def price(self, ctx, arg="noargs"):
		api = "http://preev.com/pulse/units:btc+usd/sources:bitstamp+kraken"
		arg = arg.lower()
		func = getattr(self, arg , None)
		if(callable(func)):
			await func(ctx)
			return

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		price = round(float(price),2)
		price = "${:,.2f} USD".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"		
		await ctx.send(message_string)

	# usd fetches USD
	@commands.command()
	async def usd(self, ctx):
		api = "http://preev.com/pulse/units:btc+usd/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		price = round(float(price),2)
		price = "${:,.2f} USD".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"		
		await ctx.send(message_string)
		
	# Fetches price in CAD
	@commands.command()
	async def cad(self, ctx):
		api = "http://preev.com/pulse/units:btc+cad/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["cad"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price),2)
		price = "${:,.2f} CAD".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)	

	# Fetches price in GBP
	@commands.command()
	async def gbp(self, ctx):
		api = "http://preev.com/pulse/units:btc+gbp/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["gbp"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price),2)
		price = "£{:,.2f} GBP".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)	

	# Fetches price in EUR
	@commands.command()
	async def eur(self, ctx):
		api = "http://preev.com/pulse/units:btc+eur/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["eur"]["kraken"]["last"]
		price = round(float(price),2)
		price = "€{:,.2f} EUR".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)
		
	# Fetches price in BRL
	@commands.command()
	async def brl(self, ctx):
		api = "http://preev.com/pulse/units:btc+brl/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["brl"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price),2)
		price = "R${:,.2f} BRL".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)	

	# Fetches price in VEF
	@commands.command()
	async def vef(self, ctx):
		api = "http://preev.com/pulse/units:btc+vef/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["vef"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price))
		price = "B${:,.0f} Venezuelan bolívar".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)	

#Proposed change (add support for missing from top 10 most used currencies) begin
	# Fetches price in JPY
	@commands.command()
	async def jpy(self, ctx):
		api = "http://preev.com/pulse/units:btc+jpy/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["jpy"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price))
		price = "¥{:,.0f} JPY".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)	

	# Fetches price in AUD
	@commands.command()
	async def aud(self, ctx):
		api = "http://preev.com/pulse/units:btc+aud/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["aud"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price))
		price = "${:,.2f} Brass Razoos".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)

	# Fetches price in CHF
	@commands.command()
	async def chf(self, ctx):
		api = "http://preev.com/pulse/units:btc+chf/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["chf"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price))
		price = "{:,.2f} CHF".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)

	# Fetches price in CNY
	@commands.command()
	async def cny(self, ctx):
		api = "http://preev.com/pulse/units:btc+cny/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["cny"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price))
		price = "¥{:,.0f} CNY".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)

	# Fetches price in HKD
	@commands.command()
	async def hkd(self, ctx):
		api = "http://preev.com/pulse/units:btc+hkd/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["hkd"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price))
		price = "${:,.2f} HKD".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)

	# Fetches price in NZD
	@commands.command()
	async def nzd(self, ctx):
		api = "http://preev.com/pulse/units:btc+nzd/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["nzd"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price))
		price = "${:,.2f} NZD".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)

	# Fetches price in ILS
	@commands.command()
	async def ils(self, ctx):
		api = "http://preev.com/pulse/units:btc+jpy/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		conversion = data["ils"]["usd"]["other"]["last"]
		price = float(price)/float(conversion)
		price = round(float(price))
		price = "₪{:,.0f} Shekels".format(float(price))
		message_string = "**1 Bitcoin** is worth **" + price + "**"
		await ctx.send(message_string)	
# END proposed change

	# Fetches price in BigMacs
	@commands.command()
	async def mac(self, ctx):
		api = "http://preev.com/pulse/units:btc+usd/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		price = round(float(price)/5.71)
		price = ":hamburger: {:,} Big Macs".format(price)
		message_string = "**1 Bitcoin** is worth **" + price + "**"	
		await ctx.send(message_string)	

	# Fetches price in McRibs
	@commands.command()
	async def mcr(self, ctx):
		api = "http://preev.com/pulse/units:btc+usd/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		price = round(float(price)/4.29)
		price = ":pig2: {:,} McRibs".format(price)
		message_string = "**1 Bitcoin** is worth **" + price + "**"	
		await ctx.send(message_string)	

	# Fetches price in Crunchwraps
	@commands.command()
	async def cru(self, ctx):
		api = "http://preev.com/pulse/units:btc+usd/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		price = round(float(price)/2.99)
		price = ":taco: {:,} Crunchwraps Supreme".format(price)
		message_string = "**1 Bitcoin** is worth **" + price + "**"	
		await ctx.send(message_string)	
	
	# Fetches price in Sticks of Butter
	@commands.command()
	async def but(self, ctx):
		api = "http://preev.com/pulse/units:btc+usd/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		price = round(float(price)/.5)
		price = ":butter: {:,} Sticks of Butter".format(price)
		message_string = "**1 Bitcoin** is worth **" + price + "**"	
		await ctx.send(message_string)	

	# Fetches price in Lambos
	@commands.command()
	async def lam(self, ctx):
		api = "http://preev.com/pulse/units:btc+usd/sources:bitstamp+kraken"

		r = requests.get(api)
		data = json.loads(r.text)

		price = data["btc"]["usd"]["bitstamp"]["last"]
		price = round(521465/float(price),8)
		price = "{:,}".format(price)
		message_string = "**:race_car: 1 Lamborghini Aventador SVJ** costs **" + price + " BTC**"		
		await ctx.send(message_string)

def setup(bot):
	bot.add_cog(General(bot))

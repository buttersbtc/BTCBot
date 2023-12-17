import BitcoinAPI as api
from constants import ITEM_DICT, CURRENCY_FORMAT_DICT, BLACKLIST
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

	async def on_ready(self):
		print("General commands loaded")

	# Price - All currencies enabled by the APi are automatically supported. Add a currency formatting string to change the way a given currency is displayed
	#To add a new item to the price call make a new entry in the itemDic with the cost and formatStr, the key being the string  used to call that item
	@commands.command()
	async def price(self, ctx, *args):
		if len(args) == 0:
			arg = "usd"
		else:
			arg = args[0]

		arg = arg.lower()

		if arg == "help":
			await ctx.channel.send("**Currency Eamples**: !p gbp, !p cad, !p xau")
			keys = ""
			for k in ITEM_DICT.keys():
				keys += k + ", "
			keys = keys[0:len(keys)-2]
			await ctx.channel.send("**Other Supported Items**: " + keys)
			await ctx.channel.send("**!p <item> sats** will give you the cost of the item in satoshis")
			return
		if arg in ITEM_DICT:
			await self.price_item(ctx, arg)
			return
		if arg == "sats":
			await self.price_sats(ctx, arg)
			return
		await self.price_currency(ctx, arg)

	async def price_sats(self, ctx, *args):
		await ctx.channel.send("**1 Bitcoin** is equal to **100,000,000 Satoshis**")

	async def price_currency(self, ctx, currency):
		price, error = api.get_current_price()
		if error:
			await ctx.channel.send("Price API is currently slow to respond. Try again later.")
			return
		price, _, error = api.get_current_price_in_currency(currency)
		if error:
			await ctx.channel.send("Unable to find currency code: " + currency)
			return
		index = "default"
		prefix = "**1 Bitcoin** is worth "
		suffix = " " + currency.upper()
		if currency in CURRENCY_FORMAT_DICT:
			index = currency
			suffix = ""
		price = prefix + "**" + CURRENCY_FORMAT_DICT[index].format(price) + suffix +"**"
		await ctx.channel.send(price)

	async def price_item(self, ctx, item):
		if not item in ITEM_DICT:
			await ctx.channel.send("Item not supported")
			return
		price, error = api.get_current_price()
		if error:
			await ctx.channel.send("Price API is currently slow to respond. Try again later.")
			return
		item_map = ITEM_DICT[item]
		emoji = item_map["emoji"]
		name = item_map["name"]
		if item_map["single"]:
			price = item_map["cost"] / price
			await ctx.channel.send(f"{emoji} {name} costs {price:,.2f} Bitcoin")
		else:
			price = price / ITEM_DICT[item]["cost"]
			await ctx.channel.send(f"**1 Bitcoin*** is worth **{emoji} {price:,.2f} {name}**")
			return

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
		fun_facts = ["**Fun Fact:** Bitcoin is the first and only decentralized digital currency",
					"**Fun Fact:** Bitcoin was created by Satoshi Nakamoto in 2009",
					"**Fun Fact:** Bitcoin is not a cryptocurrency, it predates them and the term only exists to create a false association to Bitcoin",
					"**Fun Fact:** Blockchain technology is neither novel nor valuable. It has none of the properties commonly ascribed to it like immutability, or decentralization, or security. This comes instead from other properties unique to Bitcoin, such as true Nakamoto consensus.",
					"**Fun Fact:** Proof of work is where Bitcoin's cost to attack and economic mutability come from.",
					"**Fun Fact:** Bitcoin's distributed ledger, the blockchain, is simply where we store the data for Bitcoin network state. It has no other valuable function or properties.",
					"**Fun Fact:** Bitcoin's peer-to-peer (p2p) network is where most of the valuable properties associated with Bitcoin emerge from, specifically the behaviour of the network actors verifying all transactions and acting in a self interested manner.",
					"**Fun Fact:** Bitcoin has a super-majority of all SHA-256 computing in the world, and without that super-majority it would be vulnerable to attacks.",
					"**Fun Fact:** The smallest unit of Bitcoin is called a Satoshi, worth one hundred millionth of a single Bitcoin.",
					"**Fun Fact:** In 2021, El Salvador became the first country to adopt Bitcoin as legal tender.",
					"**Fun Fact:** At one point, the FBI was one of the world’s largest owners of Bitcoin, due to seizures from the Silk Road, an online black market.",
					"**Fun Fact:** The world's first Bitcoin ATM was installed in Vancouver, Canada, in 2013.",
					"**Fun Fact:** The first Bitcoin transaction was made by Satoshi Nakamoto to Hal Finney in 2009.",
					"**Fun Fact:** It’s estimated that around 20% of all Bitcoins are lost or inaccessible, mainly due to forgotten passwords or broken hard drives.",
					"**Fun Fact:** The first real-world transaction using Bitcoin was in 2010, when a programmer named Laszlo Hanyecz bought two pizzas for 10,000 Bitcoins. Just 3 years later, in October of 2013, those Bitcoins could have bought him over 100,000 pizzas.",
					"**Fun Fact:** In 2010, a vulnerability in the Bitcoin protocol was exploited, creating billions of Bitcoins. The bug was quickly fixed, and the extra Bitcoins were erased. This is the only time a 'free Bitcoin' bug was exploited on the network.",
					"**Fun Fact:** Bitcoin is the only decentralized entity in the 'crypto' space and 'cryptocurrency' is generally a by-word for scams.",
					"**Fun Fact:** Bitcoin operates on a decentralized network, meaning it isn’t controlled by any single entity or government.",
					"**Fun Fact:** Bitcoins are created through a process called mining, which involves using electricity to run many special computers called ASICs. These are used to search for the correct random number that entitles them to mint new bitcoins, publish bitcoin transactions, and take their fees. The more powerful ASICs you have, the more likely you are to gain this privilege at any given time. Because ASICs are distributed all around the world and owned by many different entities, Bitcoin is safe from attack.",
					"**Fun Fact:** Approximately every four years, the reward for Bitcoin mining halves, an event known as 'halving.' This reduces the rate at which new Bitcoins are created.",
					"**Fun Fact:** There will only ever be 21 million Bitcoins in existence, making it a deflationary currency once it is all printed or the loss rate is greater than the printed rate. Until then it is inflationary. As of this writing 95% of all Bitcoin have been mined.",
					"**Fun Fact:** Public spaces like r/bitcoin, twitter, and telegram are full of misinformation. Each of us can make our communities better places by verifying the information we see and refuting misinformation. Though if you do, expect to be banned from those spaces. Entrenched interests stand against Bitcoin as do petty egos.",
					"**Fun Fact:** Bitcoin is for enemies. It doesn't care about you, your ideology, or your grudges. It caters to your political opponents, it caters to those you believe to be unethical. If it did any less, then it would be subject to the whims of popular culture and tyranny of the majority. Bitcoin is a tool and it can be used for many ends, even those you may disagree with.",
					"**Fun Fact:** When Bitcoin is attacked it relies on the decentralized-economic security model. What this means is that those misusing blockspace will pay for it as a function of time, bankrupting them. Failing that, nodes have the power to fork and defend themselves. These are the economic and decentralized foundations of Bitcoin's security model, so run a node!",
					"**Fun Fact:** Bitcoin is thankless. It owes you nothing, so expect nothing. Your node and your will defines Bitcoin, so use it and stand for yourself.",
					"**Fun Fact:** Bitcoin addresses are most commonly the hash of 'smart contracts' and the process of spending enables verification of their execution.",
					"**Fun Fact:** A scam built on Bitcoin is a still a scam, is still fraud, is still worthless. NFT's, ordinals, shitcoin emulating layers, federations, stablecoins, and others fall into this category.",
					"**Fun Fact:** Custodying your own Bitcoin isn't difficult. If you don't, please do. Download a wallet, create some keys offline in an air gapped environment, ideally provide your own entropy with dice or corrected coin flips, and backup your seed in metal. These simple steps make you more secure than LukeJr.",
					"**Fun Fact:** The speaker doesn't matter, the message matters. Evaluate and verify the things you're told in Bitcoin and this discord. Trust no one and verify everything.",
					"**Fun Fact:** Bitcoin hasn't slept since 2013 when it took a 6 hour nap to reorg. I don't think I've slept since then either, come to mention it.",
					"**Fun Fact:** In 2018 a [vulnerability was discovered](https://bitcoincore.org/en/2018/09/20/notice/), originally introduced in 2017, which enabled DoS attacks against nodes as well as inflation of the Bitcoin supply. This was all BlueMatts fault. The issue was patched and deployed before being exploited, but stands to remind us that we must peer review code and run diverse node clients.",
					"**Fun Fact:** Between 2015 and 2017 the community engaged in what has become known as the Blocksize Wars, wherein over 80% of the traditionally powerful actors of any ecosystem - the rich, the businesses, and in our case the miners as well - attempted to change Bitcoin's consensus to reduce their technical costs at the expense of node runners. A minority of node runners threatening a user activated soft fork effectively stopped the attack by holding an economic gun to the businesses heads.",
					"**Fun Fact:** There are no shortcuts to verification or security.",
					"**Fun Fact:** Those obsessed with the Bitcoin price would (and have tried to) destroy its valuable properties such as decentralization (ability to run a node) and economic security (cost to transact) because they are too short sighted to care about Bitcoin, they only care about fiat.",
					"**Not Fun Fact:** People end their life every cycle by failing to plan for the turmoil of shitcoins crashing and middlemen collapsing, entire lives and families have been ruined. Don't be one of them. Don't borrow, don't over leverage, don't shitcoin, and don't use middlemen. Bitcoin fixes this.",
					"**Fun Fact:** There is no free Bitcoin. There is only spam and scams.",
					"**Fun Fact:** Bitcoin artists like tip_nz, BWA, ZhouTonged, and many others bring Bitcoin education to music, check them out.",
					"**Fun Fact:** Bitcoin is one of the greenest industries on the planet, especially of its size, with around half of all energy coming from renewables and subsidizing renewable energy sources. Other energy consumed includes curtailment - i.e. power that would otherwise be lost to ground - and displacing natural gas vents and flares thus displacing pollution. Bitcoin also uses significantly less energy than the traditional banking sector.",
					"**Fun Fact:** Half of Bitcoiners identify as left leaning, while the other half identify as right leaning. Bitcoin is for everyone who chooses to verify. Because of its unique properties, it is protected and removed from ideology.",
					"**Fun Fact:** Bitcoin saves lives in conflicts, enabling the escape of abuse and allowing would-be conscripts an opportunity to escape through unconfiscatable money and bribery.",
					"**Fun Fact:** If every would-be victim of abuse held Bitcoin they would have more options to escape that abuse. Bitcoin is a liberator.",
					"**Fun Fact:** Lots of people in the Bitcoin space have no idea what they are talking about, often and especially veterans and influencers.",
					"**Fun Fact:** Michael Saylor told noobies to buy the top with debt and remortgage their homes, says Bitcoin isn't a currency, spreads environmental FUD, and attempts to coordinate large groups of miners. If you listen to him you're as big of a fool as he is.",
					"**Fun Fact:** Andreas Antonopoulos is a scamming shitcoiner who spreads FUD and misinformation out of both ignorance and a desire to lead his followers.",
					"**Fun Fact:** Bitcoin Magazine is actually all about shitcoins, NFT's and scams. They even make and sell their own. They were founded by one of the most prolific shitcoiners in history as well.",
					"**Fun Fact:** Middlemen want to capture you and your business, but Bitcoin means you don't need them. So stop enabling middlemen, especially custodians. Opt for low trust businesses that leverage Bitcoin's innate features to keep your coins in your possession."
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
	async def help(self, ctx, *args):
		message_string = "Commands this bot accepts:"
		sorted_cmd = sorted(self.bot.commands, key=lambda cmd: cmd.name)
		for cmd in sorted_cmd:
			message_string +=  " " + os.getenv('BOT_PREFIX') + f"{cmd},"
		message_string = message_string[:len(message_string)-1]
		message_string += ". For bot support inquire at <http://bitcointech.help> or in the issues at <https://github.com/buttersbtc/BTCBot/issues>"
		await ctx.send(message_string)

async def setup(bot):
	await bot.add_cog(General(bot))

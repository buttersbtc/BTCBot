import re
import discord
from discord.ext import commands
import requests
import json
import datetime
import os
from dotenv import load_dotenv
from captcha.image import ImageCaptcha
import math
import hashlib
import datetime
from decimal import Decimal
import time
import ipc

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def report(self, ctx):
		load_dotenv()
		if os.getenv('ENABLE_REPORTS') == "1":
			reportChannel = os.getenv('REPORT_CHANNEL')
			for guild in self.bot.guilds:
				for channel in guild.channels:
					if channel.name == reportChannel:
						msg = ctx.author.mention + " reporting: " + ctx.message.content.replace("!report ", "")
						if ctx.message.reference is not None:
							reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
							msg += " - " + reply.author.mention + ": " + reply.content + " - " + reply.jump_url
						await channel.send(msg)

			await ctx.message.delete()


	@commands.command()
	async def newuser(self, ctx):
		if ctx.message.reference is not None:
			reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
			user = ", " + reply.author.mention
		else:
			user = ""
		await ctx.channel.send("Welcome to our community Bitcoin chat" + user + "! Please review the #rules while you're here; primarily no altcoin, stock, or off topic discussion. If you’re new to bitcoin, please check out https://lopp.net/bitcoin.html, a community curated list of educational resources, tools, and information.")

	@commands.command()
	async def exchanges(self, ctx, *args):
		exchangeDic = {
			"p2p": "Bisq, robosats, HodlHodl",
			"bahrain": "Rain",
			"indonesia":"Indodax",
			"israel": "Bits of Gold",
			"japan": "Bitbank, BitFlyer ,BtcBox",
			"kuwait": "Rain",
			"malaysia": "Luno",
			"oman": "Rain",
			"singapore": "Binance, Mine Digital",
			"south korea":"Bithumb , Coinone, Korbit",
			"saudi arabia":"Rain",
			"taiwan": "MaiCoin MAX, BitoPro",
			"turkey": "Koinim",
			"uae": "BitOasis, Karsha, Rain",
			"europe": "Relai",
			"netherlands": "Bitvavo",
			"poland": "BitBay",
			"ukraine": "Kuna",
			"uk": "Bitstamp, Coinbase, Gemini, Kraken, OKCoin, Binance, Bittylicious, CoinCorner, Coinfloor, CoinJar, Relai",
			"nigeria": "Luno, BuyCoins",
			"south africa": "Luno",
			"uganda": "Binance",
			"canada": "BullBitcoin, BitcoinWell",
			"mexico": "Bitso, Volabit",
			"usa": "River Financial, CashApp, Strike",
			"argentina": "ArgenBTC, SatoshiTango",
			"brazil": "Brasil Bitcoin, Mercado Bitcoin, NovaDAX, Walltime",
			"chile": "Buda",
			"colombia": "Buda",
			"peru": "Buda",
			"venezuela": "Bisq, Cryptobuyer",
			"australia": "Bitaroo, BTC Markets, CoinJar, CoinSpot, Digital Surge, CoinTree, HardBlock, Independent Reserve, Mine Digital, Swyftx",
			"new zealand": "Independent Reserve, Kiwi-coin, Mine Digital"
			}
		arg = ""
		for a in args[0]:
			arg += str(a) + " "
		arg = arg[0:len(arg)-1]
		if arg.lower() in exchangeDic:
			send = "Exchanges in " + arg + ": " + exchangeDic[arg.lower()]
			if (arg.lower() != "p2p"):
				send += ". When using custodial exchanges, be sure to withdraw your coins to your own wallet after buying! P2P is highly recommended over centralized exchanges."
			await ctx.channel.send(send)
		else:
			keys = ""
			for k in exchangeDic.keys():
				keys += k + ", "
			keys = keys[0:len(keys)-2]
			await ctx.channel.send("Available options: " + keys)

	@commands.command()
	async def exchange(self, ctx, *args):
		await Utilities(self).exchanges(self, ctx, args)

	@commands.command()
	async def ex(self, ctx, *args):
		await Utilities(self).exchanges(self, ctx, args)

	@commands.command()
	async def x(self, ctx, *args):
		await Utilities(self).exchanges(self, ctx, args)

	@commands.command()
	async def wallets(self, ctx, *args):
		walletDic = {
			"electrum": {"tags": ["pc", "windows", "linux", "mac", "android", "hot", "airgap", "psbt", "timelocks", "recommended", "multisig", "advanced", "lightning", "2fa", "node-compatible", "spv"], "link":"https://electrum.org/"},
			"sparrow": {"tags": ["pc", "windows", "linux", "mac", "hot", "advanced", "multisig", "node-compatible", "recommended"], "link":"https://sparrowwallet.com/"},
			"core": {"tags": ["pc", "windows", "linux", "hot", "node", "full-node", "advanced", "recommended"], "link":"https://bitcoincore.org/"},
			"knots": {"tags": ["pc", "windows", "linux", "hot", "node", "full-node", "advanced", "recommended"], "link":"https://bitcoinknots.org/"},
			"joinmarket": {"tags": ["pc", "windows", "hot", "privacy", "coinjoin", "recommended"], "link":"https://www.keepitsimplebitcoin.com/joinmarket/"},
			"coldcard": {"tags": ["hardware", "cold", "requires-wallet", "multisig", "node-compatible", "psbt", "airgap", "recommended"], "link":"https://coldcardwallet.com/"},
			"green": {"tags": ["android", "ios", "2fa", "pc", "windows", "linux", "mac", "multisig", "hot", "spv"], "link":"https://blockstream.com/green/"},
			"phoenix": {"tags": ["android", "hot", "lightning", "easy"], "link":"https://phoenix.acinq.co/"},
			"lnd": {"tags": ["pc", "windows", "linux", "mac", "hot", "node", "lightning", "lightning-node", "node-compatible", "advanced"], "link":"https://github.com/lightningnetwork/lnd/releases"},
			"c-lightning": {"tags": ["pc", "windows", "linux", "mac", "hot", "node", "lightning", "lightning-node", "node-compatible", "advanced"], "link":"https://github.com/ElementsProject/lightning/releases"},
			"blue": {"tags": ["android", "ios", "hot", "lightning", "self-custody", "node-compatible", "lightning-node-required"], "link":"https://bluewallet.io/"},
			"mycelium": {"tags": ["android", "ios", "hot", "local-trader"], "link":"https://wallet.mycelium.com/"},
			"seedsigner": {"tags": ["hardware", "airgap", "diy", "cold", "recommended"], "link":"https://seedsigner.com/"},
			"yeticold": {"tags": ["hardware", "airgap", "diy", "cold", "recommended"], "link":"https://yeticold.com/"},
            		"glacier-protocol": {"tags": ["hardware", "airgap", "diy", "cold"], "link":"https://glacierprotocol.org/"},
            		"Krux": {"tags": ["hardware", "airgap", "diy", "cold"], "link":"https://selfcustody.github.io/krux/"},
			"breez": {"tags": ["android", "ios", "hot", "lightning", "easy"], "link":"https://breez.technology/"},
			"wallet-of-satoshi": {"tags": ["android", "ios", "hot", "lightning", "partial-custody", "easy"], "link":"https://www.walletofsatoshi.com/"},
			"liana": {"tags": ["pc", "mac", "windows", "linux", "hot", "timelocks", "multisig", "cold", "easy", "advanced"], "link":"https://wizardsardine.com/liana/"},
			"rtl": {"tags": ["pc", "mac", "windows", "linux", "web", "self-hosted", "hot", "lightning-node-required", "advanced"], "link":"https://github.com/Ride-The-Lightning/RTL"},
                        "blixt": {"tags": ["android", "hot", "lightning", "advanced"], "link":"https://blixtwallet.github.io"},
			}
		resp = " \n"
		for wallet in walletDic:
			if args[0][0].lower() == wallet:
				await ctx.channel.send(wallet[0].upper() + wallet[1:len(wallet)] + ": " + walletDic[wallet]["link"] + " tags: " + ", ".join(walletDic[wallet]["tags"]))
				return
			overlap = list(set(walletDic[wallet]["tags"]) & set(args[0]))
			if len(overlap) == len(args[0]):
				resp += wallet[0].upper() + wallet[1:len(wallet)] + ": <" + walletDic[wallet]["link"] + "> tags: " + ", ".join(walletDic[wallet]["tags"]) + "\n"

		await ctx.channel.send(resp)

	@commands.command()
	async def wallet(self, ctx, *args):
		await Utilities(self).wallets(self, ctx, args)

	@commands.command()
	async def w(self, ctx, *args):
		await Utilities(self).wallets(self, ctx, args)

	@commands.command()
	async def dev(self, ctx, *args):
		msg = "\n<https://github.com/bitcoin/bitcoin> <- the repo\n<https://web.libera.chat/#bitcoin-core-dev> <- the irc\n<https://github.com/bitcoin-core/bitcoin-devwiki/wiki/General-IRC-meeting> <- the dev meetings\n<https://bitcoincore.reviews/> the PR review club meetings\n<https://bitcoin.stackexchange.com> <- the stack exchange\n<https://lists.linuxfoundation.org/pipermail/bitcoin-dev/> <- the general dev mailinglist\n<https://lists.linuxfoundation.org/pipermail/bitcoin-core-dev/> <- core dev mailinglist\n<https://bitcoinops.org/en/newsletters/> <- optech newsletters dev summary\n<https://bitcoincoreslack.herokuapp.com/> <- core slack\n<https://delvingbitcoin.org/> <- technical discussion community\n<https://bitcoin.design/guide/> <- the development design guide\n<https://www.bitcointech.wiki/editor> <- the online transaction editor\n<https://bitcoincore.academy/> <- Bitcoin Core Onboarding\n<https://github.com/bitcoin/bips> <- Bitcoin Improvement Proposals"
		await ctx.channel.send(msg)

	@commands.command()
	async def job(self, ctx, *args):
		msg = "Bitcoin job boards and resources:\n<https://cash.app/careers>\n<https://reddit.com/r/Jobs4Bitcoins>\n<https://strike.me/jobs>\n<https://www.bitmex.com/careers>\n<https://angel.co/company/river-financial/jobs>\n<https://bitcoinerjobs.co/>"
		await ctx.channel.send(msg)

	@commands.command()
	async def jobs(self, ctx, *args):
		await Utilities(self).job(self, ctx, args)

	@commands.command()
	async def quantum(self, ctx, *args):
		msg = "A general purpose and stable high qubit quantum computer (which doesn't exist and no one is sure if will ever exist) can run an algorithm called shor's. Shor's is used to factor numbers.  You can thus use shor's to derive a private key from a public key. Bitcoin exposes public keys in the scenarios of certain address reuse and when certain transactions are sitting in the mempool, as well as very old 2009 era pay to pubkey coinbases and new taproot transactions. What will happen if such a computer ever exists is slowly attempts to mine the most static of these coins, probably the old coinbases, will occur. Once this happens everyone will know there is a quantum actor and avoid address reuse or in the worst case just move to a new address format. It's also important to remember that a quantum attack takes considerable time, not dissimilar to mining, as it's the process for searching for a private key. Another Algorithm, called grovers, will enable a new kind of mining ASIC, similar to how generations of PoW devices have always functioned."
		await ctx.channel.send(msg)

	@commands.command()
	async def ban(self, ctx, *args):
		if hasattr(ctx.message.author, 'roles') and any(role.name == os.getenv('MOD_ROLE') for role in ctx.message.author.roles):
			n=0
			for user in ctx.message.mentions:
				if hasattr(user, 'roles') and any(role.name == os.getenv('MOD_ROLE') for role in user.roles):
					await ctx.channel.send("Can't ban mods")
				else:
					await user.ban()
					n = n+1
			for arg in args:
				userMention = re.search("([0-9]*)",arg)
				if userMention:
					user = await self.bot.fetch_user(int(arg))
					if hasattr(user, 'roles') and any(role.name == os.getenv('MOD_ROLE') for role in user.roles):
						await ctx.channel.send("Can't ban mods")
					elif user != None:
						await ctx.guild.ban(user)
						n = n+1
			await ctx.channel.send(str(n) + " users banned")

		else:
			await ctx.channel.send("No permission.")

	@commands.command()
	async def banafter(self, ctx, *args):
		if hasattr(ctx.message.author, 'roles') and any(role.name == os.getenv('MOD_ROLE') for role in ctx.message.author.roles):
			n=0
			start = (await ctx.fetch_message(args[0])).created_at
			end = datetime.datetime.now(tz=None) if len(args) < 2 else (await ctx.fetch_message(args[1])).created_at
			for message in await ctx.message.channel.history(after=start, before=end).flatten():
				if hasattr(message.author, 'roles') and any(role.name == os.getenv('MOD_ROLE') for role in message.author.roles):
					await ctx.channel.send("Can't ban mods")
				else:
					await ctx.guild.ban(message.author)
					n = n+1
			await ctx.channel.send(str(n) + " users banned")
		else:
			await ctx.channel.send("No permission.")

	@commands.command()
	async def captcha(self, ctx, *args):
		if os.getenv('ENABLE_ANTI_BOT') == "1":
			member = ctx.message.author
			await member.send("Please complete the following captcha:")
			image = ImageCaptcha()
			data = image.generate(str(hashlib.sha256(str(round(math.sqrt(int(member.id)/int(os.getenv('SALT1')) + int(os.getenv('SALT2'))))).encode("utf-8")).hexdigest())[:8].upper())
			await member.send(file=discord.File(data, 'captcha.png'))

	@commands.command()
	async def modmail(self, ctx, *args):
		if os.getenv('ENABLE_MODMAIL') == "1" and os.getenv('MODMAIL_CHANNEL') != None and len(args) > 1:
			for guild in self.bot.guilds:
				for channel in guild.channels:
					if channel.name == os.getenv('MODMAIL_CHANNEL'):
						msg = "Dear benevolant and respected moderators,\n```" + ctx.message.content.replace(os.getenv('BOT_PREFIX') + "modmail ", "") +"```\nLove, " + ctx.message.author.mention
						await channel.send(msg)
			await ctx.message.delete()
		if len(args) <= 1:
			await channel.send("Please include a message with your modmail. ex. `!modmail You moderators are the worst. I hope you fall down the stairs and break your legs, and your stairs.`")

	@commands.command()
	async def tools(self, ctx, *args):
		msg = '''
<https://www.bitcointech.wiki/editor> <- Transaction Editor
<https://bitcoinsearch.xyz/> <- Bitcoin Technical Search
<https://btcpayserver.org/> <- Bitcoin Point of Sale Software
<https://bisq.network/> <- P2P Trading Software
<https://wizardsardine.com/liana/> <- Liana Simple Inhereitance and Multisig Wallet
<https://github.com/JoinMarket-Org/joinmarket-clientserver> <- Joinmarket Coinjoins
<https://github.com/lightninglabs/pool> <- Lightning Pool Low Trust Liquidity Marketplace
<https://blockstream.com/satellite-api/> <- Blockstream Satellite Bitcoin Accessibility
<https://github.com/Blockstream/esplora/tree/master> <- Self Hosted Block Explorer
<https://blockstream.info/> <- Block Explorer
<https://github.com/jhoenicke/mempool> <- Self Hosted Mempool Statistics
<https://jochen-hoenicke.de/queue/#BTC,24h,weight> <- Mempool Statistics
<https://blockstream.info/tx/push> <- Broadcast a TX
<https://1ml.com/> <- Lightning Explorer
<https://github.com/BoltzExchange/boltz-lnd> <- Atomic Swaps for LND
<https://github.com/lightningd/plugins> <- Plugins for C-Lightning
		'''
		await ctx.channel.send(msg)

	# Fetches Bitcoin TX by hash
	@commands.command()
	async def tx(self, ctx, *args):
		if len(args) != 1:
			await ctx.send("The tx command requires a tx hash following it.")
			return
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

		message_string = '''View in [bitcointech.wiki/editor](<https://bitcointech.wiki/editor?d={txid}>)```TX {txid}
{confirmed} {block} {time}
Sent {amount} sat for {fee} sat fee ({feerate} sat/vbtye, {feepercent}%)
{inputs} inputs, {outputs} outputs, {size} vbytes
```'''.format(txid=data["txid"], confirmed=confirmed, block=block, time=time, amount='{:,.0f}'.format(amount), fee='{:,.0f}'.format(fee), feerate='{:,.2f}'.format(feerate), feepercent='{:,.2f}'.format(feepercent), inputs=inputs, outputs=outputs, size='{:,.2f}'.format(size))
		await ctx.send(message_string)

	# Fetches Bitcoin address info
	@commands.command()
	async def address(self, ctx, *args):
		if len(args) != 1:
			await ctx.send("The address command requires an address following it.")
			return

		api = "https://blockstream.info/api/address/" + args[0]
		r = requests.get(api)
		try:
			data = json.loads(r.text)
		except:
			await ctx.send("Invalid argument, please provide a valid address")
			return
		balance = data["chain_stats"]["funded_txo_sum"] - data["chain_stats"]["spent_txo_sum"]
		mempoolAmt = data["mempool_stats"]["funded_txo_sum"] - data["mempool_stats"]["spent_txo_sum"]

		message_string = '''View in [bitcointech.wiki/editor](<https://bitcointech.wiki/editor?d={address}>)```Address {address}
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

		for bracket in brackets:
			if len(bracket) == 2:
				bracket.append(0)
			if len(bracket) == 3:
				bracket.append(0)

		message_string = '''```Blockstream's mempool has {count} TX and is {size} MB
Total fees in mempool are {fees} BTC
The tip of the mempool ({range01}MB) ranges between {range0bottomMB} sat/vbyte and {range0topMB} sat/vbyte
{range10}MB - {range11}MB = {range1bottomMB}-{range1topMB} sat/vbyte
{range20}MB - {range21}MB = {range2bottomMB}-{range2topMB} sat/vbyte
{range30}MB - {range31}MB  = {range3bottomMB}-{range3topMB} sat/vbyte
```'''.format(count='{:,.0f}'.format(data["count"]), size='{:,.2f}'.format(data["vsize"]/1000000), fees='{:,.2f}'.format(data["total_fee"]/100000000),
			  range01='{:,.0f}'.format(brackets[0][1]/1000000), range0bottomMB='{:,.0f}'.format(brackets[0][3]), range0topMB='{:,.0f}'.format(brackets[0][2]),
			  range10='{:,.0f}'.format(brackets[1][0]/1000000), range11='{:,.0f}'.format(brackets[1][1]/1000000), range1bottomMB='{:,.0f}'.format(brackets[1][3]), range1topMB='{:,.0f}'.format(brackets[1][2]),
			  range20='{:,.0f}'.format(brackets[2][0]/1000000), range21='{:,.0f}'.format(brackets[2][1]/1000000), range2bottomMB='{:,.0f}'.format(brackets[2][3]), range2topMB='{:,.0f}'.format(brackets[2][2]),
			  range30='{:,.0f}'.format(brackets[3][0]/1000000), range31='{:,.0f}'.format(brackets[3][1]/1000000), range3bottomMB='{:,.0f}'.format(brackets[3][3]), range3topMB='{:,.0f}'.format(brackets[3][2]))
		await ctx.send(message_string)

	# Fetches Bitcoin tip height
	@commands.command()
	async def height(self, ctx, *args):
		api = "https://blockstream.info/api/blocks/tip/height"
		r = requests.get(api)
		height = r.text
		message_string = "The current block height is " + r.text
		await ctx.send(message_string)

	@commands.command()
	async def total(self, ctx, *args):
		api = "https://blockchain.info/q/totalbc"
		r = requests.get(api)
		totalCoins = int(r.text)/100000000
		percentMined = totalCoins / 21000000 * 100
		await ctx.send("There are " + '{:,.0f}'.format(totalCoins) + " BTC in circulation. " + '{:,.5f}'.format(percentMined) + "% of all bitcoin have been mined. Only " + '{:,.5f}'.format(100 - percentMined) + "% remain to be mined." )


	# Fetches Bitcoin mempool info from blockstreams mempool
	@commands.command()
	async def fee(self, ctx, *args):
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

		high = '{:,.0f}'.format(brackets[0][3])
		medium = '{:,.0f}'.format((brackets[1][3] + brackets[1][2]) / 2)
		low = '{:,.0f}'.format(brackets[2][2])
		vlow = '{:,.0f}'.format((brackets[3][3] + brackets[3][2]) / 2)


		message_string = '''```
High Priority (1-2 blocks/10m-20m) = {high} sat/vbyte
Medium Priority (2-6 blocks/20m-1h) = {medium} sat/vbyte
Low Priority (6 blocks+/1h+) = {low} sat/vbyte
Very Low Priority (144 blocks+/1d+) = {vlow} sat/vbyte
```'''.format(high=high, medium=medium, low=low, vlow=vlow)
		await ctx.send(message_string)

	@commands.command()
	async def fees(self, ctx, *args):
		await Utilities(self).fee(self, ctx, args)

	@commands.command()
	async def tipUser(self, ctx, user: discord.User, amount, *args):
		member = ctx.message.author
		msg = '{"action":"new_invoice", "id":"' + str(user.id) + '", "requestId":"' + str(member.id) + '", "amount":' + str(amount) + ', "memo":"Bitcoin discord user ' + member.name + ' to ' + user.name + ': ' + " ".join(args) + '"'
		btc = False
		ln = False
		if "btc" in args or ("btc" not in args and "ln" not in args):
			btc = True
			msg += ', "btc": true'
		if "ln" in args or ("btc" not in args and "ln" not in args):
			ln = True
			msg += ', "ln": true'
		if "public" in args:
			print(str(ctx.channel.id))
			msg += ', "channel": "' + str(ctx.channel.id) + '", "noPending": true'
		msg += '}'

		ipc.websocket.send(msg)

	@commands.command()
	async def tip(self, ctx, *args):
		if os.getenv('ENABLE_TIPS') == "1":
			user = None
			amount = None
			if ctx.message.reference is not None:
				reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
				user = reply.author
			if len(args) == 0:
				amount = 0
			for arg in args:
				userMention = re.search("<@([0-9]*)>",arg)
				if userMention:
					user = self.bot.get_user(int(userMention[1]))
					continue
				try:
					amount = int(arg)
				finally:
					continue

			if amount is None:
				amount = 0

			if user is None:
				return await ctx.send("You can pay others using the "+os.getenv('BOT_PREFIX')+"tip commmand with the format of the following examples: `"+os.getenv('BOT_PREFIX')+"tip @user <amount>`,  `"+os.getenv('BOT_PREFIX')+"tip @user`, `"+os.getenv('BOT_PREFIX')+"tip @user <amount> ln`, `"+os.getenv('BOT_PREFIX')+"tip @user btc`, or as a reply to a user you wish to pay in the form `"+os.getenv('BOT_PREFIX')+"tip <amount>`, `"+os.getenv('BOT_PREFIX')+"tip btc` and `"+os.getenv('BOT_PREFIX')+"tip amount ln`. If no amount is provided 0 amounts are assumed. If no btc or ln flag is provided both are assumed. To receive tips use the command `"+os.getenv('BOT_PREFIX')+"register <btc_address>`")

			await Utilities(self).tipUser(self, ctx, user, amount, *args)

	@commands.command()
	async def pay(self, ctx, user: discord.User, amount, *args):
		await Utilities(self).tip(self, ctx, user, amount, args)


	@commands.command()
	async def register(self, ctx, *args):
		if os.getenv('ENABLE_TIPS') == "1":
			msg = ''
			validPrefix = ["1", "3", "bc1", "2", "m", "n", "tb1"]
			if len(args) > 0 and (args[0][:1] in validPrefix or args[0][:3] in validPrefix):
				msg = '{"action":"register", "id":"' + str(ctx.message.author.id) + '", "staticBTC":"'+ args[0] +'"}'
			else:
				msg = '{"action":"register", "id":"' + str(ctx.message.author.id) + '"}'
			ipc.websocket.send(msg)

	@commands.command()
	async def halving(self, ctx, *args):
		api = "https://blockstream.info/api/blocks/tip/height"
		r = requests.get(api)
		height = r.text
		remainder = 210000 - (int(height) % 210000)
		days = (remainder * 10 / 60 / 24)
		date = datetime.datetime.now() + datetime.timedelta(minutes=remainder*10)
		timestamp = time.mktime(date.timetuple())
		message_string = "The halving will happen in " + '{:,.0f}'.format(remainder) + " blocks, or approximately " + '{:,.0f}'.format(days) + " days or around <t:" + '{:.0f}'.format(timestamp) +">"
		await ctx.send(message_string)

	@commands.command()
	async def halvening(self, ctx, *args):
		await Utilities(self).halving(self, ctx, args)

	def get_hashrate(self):
		api = "https://mempool.space/api/v1/mining/hashrate/current"
		r = requests.get(api)
		data = json.loads(r.text)
		return Decimal(data["currentHashrate"])

	@commands.command()
	async def hashrate(self, ctx, *args):
		#                                                   kilo   mega   giga   tera   peta   exa
		network_hashrate = Utilities(self).get_hashrate() / 1000 / 1000 / 1000 / 1000 / 1000 / 1000
		message_string = "The current network hashrate is {} EH/s.".format(floatFormat(round(network_hashrate, 2)))
		await ctx.send(message_string)

	@commands.command()
	async def reward(self, ctx, *args):
		if len(args) == 0:
			await ctx.send("Please specify the number of blocks to average over.")
			return

		try:
			block_count = int(args[0])
		except:
			await ctx.send("An integer block count must be specified.")
			return

		if block_count < 1:
			await ctx.send("Block count must be at least 1")
			return

		api = "https://mempool.space/api/v1/mining/reward-stats/{}".format(block_count)
		r = requests.get(api)
		try:
			data = json.loads(r.text)
			average_reward = Decimal(data["totalReward"]) / block_count / 100000000
		except:
			await ctx.send("Failed to get the average reward.")
			return

		message_string = "The average block reward over the last {} blocks is {} BTC.".format(block_count, floatFormatBtc(round(average_reward, 8)))
		await ctx.send(message_string)

	@commands.command()
	async def solomine(self, ctx, *args):
		if len(args) == 0:
			await ctx.send("Please specify a hashrate in TH/s, eg '150'.")
			return

		try:
			solo_hash_rate = Decimal(args[0])
		except:
			await ctx.send("Invalid hashrate specified.")
			return

		if solo_hash_rate <= 0:
			await ctx.send("With a hashrate of 0 or less, it'll take you forever to mine a block!")
			return

		#                                                   kilo   mega   giga   tera
		network_hashrate = Utilities(self).get_hashrate() / 1000 / 1000 / 1000 / 1000

		hash_share = solo_hash_rate / network_hashrate
		blocks = 1 / hash_share
		days = blocks / 6 / 24

		if days > 365.2425:
			time_description = "{} years".format(floatFormat(round(days / Decimal(365.2425), 2)))
		else:
			time_description = "{} days".format(floatFormat(round(days, 2)))

		message_string = "With a hashrate of {} TH/s, and a network hashrate of {} TH/s, it would take on average {} blocks, or {} to mine a block.".format(
			floatFormat(solo_hash_rate),
			floatFormat(round(network_hashrate, 4)),
			floatFormat(round(blocks, 2)),
			time_description)

		await ctx.send(message_string)

	@commands.command()
	async def mine(self, ctx, *args):
		if len(args) != 4:
			await ctx.send("The !mine command requires four arguments: `period` (block/hour/day/week/month/year), `sats/kWh` (electricity cost), `mining watts` (eg: 3247 for an S19j XP), and `joules per terahash` (eg: 21.5 for an S19j XP).")
			return

		period = args[0].lower()
		try:
			sats_kwh = Decimal(args[1])
		except:
			await ctx.send("Invalid sats/KWh.")

		try:
			mining_watts = Decimal(args[2])
		except:
			await ctx.send("Invalid mining watts.")

		try:
			joules_per_terahash = Decimal(args[3])
		except:
			await ctx.send("Invalid joules/TH.")

		if mining_watts <= 0:
			await ctx.send("Invalid mining watts; mining requires energy!")
			return

		if joules_per_terahash <= 0:
			await ctx.send("Invalid joules per terahash; hashing requires energy!")
			return

		match period:
			case "block":
				period_block_count = 1
			case "hour":
				period_block_count = 6
			case "day":
				period_block_count = 6 * 24
			case "week":
				period_block_count = 6 * 24 * 7
			case "month":
				period_block_count = 6 * 24 * 30
			case "year":
				period_block_count = 6 * 24 * 365.2425
			case _:
				await ctx.send("Invalid calculation period; allowed values are: 'block', 'hour', 'day', week, month, and 'year'.")
				return

		#                                                   kilo   mega   giga   tera
		network_hashrate = Utilities(self).get_hashrate() / 1000 / 1000 / 1000 / 1000

		reward_block_count = max(6 * 24 * 30, round(period_block_count))
		api = "https://mempool.space/api/v1/mining/reward-stats/{}".format(reward_block_count)
		r = requests.get(api)
		try:
			data = json.loads(r.text)
			average_reward = Decimal(data["totalReward"]) / reward_block_count / 100000000
		except:
			await ctx.send("Mining calculation failed; something went wrong when getting the average reward. {} blocks".format(reward_block_count))
			return

		hash_rate = mining_watts / joules_per_terahash
		hash_share = hash_rate / network_hashrate

		watts_per_block = mining_watts / 6
		block_cost = watts_per_block * sats_kwh / 1000 / 100000000
		reward_per_block = average_reward * hash_share

		watts = watts_per_block * period_block_count
		electricity_cost = block_cost * period_block_count
		gross_income = reward_per_block * period_block_count

		net_income = gross_income - electricity_cost

		if watts >= 1000:
			energy_string = '{} kWh'.format(floatFormat(round(watts / 1000, 2)))
		else:
			energy_string = "{:,.0f} Wh".format(watts)

		hash_rate = floatFormat(round(hash_rate, 4))
		net_income = floatFormatBtc(round(net_income, 8))
		gross_income = floatFormatBtc(round(gross_income, 8))
		electricity_cost = floatFormat(round(electricity_cost, 8))
		if sats_kwh == 0.0:
			message_string = "Your hashrate is {} TH/s, and your expected income each {} is {} BTC, using {}.".format(
				hash_rate,
				period,
				net_income,
				energy_string)
		else:
			message_string = "Your hashrate is {} TH/s, and your expected income each {} is {} BTC. Using {} costing {} BTC, your expected net is {} BTC.".format(
				hash_rate,
				period,
				gross_income,
				energy_string,
				electricity_cost,
				net_income)

		await ctx.send(message_string)

async def setup(bot):
	await bot.add_cog(Utilities(bot))

def floatFormat(value):
    return ("{:,.15f}".format(value)).rstrip('0').rstrip('.')

def floatFormatBtc(value):
    return ("{:,.8f}".format(value)).rstrip('.')

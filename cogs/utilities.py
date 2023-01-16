import discord
from discord.ext import commands
import requests
import json
import datetime
import os
from dotenv import load_dotenv
from captcha.image import ImageCaptcha
import math

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Report to mod-log channel. Subsitute other channel ID's as necessary
	#todo get channel by ID
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
						await channel.send(msg);

			await ctx.message.delete()


	@commands.command()
	async def newuser(self, ctx):
		if ctx.message.reference is not None:
			reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
			user = ", " + reply.author.mention
		else:
			user = ""
		await ctx.channel.send("Welcome to our community Bitcoin chat" + user + "! Please review the #rules while you're here; primarily no altcoin, stock, or off topic discussion. If you’re new to bitcoin, please check out https://lopp.net/bitcoin.html, a community curated list of educational resources, tools, and information. To report users breaking the rules, please reply to the message in question with !report <reason>.")
	
	
	@commands.command()
	async def exchanges(self, ctx, *args):
		exchangeDic = {
			"international": "Bitstamp, Coinbase, Gemini, Kraken, OKCoin, Binance",
			"p2p": "Bisq, HodlHodl, BitQuickBitcoin, Local Bitcoins, PaxfulBitcoin",
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
			"europe""": "Kraken, Coinbase, AnyCoin Direct, Binance, Bitcoin.de, bitFlyer, BitPanda, Bitvavo, Kriptomat, Paymium, The Rock Trading, Relai",
			"netherlands": "Bitvavo",
			"poland": "BitBay",
			"ukraine": "Kuna",
			"uk": "Bitstamp, Coinbase, Gemini, Kraken, OKCoin, Binance, Bittylicious, CoinCorner, Coinfloor, CoinJar, Relai",
			"nigeria": "Luno, BuyCoins",
			"south africa": "Luno",
			"uganda": "Binance",
			"canada": "BullBitcoin, Newton, Kraken, Shakepay, Bitbuy, Bisq, Canadian Bitcoins, Coinberry, Coinsmart, NDAX",
			"mexico": "Bitso, Volabit",
			"usa": "Kraken, Coinbase, CEX IO, Bitstamp, bitFlyer, Bittrex, Gemini, itBit, River Financial, Swan Bitcoin, eToro, Binance, LocalBitcoins, Changelly, Coinmama, Bitpanda, Blockchain, BitcoinIRA, CoinSwitch, KuCoin, CashApp, Bisq, Paxful",
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
			await ctx.channel.send("Exchanges in " + arg + ": " + exchangeDic[arg.lower()])
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
			"electrum": {"tags": ["pc", "windows", "linux", "mac", "android", "hot", "advanced", "lightning", "2fa", "spv"], "link":"https://electrum.org/"},
			"core": {"tags": ["pc", "windows", "linux", "hot", "node", "full-node", "advanced"], "link":"https://bitcoincore.org/"},
			"knots": {"tags": ["pc", "windows", "linux", "hot", "node", "full-node", "advanced"], "link":"https://bitcoinknots.org/"},
			"wasabi": {"tags": ["pc", "windows", "hot", "privacy"], "link":"https://wasabiwallet.io/"},
			"coldcard": {"tags": ["hardware", "cold", "requires-wallet"], "link":"https://coldcardwallet.com/"},
			"green": {"tags": ["android", "ios", "2fa", "pc", "windows", "linux", "mac", "hot", "spv"], "link":"https://blockstream.com/green/"},
			"phoenix": {"tags": ["android", "hot", "lightning", "easy"], "link":"https://phoenix.acinq.co/"},
			"lnd": {"tags": ["pc", "windows", "linux", "mac", "hot", "node", "lightning", "lightning-node", "advanced", "partial-custody"], "link":"https://github.com/lightningnetwork/lnd/releases"},
			"c-lightning": {"tags": ["pc", "windows", "linux", "mac", "hot", "node", "lightning", "lightning-node", "advanced"], "link":"https://github.com/ElementsProject/lightning/releases"},
			"blue": {"tags": ["android", "ios", "hot", "lightning", "partial-custody", "easy"], "link":"https://bluewallet.io/"},
			"mycelium": {"tags": ["android", "ios", "hot", "local-trader"], "link":"https://wallet.mycelium.com/"},
			"trezor": {"tags": ["hardware", "hot"], "link":"https://trezor.io/"},
			"breez": {"tags": ["android", "ios", "hot", "lightning", "easy"], "link":"https://breez.technology/"},
			"wallet-of-satoshi": {"tags": ["android", "ios", "hot", "lightning", "partial-custody", "easy"], "link":"https://www.walletofsatoshi.com/"},
			"sbw": {"tags": ["android", "hot", "lightning", "node", "spv", "advanced"], "link":"https://lightning-wallet.com/"},
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
		msg = "<https://github.com/bitcoin/bitcoin> <- the repo\n<https://webchat.freenode.net/?channels=bitcoin-core-dev> <- the irc\n<https://bitcoin.stackexchange.com>/ <- the stack exchange\n<https://lists.linuxfoundation.org/pipermail/bitcoin-dev/> <- the general dev mailinglist\n<https://lists.linuxfoundation.org/pipermail/bitcoin-core-dev/> <- core dev mailinglist\n<https://bitcoinops.org/en/newsletters/> <- optech newsletters dev summary\n<https://bitcoincoreslack.herokuapp.com/> <- core slack"
		await ctx.channel.send(msg)

	@commands.command()
	async def job(self, ctx, *args):
		msg = "Bitcoin job boards and resources: \n<https://pompcryptojobs.com/>\n<https://reddit.com/r/Jobs4Bitcoins>\n<https://reddit.com/r/Jobs4Bitcoin>\n<https://strike.me/jobs>\n<https://www.kraken.com/careers>\n<https://bitstamp.talentlyft.com/>\n<https://www.bitmex.com/careers>\n<https://angel.co/company/river-financial/jobs>\n<https://bitcoinerjobs.co/>"
		await ctx.channel.send(msg)

	@commands.command()
	async def quantum(self, ctx, *args):
		msg = "A general purpose and stable high qubit quantum computer (which doesn't exist and no one is sure if will ever exist) can run an algorithm called shor's. Shor's is used to factor numbers.  You can thus use shor's to derive a private key from a public key. Bitcoin exposes public keys in the scenarios of certain address reuse and when certain transactions are sitting in the mempool, as well as very old 2009 era pay to pubkey coinbases and new taproot transactions. What will happen if such a computer ever exists is slowly attempts to mine the most static of these coins, probably the old coinbases, will occur. Once this happens everyone will know there is a quantum actor and avoid address reuse or in the worst case just move to a new address format. It's also important to remember that a quantum attack takes considerable time, not dissimilar to mining, as it's the process for searching for a private key. Another Algorithm, called grovers, will enable a new kind of mining ASIC, similar to how generations of PoW devices have always functioned."
		await ctx.channel.send(msg)

	@commands.command()
	async def chart(self, ctx, *args):
		exchange = args[0].lower() if len(args) > 0 else "bitstamp"
		timespan = args[0].lower() if len(args) > 1 else "150"
		r = requests.get("https://bitcoincharts.com/charts/chart.png?width=940&m=" + exchange + "USD&SubmitButton=Draw&r=" + timespan + "&i=&c=0&s=&e=&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&", stream = True)
		if r.status_code == 200:
			r.raw.decode_content = True
			embed = discord.Embed()
			embed.set_image(url="https://bitcoincharts.com/charts/chart.png?width=940&m=" + exchange + "USD&SubmitButton=Draw&r=" + timespan + "&i=&c=0&s=&e=&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&")
			msg = "https://bitcoincharts.com/charts/chart.png?width=940&m=" + exchange + "USD&SubmitButton=Draw&r=" + timespan + "&i=&c=0&s=&e=&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&";
			await ctx.channel.send(embed=embed)
	
	@commands.command()
	async def ban(self, ctx, *args):
		if hasattr(ctx.message.author, 'roles') and any(role.name == os.getenv('MOD_ROLE') for role in ctx.message.author.roles):
			n=0
			for user in ctx.message.mentions:
				await user.ban()
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
				await ctx.guild.ban(message.author)
				n = n+1
			await ctx.channel.send(str(n) + " users banned")
		else:
			await ctx.channel.send("No permission.")

	@commands.command()
	async def captcha(self, ctx, *args):
		print("in captcha")
		member = ctx.message.author
		await member.send("Please complete the following captcha:")
		image = ImageCaptcha()
		data = image.generate(str(round(math.sqrt(int(ctx.message.author.id)/int(os.getenv('SALT1')) + int(os.getenv('SALT2'))))))
		await member.send(file=discord.File(data, 'captcha.png'))


def setup(bot):
	bot.add_cog(Utilities(bot))

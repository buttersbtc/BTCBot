import discord
from discord.ext import commands
import requests
import json
import os
from dotenv import load_dotenv

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	load_dotenv()
	reportChannel = os.getenv('REPORT_CHANNEL')

	# Report to r/bitcoin mod-log. Subsitute other channel ID's as necessary
	#todo get channel by ID
	@commands.command()
	async def report(self, ctx):
		load_dotenv()
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
		await ctx.channel.send("Welcome to the r/Bitcoin chat" + user + ". Please review the #rules while you're here; primarily no altcoin, stock, or off topic discussion. Also please read our newcomers faq at https://www.reddit.com/r/Bitcoin/comments/i19uta/bitcoin_newcomers_faq_please_read/. For additional learning resources and information please check out https://lopp.net/bitcoin.html, a community curated resource list. To report users for breaking these rules please reply to the rulebreaking comment and type !report <reason>.")

def setup(bot):
	bot.add_cog(Utilities(bot))
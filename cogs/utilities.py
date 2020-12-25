import discord
from discord.ext import commands
import requests
import json
import os

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	

	# Report to r/bitcoin mod-log. Subsitute other channel ID's as necessary
	@commands.command()
	async def report(self, ctx):
		for guild in self.bot.guilds:
			for channel in guild.channels:
				if channel.name == "mod-log":
					msg = ctx.author.mention + " reporting: " + ctx.message.content.replace("!report ", "")
					if ctx.message.reference is not None:
						print(ctx.message.reference)
						reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
						msg += " - " + reply.author.mention + ": " + reply.content + " - " + reply.jump_url
					await channel.send(msg);

		await ctx.message.delete()



def setup(bot):
	bot.add_cog(Utilities(bot))
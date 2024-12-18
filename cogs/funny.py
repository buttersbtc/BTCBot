import random

from discord.ext import commands

from constants import FUN_FACTS

class Funny(commands.Cog):
    """ Commands subject to funny things """
    def __init__(self, bot):
        self.bot = bot
        self.facts = self.get_facts()
        
    # Random fun facts generator in shuffled order
    @staticmethod
    def get_facts():
        while True:
            random.shuffle(FUN_FACTS)
            for fact in FUN_FACTS:
                yield fact
        
    # Bitcoin is a btc
    @commands.command()
    async def btc(self, ctx):
        await ctx.send("**1 Bitcoin** is worth **1 Bitcoin**")

    # Fetches price in cats
    @commands.command()
    async def cat(self, ctx):
        await ctx.send("**:black_cat:** stop trying to price cats!")
        
    # Fun facts
    @commands.command()
    async def ff(self, ctx):
        await ctx.send(next(self.facts))
    
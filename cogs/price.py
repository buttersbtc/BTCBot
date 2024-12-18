import math

from discord.ext import commands

import BitcoinAPI as api
from constants import ITEM_DICT, CURRENCY_FORMAT_DICT, BLACKLIST, BITCOIN_IN_SATS, FUN_FACTS, REMOVE_HELP, CHART_TYPES

class Price(commands.Cog):
    """ Commands subject to price """
    def __init__(self, bot):
        self.bot = bot
  
    async def on_ready(self):
        print("Pricing commands loaded")

    # Price - All currencies enabled by the APi are automatically supported. Add a currency formatting string to change the way a given currency is displayed
    # To add a new item to the price call make a new entry in the itemDic with the cost and formatStr, the key being the string  used to call that item
    @commands.command()
    async def price(self, ctx, *args):
        if len(args) == 0:
            arg = "usd"
        else:
            arg = args[0].lower()
            
        if arg == "help":
            await ctx.channel.send("**Currency Examples**: !p gbp, !p cad, !p xau")
            await ctx.channel.send(f"**Other Supported items**: {", ".join(ITEM_DICT.keys())}")
            await ctx.channel.send("**!p <item> sats** will give you the cost of the item in satoshis")
            
        elif arg in ITEM_DICT:
            await self.price_item(ctx, args)
            
        elif arg == "sats":
            await self.price_sats(ctx)
        
        else:
            await self.price_currency(ctx, args)
     
    # Price synonym       
    @commands.command()
    async def p(self, ctx, *args):
        await self.price(self, ctx, *args)
        
    # Fetches hours worked for a bitcoin at a rate.
    @commands.command()
    async def wage(self, ctx, *args):
        if len(args) != 2 or not args[0].isdigit() or math.floor(int(args[0])) == 0:
            return await ctx.send("To use wage include the amount earned in the wage and a currency. ex. !wage 15.00 USD")
        
        wage = float(args[0])
        currency = args[1].lower()
        format_string = "**1 Bitcoin** costs **{:,.0f}** hours"
        
        if currency == "usd":
            price, error = api.get_current_price()
            if error:
                return await ctx.send("This price API is currently unavailable")
            
            return await ctx.send(format_string.format(price / wage))
        
        if currency == "sats":
            return await ctx.send(format_string.format(BITCOIN_IN_SATS/wage))
        
        price, _, error = api.get_current_price_in_currency(currency)
        if error:
            return await ctx.send(error)
        
        await ctx.send(format_string.format(price / wage))
        
    # Fetches Bitcoin all time high (ATH) price
    @commands.command()
    async def ath(self, ctx, *args):
        if len(args) == 0:
            ath, error = api.get_bitcoin_ath("usd")
        else:
            ath, error = api.get_bitcoin_ath(args[0].lower())
            
        if error:
            return await ctx.send(error)
        
        await ctx.send(f"**Bitcoin ATH** is currently **{ath}**")
            
    async def price_item(self, ctx, args):
        item = args[0]
        if not item in ITEM_DICT:
            return await ctx.channel.send("Item not supported")
        
        price, error = api.get_current_price()
        if error:
            return await ctx.channel.send("The price API is currently unavailable")
        
        item_map = ITEM_DICT[item]
        emoji = item_map["emoji"]
        name = item_map["name"]
        
        if "sats" in args or "sat" in args:
            price /= 100000000
            price = ITEM_DICT[item]["cost"] / price
            await ctx.channel.send(f"**1 {emoji} {name}** is worth **{price:,.0f} satoshi**")
            
        elif item_map["single"]:
            price = item_map["cost"] / price
            await ctx.channel.send(f"**1 {emoji} {name}** is worth **{price:,.2f} bitcoin**")
            
        else:
            price = price / ITEM_DICT[item]["cost"]
            await ctx.channel.send(f"**1 bitcoin** is worth **{price:,.2f} {emoji} {name}**")
            
    async def price_sats(self, ctx):
        await ctx.channel.send("**1 bitcoin** is equal to **100,000,000 satoshis**")
        
    async def price_currency(self, ctx, args):
        currency = args[0]
        
        _, error = api.get_current_price()
        if error:
            return await ctx.channel.send("The price API is currently unavailable")
        
        price, _, error = api.get_current_price_in_currency(currency)
        if error:
            return await ctx.send(error)
        
        if "sats" in args or "sat" in args:
            price *= 100000000
            return await ctx.channel.send(f"**1 {currency.upper()}** is worth **{price:,.0f} satoshi**")
        
        index = "default"
        suffix = currency.upper()
        if currency in CURRENCY_FORMAT_DICT:
            index = currency
            suffix = ""
            
        await ctx.channel.send(f"**1 bitcoin** is worth **{CURRENCY_FORMAT_DICT[index].format(price)} {suffix}**")

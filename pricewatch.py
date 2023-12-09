import asyncio

import requests
import discord

from BitcoinAPI import BitcoinAPI

class pricewatch():
    async def watch(self, bot):
        api = BitcoinAPI()
        while True:
            await asyncio.sleep(5)
            try:
                price, error = api.get_current_price()
                if error:
                    print(error)
                    continue
                price = "${:,.2f} USD".format(price)

                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=price))
            except requests.RequestException as _:
                print("price watch fail")

    def __init__(self):
        print("Started Price Watch")

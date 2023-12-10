import asyncio
import logging
import requests
import discord
import BitcoinAPI as api

class pricewatch:
    async def watch(self, bot):
        while True:
            await asyncio.sleep(5)
            try:
                price, error = api.get_current_price()
                if error:
                    logging.log(logging.ERROR, error)
                    continue
                price = "${:,.2f} USD".format(price)

                await bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching, name=price
                    )
                )
            except requests.RequestException as _:
                logging.log(logging.ERROR, "price watch fail")

    def __init__(self):
        logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
        logging.log(logging.INFO, "Starting Price Watch")

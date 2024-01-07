import json
import time

import discord
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from chart import chart

TIMEOUT = 10
coincap_rates = "https://api.coincap.io/v2/rates/"
coincap_btc = "https://api.coincap.io/v2/assets/bitcoin"
coingecko = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin&order=market_cap_desc&per_page=100&page=1&sparkline=false"


def get_current_price() -> tuple[None, str] | tuple[float, None]:
    """
    Retrieve the current price of Bitcoin from the CoinCap API.
    This function sends a GET request to the CoinCap API to fetch the current
    price of Bitcoin. If the request is successful, it parses the response to
    extract the price in USD. In case of any exceptions during the request, it
    captures the exception and returns an error message.
    Returns:
    tuple[float, None]: On success, the price of Bitcoin in USD and None for error.
    tuple[None, str]: On failure, None for the price and an error message.
    """
    error = None
    try:
        response = requests.get(coincap_btc, timeout=TIMEOUT)
        response.raise_for_status()
        bitcoin_price = float(response.json()["data"]["priceUsd"])
    except requests.RequestException as e:
        error = f"Failed to fetch price with error: {e}"
        return None, error
    return bitcoin_price, error


def get_currency_rates(currency: str) -> tuple[None, None, str] | tuple[str, str, str]:
    """
    Retrieve the exchange rate for a specified currency from the CoinCap API.
    This function fetches the exchange rates from the CoinCap API and searches
    for the specified currency in the response data. If the currency is found,
    it returns the currency symbol and its rate in USD. If the currency is not found
    or if the request fails, an error message is returned.
    Parameters:
    currency (str): The symbol of the currency (e.g., 'EUR', 'GBP') for which
                    the exchange rate is requested.
    Returns:
    tuple[str, str, str]: On success, the currency symbol, the exchange rate in USD,
                          and None for the error.
    tuple[None, None, str]: On failure, None for the currency symbol and rate,
                            and an error message.
    """
    error = None
    currency_symbol = None
    rateUsd = None
    currency = currency.upper()
    try:
        response = requests.get(coincap_rates, timeout=TIMEOUT)
        response.raise_for_status()
        rates = response.json()
        for rate in rates["data"]:
            if rate["symbol"] == currency:
                currency_symbol = rate["currencySymbol"]
                rateUsd = rate["rateUsd"]
                break
        else:
            error = f"Currency does not exist"
    except requests.RequestException as e:
        error = f"Failed to fetch rates with error: {e}"
        return None, None, error
    return currency_symbol, rateUsd, error


def get_current_price_in_currency(currency: str) -> tuple[None, None, str] | tuple[float, str, None]:
    """
    Retrieve the current price of Bitcoin in a specified currency.
    This function first gets the exchange rate for the given currency against USD
    and the current price of Bitcoin in USD. It then calculates the price of Bitcoin
    in the given currency.
    Parameters:
    currency (str): The symbol of the currency (e.g., 'EUR', 'GBP') in which to
                    convert the Bitcoin price.
    Returns:
    tuple[float, str, None]: On success, the price of Bitcoin in the specified
                             currency, the currency symbol, and None for the error.
    tuple[None, None, str]: On failure, None for the price and currency symbol,
                            and an error message.
    """
    currency_symbol, rateUsd, error = get_currency_rates(currency)
    if error:
        return None, None, error
    price_in_usd, error = get_current_price()
    if error:
        return None, None, error
    price_in_currency = float(price_in_usd) / float(rateUsd)
    return price_in_currency, currency_symbol, None


def get_bitcoin_ath() -> tuple[None, str] | tuple[float, None]:
    """
    Retrieve the all-time high price of Bitcoin from the CoinGecko API.
    This function sends a GET request to the CoinGecko API to fetch the all-time
    high price of Bitcoin. If the request is successful, it parses the response to
    extract the price in USD. In case of any exceptions during the request, it
    captures the exception and returns an error message.
    Returns:
    tuple[float, None]: On success, the all-time high price of Bitcoin in USD and None for error.
    tuple[None, str]: On failure, None for the price and an error message.
    """
    error = None
    try:
        response = requests.get(coingecko, timeout=TIMEOUT)
        response.raise_for_status()
        bitcoin_ath = float(response.json()[0]["ath"])
    except requests.RequestException as e:
        error = f"Failed to fetch price with error: {e}"
        return None, error
    return bitcoin_ath, error


def get_chart(name, timespan="10weeks"):
    error = None
    file = None
    try:
        response = requests.get('https://api.blockchain.info/charts/' + name + '?timespan=' + timespan+ "&format=json", timeout=TIMEOUT)
        responseJson = json.loads(response.content)
        file = discord.File(chart(responseJson), "chart.png")
    except requests.RequestException as e:
        error = f"Failed to fetch chart with error: {e}"
        return None, error
    return file, error


def get_nodes_online() -> int:
    """
    Retrieves the current total number of online nodes.

    This function initiates a headless Chrome browser session to access and scrape data from
    'https://luke.dashjr.org/programs/bitcoin/files/charts/software.html'. It specifically targets
    div elements on the webpage, extracts their textual content, and parses these to identify and
    sum the counts of online nodes. A hardcoded delay of 5 seconds is implemented to allow for complete
    loading of the webpage's dynamic content before data extraction commences.

    Returns:
        int: An integer representing the aggregate count of online nodes.

    """

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://luke.dashjr.org/programs/bitcoin/files/charts/software.html")
    time.sleep(5)

    child_divs = driver.find_elements(By.XPATH, ".//div")

    text = [child.text for child in child_divs if child.text != ""]
    node_count = sum(set([int(value.split(" ")[0]) for value in text]))
    driver.close()

    return node_count

import requests


class BitcoinAPI:
    def __init__(self):
        self.coincap_rates = "https://api.coincap.io/v2/rates/"
        self.coincap_btc = "https://api.coincap.io/v2/assets/bitcoin"
        self.coingecko = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin&order=market_cap_desc&per_page=100&page=1&sparkline=false"

    def get_current_price(self) -> tuple[None, str] | tuple[float, None]:
        error = None
        try:
            response = requests.get(self.coincap_btc)
            response.raise_for_status()
            bitcoin_price = float(response.json()["data"]["priceUsd"])
        except requests.RequestException as e:
            error = f"Failed to fetch price with error: {e}"
            return None, error

        return bitcoin_price, error

    def get_currency_rates(self, currency: str) -> tuple[None, None, str] | tuple[str, str, str]:
        error = None
        currency = currency.upper()
        try:
            response = requests.get(self.coincap_rates)
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

    def get_current_price_in_currency(self, currency: str) -> tuple[None, None, str] | tuple[float, str, None]:
        currency_symbol, rateUsd, error = self.get_currency_rates(currency)
        if error:
            return None, None, error

        price_in_usd, error = self.get_current_price()
        if error:
            return None, None, error

        price_in_currency = float(price_in_usd) / float(rateUsd)
        return price_in_currency, currency_symbol, None

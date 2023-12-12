import unittest
from unittest.mock import patch

from BitcoinAPI import get_current_price_in_currency


class TestGetCurrentPriceInCurrency(unittest.TestCase):

    @patch('BitcoinAPI.get_current_price')
    @patch('BitcoinAPI.get_currency_rates')
    def test_successful_conversion(self, mock_get_currency_rates, mock_get_current_price):
        mock_get_currency_rates.return_value = ("€", "1.12", None)
        mock_get_current_price.return_value = (50000.00, None)

        price, currency_symbol, error = get_current_price_in_currency("EUR")
        self.assertEqual(price, 50000.00 / 1.12)
        self.assertEqual(currency_symbol, "€")
        self.assertIsNone(error)

    @patch('BitcoinAPI.get_current_price')
    @patch('BitcoinAPI.get_currency_rates')
    def test_failure_in_currency_rates(self, mock_get_currency_rates, mock_get_current_price):
        mock_get_currency_rates.return_value = (None, None, "Currency rate fetch error")

        price, currency_symbol, error = get_current_price_in_currency("XYZ")
        self.assertIsNone(price)
        self.assertIsNone(currency_symbol)
        self.assertEqual(error, "Currency rate fetch error")

    @patch('BitcoinAPI.get_current_price')
    @patch('BitcoinAPI.get_currency_rates')
    def test_failure_in_current_price(self, mock_get_currency_rates, mock_get_current_price):
        mock_get_currency_rates.return_value = ("€", "1.12", None)
        mock_get_current_price.return_value = (None, "Bitcoin price fetch error")

        price, currency_symbol, error = get_current_price_in_currency("EUR")
        self.assertIsNone(price)
        self.assertIsNone(currency_symbol)
        self.assertEqual(error, "Bitcoin price fetch error")


if __name__ == '__main__':
    unittest.main()

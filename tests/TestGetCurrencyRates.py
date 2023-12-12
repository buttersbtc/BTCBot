import unittest
from unittest.mock import patch, MagicMock
import requests

from BitcoinAPI import get_currency_rates


class TestGetCurrencyRates(unittest.TestCase):

    @patch('BitcoinAPI.requests.get')
    def test_successful_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {"symbol": "USD", "currencySymbol": "$", "rateUsd": "1.00"},
                {"symbol": "EUR", "currencySymbol": "€", "rateUsd": "1.12"}
            ]
        }
        mock_get.return_value = mock_response

        currency_symbol, rate_usd, error = get_currency_rates("EUR")
        self.assertEqual(currency_symbol, "€")
        self.assertEqual(rate_usd, "1.12")
        self.assertIsNone(error)

    @patch('BitcoinAPI.requests.get')
    def test_currency_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {"symbol": "USD", "currencySymbol": "$", "rateUsd": "1.00"}
            ]
        }
        mock_get.return_value = mock_response

        currency_symbol, rate_usd, error = get_currency_rates("XYZ")
        self.assertIsNone(currency_symbol)
        self.assertIsNone(rate_usd)
        self.assertEqual(error, "Currency does not exist")

    @patch('BitcoinAPI.requests.get')
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Connection error")

        currency_symbol, rate_usd, error = get_currency_rates("EUR")
        self.assertIsNone(currency_symbol)
        self.assertIsNone(rate_usd)
        self.assertIn("Failed to fetch rates with error:", error)


if __name__ == '__main__':
    unittest.main()

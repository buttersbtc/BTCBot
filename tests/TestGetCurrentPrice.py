import unittest
from unittest.mock import patch, MagicMock
import requests

from BitcoinAPI import get_current_price


class TestGetCurrentPrice(unittest.TestCase):

    @patch('BitcoinAPI.requests.get')
    def test_successful_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {"priceUsd": "50000.00"}
        }
        mock_get.return_value = mock_response

        price, error = get_current_price()
        self.assertEqual(price, 50000.00)
        self.assertIsNone(error)

    @patch('BitcoinAPI.requests.get')
    def test_http_error(self, mock_get):
        mock_get.side_effect = requests.HTTPError("Server error")

        price, error = get_current_price()
        self.assertIsNone(price)
        self.assertIn("Failed to fetch price with error:", error)

    @patch('BitcoinAPI.requests.get')
    def test_connection_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError("Connection failed")

        price, error = get_current_price()
        self.assertIsNone(price)
        self.assertIn("Failed to fetch price with error:", error)


if __name__ == '__main__':
    unittest.main()

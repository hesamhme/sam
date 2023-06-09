from django.test import TestCase
from django.urls import reverse


class BuyStockAPITests(TestCase):
    def test_buy_stock_accept(self):
        # Prepare test data and send a POST request
        data = {
            'user': 'user2',
            'stock_name': 'stock1',
            'quantity': 100
        }
        response = self.client.post(reverse('buy-stock'), data)

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'Accept')

    def test_buy_stock_deny(self):
        # Prepare test data and send a POST request
        data = {
            'user': 'user2',
            'stock_name': 'stock1',
            'quantity': 1000
        }
        response = self.client.post(reverse('buy-stock'), data)

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'Deny')

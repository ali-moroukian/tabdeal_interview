from django.db.models import Sum
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from sellers.choices import TRANSACTION_TYPE_DEPOSIT, TRANSACTION_TYPE_WITHDRAW
from sellers.models import Seller, Transaction


class AnimalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller1 = Seller.objects.create()
        self.seller2 = Seller.objects.create()

    @staticmethod
    def get_seller_balance(seller_id):
        return Seller.objects.get(id=seller_id).balance

    def test_seller_balance(self):
        resp = self.client.post(
            reverse('seller_charge', kwargs={'seller_id': self.seller1.id}),
            data={'amount': 100}
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            reverse('seller_charge', kwargs={'seller_id': self.seller1.id}),
            data={'amount': 1000}
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            reverse('seller_charge', kwargs={'seller_id': self.seller2.id}),
            data={'amount': 1000}
        )
        self.assertEqual(resp.status_code, 200)

        for _ in range(60):
            resp = self.client.post(
                reverse('phone_charge', kwargs={'seller_id': self.seller2.id}),
                data={'amount': 5, 'phone_number': '09123456789'}
            )
            self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            reverse('phone_charge', kwargs={'seller_id': self.seller2.id}),
            data={'amount': 1000, 'phone_number': '09123456789'}
        )
        self.assertEqual(resp.status_code, 400)

        self.assertEqual(self.get_seller_balance(self.seller1.id), 1100)
        self.assertEqual(self.get_seller_balance(self.seller2.id), 700)

        deposit_amount = Transaction.objects.filter(
            type=TRANSACTION_TYPE_DEPOSIT).aggregate(Sum('amount'))['amount__sum']
        withdraw_amount = Transaction.objects.filter(
            type=TRANSACTION_TYPE_WITHDRAW).aggregate(Sum('amount'))['amount__sum']
        total_balance = Seller.objects.aggregate(Sum('balance'))['balance__sum']
        self.assertEqual(deposit_amount, withdraw_amount + total_balance)

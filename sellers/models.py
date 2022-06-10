from django.db import models

from sellers.choices import *


class Seller(models.Model):
    balance = models.PositiveBigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    TYPES = (
        (TRANSACTION_TYPE_DEPOSIT, 'deposit'),
        (TRANSACTION_TYPE_WITHDRAW, 'withdraw'),
    )

    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, related_name='transactions')

    amount = models.PositiveBigIntegerField()
    type = models.CharField(max_length=50, choices=TYPES)
    time = models.DateTimeField(auto_now_add=True)

    extra_data = models.JSONField(blank=True, default=dict)

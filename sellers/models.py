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

    amount = models.PositiveBigIntegerField()
    type = models.CharField(max_length=50, choices=TYPES)
    time = models.DateTimeField(auto_now_add=True)

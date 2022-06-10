import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from sellers.models import Seller


class SellerBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('id', 'balance',)
        read_only_fields = ('balance',)


class ChargeSellerSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)


class ChargePhoneSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    phone_number = serializers.CharField(max_length=100)

    def validate_amount(self, value):
        seller = self.context['seller']
        if value > seller.balance:
            raise ValidationError('seller balance is not enough.')
        return value

    @staticmethod
    def validate_phone_number(value):
        if not re.match('^09[0-9]{9}$', value):
            raise ValidationError('phone number should start with 09 and have 11 digits.')
        return value

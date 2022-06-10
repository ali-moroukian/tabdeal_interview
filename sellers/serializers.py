from rest_framework import serializers

from sellers.models import Seller


class SellerBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('id', 'balance',)
        read_only_fields = ('balance',)


class ChargeSellerSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)

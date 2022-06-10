from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from sellers.choices import *
from sellers.models import Seller, Transaction
from sellers.serializers import ChargeSellerSerializer, SellerBalanceSerializer, ChargePhoneSerializer


class ChargeSellerAPIView(APIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = ChargeSellerSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data.get('amount')

        seller = get_object_or_404(Seller, id=kwargs['seller_id'])
        seller.balance += amount
        seller.save()

        Transaction.objects.create(
            seller=seller,
            amount=amount,
            type=TRANSACTION_TYPE_DEPOSIT,
        )

        return Response(SellerBalanceSerializer(seller).data)


class ChargePhoneAPIView(APIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        seller = get_object_or_404(Seller, id=kwargs['seller_id'])

        serializer = ChargePhoneSerializer(data=self.request.data, context={'seller': seller})
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data.get('amount')
        phone_number = serializer.validated_data.get('phone_number')

        seller.balance -= amount
        seller.save()

        Transaction.objects.create(
            seller=seller,
            amount=amount,
            type=TRANSACTION_TYPE_WITHDRAW,
            extra_data={'phone_number': phone_number},
        )

        return Response({
            'detail': f'{phone_number} charged {amount} unit.',
            'seller': SellerBalanceSerializer(seller).data,
        })

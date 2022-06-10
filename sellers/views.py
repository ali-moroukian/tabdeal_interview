from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from sellers.choices import *
from sellers.models import Seller, Transaction
from sellers.serializers import ChargeSellerSerializer, SellerBalanceSerializer


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
            amount=amount,
            type=TRANSACTION_TYPE_DEPOSIT,
        )

        return Response(SellerBalanceSerializer(seller).data)

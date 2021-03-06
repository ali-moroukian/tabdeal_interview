from django.urls import path

from sellers.views import ChargeSellerAPIView, ChargePhoneAPIView

urlpatterns = [
    path('<int:seller_id>/charge/', ChargeSellerAPIView.as_view(), name='seller_charge'),
    path('<int:seller_id>/charge_phone/', ChargePhoneAPIView.as_view(), name='phone_charge'),
]

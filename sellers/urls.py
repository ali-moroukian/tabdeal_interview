from django.urls import path

from sellers.views import ChargeSellerAPIView

urlpatterns = [
    path('<int:seller_id>/charge/', ChargeSellerAPIView.as_view()),
]
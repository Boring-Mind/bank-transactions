from django.urls import path

from .views import TransactionsCreateView

urlpatterns = [
    path('', TransactionsCreateView.as_view(), name="transaction_create"),
]

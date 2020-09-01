from django.urls import path

from .views import AccountCreateView, AccountIdView

urlpatterns = [
    path('/<int:pk>', AccountIdView.as_view(), name="account_id"),
    path('', AccountCreateView.as_view(), name="account_create"),
]

from django.urls import path

from .views import AccountCreateView

urlpatterns = [
    path('', AccountCreateView.as_view(), name="account_create"),
]

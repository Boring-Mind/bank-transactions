from django.urls import path

from .views import currency_get_view

urlpatterns = [
    path('', currency_get_view, name="currency"),
]

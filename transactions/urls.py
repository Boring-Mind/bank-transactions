from django.urls import path

from .views import transactions_views

urlpatterns = [
    path('', transactions_views, name="transactions"),
]

from django.urls import path

from .views import *

urlpatterns = [
    path('', ClientCreateView.as_view(), name="user"),
    path('<int:pk>', ClientIdView.as_view(), name="user_id"),
]

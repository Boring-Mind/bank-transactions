from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('users/', include('clients.urls')),
    path('currencies', include('currency.urls')),
    path('transactions', include('transactions.urls')),
    path('accounts', include('accounts.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]

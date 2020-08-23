from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('users/', include('clients.urls')),
    path('currencies', include('currency.urls')),
    path('transactions', include('transactions.urls')),
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

urlpatterns = format_suffix_patterns(urlpatterns)

from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('users/', include('clients.urls')),
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

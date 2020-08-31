from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import (AuthenticationFailed,
                                                 InvalidToken)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.state import User


class JWTCachedAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """Find and return a user using the given validated token.

        User credentials acquisition is cached for 5 minutes.
        If the user is deleted, cache is invalidated.
        Timeout of cache cannot last more than access token lifetime.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(
                _('Token contained no recognizable user identification')
            )

        try:
            if cached := cache.get(f'jwt_user_{user_id}'):
                user = cached
            else:
                user = User.objects.get(
                    **{api_settings.USER_ID_FIELD: user_id}
                )
                cache.set(f'jwt_user_{user_id}', user)
        except User.DoesNotExist:
            raise AuthenticationFailed(
                _('User not found'), code='user_not_found'
            )

        if not user.is_active:
            raise AuthenticationFailed(
                _('User is inactive'), code='user_inactive'
            )

        return user

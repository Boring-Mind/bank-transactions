from drf_utils.renderers import PlainJsonRenderer
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response

from .models import Currency
from .serializers import CurrencyReadSerializer


def is_authenticated(request) -> bool:
    return bool(request.user and request.user.is_authenticated)


@api_view(['GET'])
@renderer_classes([PlainJsonRenderer])
def currency_get_view(request):
    if not is_authenticated(request):
        return Response(
            {'message': 'Authentication token is not provided.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    data = Currency.objects.all().defer('full_name')
    data = CurrencyReadSerializer.serialize_data(data)

    return Response(data, status=status.HTTP_200_OK)

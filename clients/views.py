from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import ClientSerializer


@api_view(['POST'])
def register_user_view(request):
    data = JSONParser().parse(request)
    serializer = ClientSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User created"}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

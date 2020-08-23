from clients.permissions import IsOwnerOrAdmin
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Account
from .serializers import AccountSerializer


class AccountIdView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = None
    permission_classes = [IsOwnerOrAdmin]

    def get(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        return super().get(request, *args, **kwargs)


class AccountCreateView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from silk.profiling.profiler import silk_profile

from .models import Transactions
from .serializers import TransactionsSerializer


class TransactionsCreateView(CreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    @silk_profile(name="Transactions Create View")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

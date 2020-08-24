from distutils.util import strtobool

from django.views.decorators.csrf import csrf_exempt
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from silk.profiling.profiler import silk_profile

from .models import Transactions
from .serializers import TransactionsPostSerializer, TransactionsReadSerializer


class TransactionsPagination(PageNumberPagination):
    """Transactions pagination class.

    Looks similar to the default pagination class, except it cannot
    receive page size from user.
    """
    
    page_size = 100
    page_query_param = None
    max_page_size = 100


class IncomingFilter(BaseFilterBackend):
    """Filter that shows only incoming or outgoing transactions."""

    @classmethod
    def cut_url_suffix(cls, get_param: str) -> str:
        return get_param.split('.')[0].lower()

    def filter_queryset(self, request, queryset, view):
        # Parse incoming parameter
        incoming = request.GET.get('incoming')
        incoming = bool(strtobool(__class__.cut_url_suffix(incoming)))

        # Parse account_id parameter
        acc_id = request.GET.get('acc_id')
        acc_id = __class__.cut_url_suffix(acc_id)
        
        if incoming:
            # Return all the incoming transactions
            return queryset.filter(receiver_id=acc_id)
        # Return all the outgoing transactions
        return queryset.filter(sender_id=acc_id)


class TransactionsCreateView(CreateAPIView):
    """View that creates new transaction on POST request."""

    queryset = Transactions.objects.all()
    serializer_class = TransactionsPostSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    @silk_profile(name="Transactions Create View")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TransactionsListView(ListAPIView):
    """View that shows all the transactions with pagination.

    Users must be authenticated.
    """

    queryset = Transactions.objects.values()
    serializer_class = TransactionsReadSerializer
    pagination_class = TransactionsPagination
    permission_classes = [IsAuthenticated]


class TransactionsIncomingView(TransactionsListView):
    """View that shows only incoming or outcoming operations."""

    filter_backends = [IncomingFilter]


@csrf_exempt
def transactions_views(request):
    """Router for all the transactions views.
    
    Needed in order to perform multiple requests to the same URL.
    Requests differ by their method or params and don't overlap.
    """
    if request.method == 'POST':
        return TransactionsCreateView.as_view()(request)
    elif request.method == 'GET':
        if request.GET.get('acc_id'):
            return TransactionsIncomingView.as_view()(request)
        elif request.GET.get('page'):
            return TransactionsListView.as_view()(request)

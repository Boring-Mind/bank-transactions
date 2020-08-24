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
    page_size = 100
    page_query_param = None
    max_page_size = 100


class IncomingFilter(BaseFilterBackend):
    """Filter that shows only incoming or outgoing transactions."""

    @classmethod
    def cut_url_suffix(cls, get_param: str) -> str:
        return get_param.split('.')[0].lower()

    def filter_queryset(self, request, queryset, view):
        # import pdb; pdb.set_trace()

        incoming = request.GET.get('incoming')
        incoming = bool(strtobool(__class__.cut_url_suffix(incoming)))

        acc_id = request.GET.get('acc_id')
        acc_id = __class__.cut_url_suffix(acc_id)
        return queryset.filter(sender_id=acc_id)


class TransactionsCreateView(CreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsPostSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    @silk_profile(name="Transactions Create View")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TransactionsListView(ListAPIView):
    queryset = Transactions.objects.select_related(
        'sender_id', 'receiver_id'
    ).values()
    serializer_class = TransactionsReadSerializer
    pagination_class = TransactionsPagination
    permission_classes = [IsAuthenticated]

class TransactionsIncomingView(TransactionsListView):
    filter_backends = [IncomingFilter]

    # def get(self, request, *args, **kwargs):


@csrf_exempt
def transactions_views(request):
    if request.method == 'POST':
        return TransactionsCreateView.as_view()(request)
    elif request.method == 'GET':
        if request.GET.get('acc_id'):
            return TransactionsIncomingView.as_view()(request)
        elif request.GET.get('page'):
            return TransactionsListView.as_view()(request)

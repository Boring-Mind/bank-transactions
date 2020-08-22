from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from silk.profiling.profiler import silk_profile

from .models import Client
from .serializers import ClientSerializer


class ClientIdView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = None

    @silk_profile(name="Client id Get View")
    def get(self, request, *args, **kwargs):
        self.serializer_class = ClientSerializer
        return super().get(request, *args, **kwargs)


class ClientCreateView(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = None

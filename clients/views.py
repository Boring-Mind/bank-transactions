from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from silk.profiling.profiler import silk_profile

from .models import Client
from .permissions import IsOwnerOrAdmin
from .serializers import ClientSerializer


class ClientIdView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = None
    permission_classes = [IsOwnerOrAdmin]

    @silk_profile(name="Client id Get View")
    def get(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        return super().get(request, *args, **kwargs)


class ClientCreateView(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = None
    permission_classes = [AllowAny]

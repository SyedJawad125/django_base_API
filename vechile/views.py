from .serializers import MakeSerializer, VechileSerializer
from .filters import VechileFilter, MakeFilter
from utils.common_crud import BaseAPIView

class MakeAPIView(BaseAPIView):
    serializer_class = MakeSerializer
    filterset_class = MakeFilter

class VechileAPIView(BaseAPIView):
    serializer_class = VechileSerializer
    filterset_class = VechileFilter
    prefetch_related_args = ['make']

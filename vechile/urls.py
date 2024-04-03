from django.urls import path
from .views import MakeAPIView, VechileAPIView

urlpatterns = [
    path('make', MakeAPIView.as_view({'get': 'get_records',
                                            'post': 'create_record',
                                            'patch': 'update_record',
                                            'delete': 'delete_records'})),

    path('vechile', VechileAPIView.as_view({'get': 'get_records',
                                      'post': 'create_record',
                                      'patch': 'update_record',
                                      'delete': 'delete_records'})),
]
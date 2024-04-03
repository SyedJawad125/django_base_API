from rest_framework.viewsets import ModelViewSet
from utils.helper import create_response, get_first_error_message_from_serializer_errors, paginate_data, get_params
from utils.response_messages import *
from django.db.models import Q


class BaseAPIView(ModelViewSet):
    serializer_class = None
    filterset_class = None
    select_related_args = []
    prefetch_related_args = []
    or_filters = {}
    and_filters = {}

    def create_record(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data, context={'request':request})
            if serialized_data.is_valid():
                response_data = serialized_data.save()
                return create_response(self.serializer_class(response_data).data, SUCCESSFUL, 200)
            return create_response({},
                                   get_first_error_message_from_serializer_errors(serialized_data.errors, UNSUCCESSFUL),
                                   400)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)

    def get_records(self, request):
        try:
            order = request.query_params.get('order', 'desc')
            order_by = request.query_params.get('order_by', 'id')
            if order and order_by:
                order_by_ = order_by.lower()
                if hasattr(self.serializer_class.Meta.model, order_by_) and order_by != "id":
                    order_by = order_by_
                if order:
                    if order == 'desc':
                        order_by = f"-{order_by_}"
                    else:
                        order_by = order_by_

            instances = self.serializer_class.Meta.model.objects.select_related(*self.select_related_args).prefetch_related(*self.prefetch_related_args).order_by(order_by)
            filtered_data = self.filterset_class(request.GET, queryset=instances)
            data = filtered_data.qs

            data, count = paginate_data(data, request)
            serialized_data = self.serializer_class(data, many=True).data
            response_data = {
                "count": count,
                "data": serialized_data
            }
            return create_response(response_data, SUCCESSFUL, 200)
        except Exception as e:
            return create_response({'error': str(e)}, UNSUCCESSFUL, 500)

    def update_record(self, request):
        try:
            if "id" in request.data:
                instance = self.serializer_class.Meta.model.objects.filter(id=request.data.get("id")).first()
                if instance:
                    serialized_data = self.serializer_class(instance, data=request.data, partial=True, context={'request':request})
                    if serialized_data.is_valid():
                        response_data = serialized_data.save()
                        return create_response(self.serializer_class(response_data).data, SUCCESSFUL, 200)
                    return create_response({}, get_first_error_message_from_serializer_errors(serialized_data.errors, UNSUCCESSFUL),400)
                else:
                    return create_response({}, NOT_FOUND, 400)
            else:
                return create_response({}, ID_NOT_PROVIDED, 404)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)

    def delete_records(self, request):
        try:
            kwargs = {}
            if "id" in request.query_params:
                kwargs = get_params("id", request.query_params.get("id"), kwargs)
                #multiple records deletion
                instances = self.serializer_class.Meta.model.objects.filter(**kwargs)
                if instances:
                    instances.delete()
                    return create_response({}, SUCCESSFUL, 200)
                else:
                    return create_response({}, NOT_FOUND, 404)
            else:
                return create_response({}, ID_NOT_PROVIDED, 404)
        except Exception as e:
            return create_response({'error': str(e)}, UNSUCCESSFUL, 500)


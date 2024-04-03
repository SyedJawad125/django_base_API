import ast
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList
from .pagination import Pagination
from django.db import models


def create_response(data, message, status_code):
    result = {
        "status_code": status_code,
        "message": message,
        "data": data
    }
    return Response(result, status=status_code)

def get_first_error_message_from_serializer_errors(serialized_errors, default_message=""):
    if not serialized_errors:
        return default_message
    try:
        serialized_error_dict = serialized_errors
        if isinstance(serialized_errors, ReturnList):
            serialized_error_dict = serialized_errors[0]
        serialized_errors_keys = list(serialized_error_dict.keys())
        try:
            message = serialized_error_dict[serialized_errors_keys[0]][0].replace("This", serialized_errors_keys[0])
            return message
        except:
            return serialized_error_dict[serialized_errors_keys[0]][0]
    except Exception as e:
        return default_message

def paginate_data(data, request):
    limit = request.query_params.get('limit', None)
    offset = request.query_params.get('offset', None)
    if limit and offset:
        pagination = Pagination()
        data, count = pagination.paginate_queryset(data, request)
        return data, count
    else:
        return data, data.count()

def get_params(name, instance, kwargs):
    instance = check_for_one_or_many(instance)
    if type(instance) == list or type(instance) == tuple:
        kwargs[f"{name}__in"] = instance
    elif type(instance) == str and instance.lower() in ["true", "false"]:
        kwargs[f"{name}"] = bool(instance.lower() == "true")
    else:
        kwargs[f"{name}"] = instance
    return kwargs

def check_for_one_or_many(instances):
    try:
        instance = ast.literal_eval(instances)
        return instance
    except Exception as e:
        print(e)
        return instances


class TimeStamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
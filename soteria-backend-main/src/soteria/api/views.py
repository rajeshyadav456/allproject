from django_tenants.utils import get_public_schema_name
from rest_framework import exceptions, generics, views
from rest_framework.response import Response

from soteria.api.utils import prep_success_response_data
from soteria.middleware.current_user import set_current_user


class ResponseMixin:
    def success_response(self, data=None, item=None, items=None, **kwargs) -> Response:
        resp_data = prep_success_response_data(data, item, items)
        return Response(data=resp_data, **kwargs)


class MethodSerializerMixin:
    """
    Utility class for get different serializer class by method.
    For example:
    method_serializer_classes = {
        ('GET', ): MyModelListViewSerializer,
        ('PUT', 'PATCH'): MyModelCreateUpdateSerializer
    }
    """

    method_serializer_classes = None

    def get_serializer_class(self):
        assert self.method_serializer_classes is not None, (
            "Expected view %s should contain method_serializer_classes "
            "to get right serializer class." % (self.__class__.__name__,)
        )
        for methods, serializer_cls in self.method_serializer_classes.items():
            if self.request.method in methods:
                return serializer_cls

        raise exceptions.MethodNotAllowed(self.request.method)


class APIView(ResponseMixin, views.APIView):
    def perform_authentication(self, request):
        # NOTE: we intentionally access `request.user` and assigned to variable,
        # because view authentication performed lazily, the first time either
        # `request.user` or `request.auth` is accessed.
        user = request.user
        set_current_user(user)


class GenericAPIView(ResponseMixin, generics.GenericAPIView):
    def perform_authentication(self, request):
        # NOTE: we intentionally access `request.user` and assigned to variable,
        # because view authentication performed lazily, the first time either
        # `request.user` or `request.auth` is accessed.
        user = request.user
        set_current_user(user)


class TenantAPIView(GenericAPIView):
    def perform_authentication(self, request):
        """
        https://www.postgresql.org/docs/current/ddl-schemas.html#DDL-SCHEMAS-PUBLIC
        : by default we setting connection to `public` tenant.
        In this method we make sure our connect must not set to `default-tenant`
        """
        from django.db import connection

        from soteria.exception import InvalidOrganizationConnection

        # tenant model
        from soteria.models import Organization

        default_tenant = Organization.objects.get(schema_name=get_public_schema_name())
        if default_tenant == connection.get_tenant():
            raise InvalidOrganizationConnection()
        user = request.user
        set_current_user(user)

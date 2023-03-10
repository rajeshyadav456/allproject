from django_filters import rest_framework as dj_filters
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.pagination import DefaultPageNumberPagination, PaginatedListAPIViewMixin
from soteria.api.views import MethodSerializerMixin, TenantAPIView
from soteria.atms.customform import CustomFormSchemaJSONField
from soteria.atms.models import Form
from soteria.atms.services.form import create_form_schema


class FormSchemaListCreateAPI(PaginatedListAPIViewMixin, MethodSerializerMixin, TenantAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Form
            fields = (
                "id",
                "name",
                "schema",
            )

    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=100)
        schema = CustomFormSchemaJSONField()

        class Meta:
            model = Form
            fields = ("name", "schema")

    class ListFilterSet(dj_filters.FilterSet):
        name = dj_filters.CharFilter(field_name="name", lookup_expr="contains")

        class Meta:
            model = Form
            fields = []

    class ListPagination(DefaultPageNumberPagination):
        pass

    ListOutputSerializer = OutputSerializer

    method_serializer_classes = {
        ("GET",): ListOutputSerializer,
        ("POST",): InputSerializer,
    }
    pagination_class = ListPagination
    queryset = Form.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticated,)
    filter_backends = [
        dj_filters.DjangoFilterBackend,
    ]
    filter_class = ListFilterSet

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        form = create_form_schema(form_name=data["name"], schema=data["schema"])
        resp_data = self.OutputSerializer(form).data
        return self.success_response(data=resp_data, status=status.HTTP_201_CREATED)

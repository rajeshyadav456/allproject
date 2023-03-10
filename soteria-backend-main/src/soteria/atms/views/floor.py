from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from soteria.api.pagination import DefaultPageNumberPagination, PaginatedListAPIViewMixin
from soteria.api.views import TenantAPIView
from soteria.atms.models import Floor


class FloorListAPI(
    PaginatedListAPIViewMixin,
    TenantAPIView,
):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Floor
            fields = (
                "id",
                "name",
                "description",
                "is_active",
                "created_at",
                "updated_at",
            )

    class ListPagination(DefaultPageNumberPagination):
        pass

    serializer_class = OutputSerializer
    pagination_class = ListPagination
    queryset = Floor.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

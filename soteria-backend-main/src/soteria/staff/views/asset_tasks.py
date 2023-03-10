from django_filters import rest_framework as dj_filters
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from soteria.api.pagination import DefaultPageNumberPagination, PaginatedListAPIViewMixin
from soteria.api.views import TenantAPIView
from soteria.atms.models import Task
from soteria.atms.serializers.job import JobDetailOutputSerializer


class AssetTaskListAPI(PaginatedListAPIViewMixin, TenantAPIView):
    class ListOutputSerializer(serializers.ModelSerializer):
        job = JobDetailOutputSerializer()

        class Meta:
            model = Task
            fields = (
                "id",
                "name",
                "job",
                "status",
                "completed_at",
                "form_submission_data",
                "start_at",
                "end_at",
                "created_at",
            )

    class ListFilterSet(dj_filters.FilterSet):
        name = dj_filters.CharFilter(field_name="name", lookup_expr="contains")
        date = dj_filters.DateFilter(method="filter_for_date")

        class Meta:
            model = Task
            fields = ["status"]

        def filter_for_date(self, queryset, name, value):
            return queryset.filter(created_at__date=value)

    class ListPagination(DefaultPageNumberPagination):
        pass

    queryset = Task.objects.all()
    serializer_class = ListOutputSerializer
    pagination_class = ListPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = [
        dj_filters.DjangoFilterBackend,
    ]
    filter_class = ListFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            job__assign_to__user=self.request.user, job__asset__id=self.kwargs["asset_id"]
        )
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

from django_filters import rest_framework as dj_filters
from rest_framework.permissions import IsAuthenticated

from soteria.api.pagination import DefaultPageNumberPagination, PaginatedListAPIViewMixin
from soteria.api.views import TenantAPIView
from soteria.atms.models import Job, Task
from soteria.staff.serializer.task_detail import TaskDetailSerializer


class TaskListAPI(PaginatedListAPIViewMixin, TenantAPIView):
    class ListOutputSerializer(TaskDetailSerializer):
        pass

    class ListFilterSet(dj_filters.FilterSet):
        form_submission_data_choices = (
            ("True", "true"),
            ("False", "false"),
        )
        name = dj_filters.CharFilter(field_name="name", lookup_expr="contains")
        date = dj_filters.DateFilter(method="filter_for_date")
        job = dj_filters.ModelChoiceFilter(queryset=Job.objects.all())
        start_at = dj_filters.DateFilter(field_name="start_at__date")
        end_at = dj_filters.DateFilter(field_name="end_at__date")
        completed_at = dj_filters.DateFilter(field_name="completed_at__date")
        is_late_submission = dj_filters.ChoiceFilter(field_name="is_late_submission", choices=form_submission_data_choices)

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
        qs = qs.filter(job__assign_to__user=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

from rest_framework.permissions import IsAuthenticated

from soteria.api.views import TenantAPIView
from soteria.atms.models import Task
from soteria.staff.serializer.task_detail import TaskDetailSerializer


class TaskDetailAPI(TenantAPIView):
    class OutputSerializer(TaskDetailSerializer):
        pass

    lookup_url_kwarg = "task_id"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Task.objects.filter(job__assign_to__user=self.request.user)
        qs = qs.filter(id=self.kwargs["task_id"])
        return qs

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        resp_data = self.OutputSerializer(task).data
        return self.success_response(resp_data)

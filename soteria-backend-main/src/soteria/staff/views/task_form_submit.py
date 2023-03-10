from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from soteria.api.views import TenantAPIView
from soteria.atms.customform import CustomFormDataJSONField
from soteria.atms.models import Task
from soteria.atms.serializers.job import JobDetailOutputSerializer
from soteria.staff.services.task_form_submit import submit_task_form


class TaskFormSubmitAPI(TenantAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        job = JobDetailOutputSerializer()

        class Meta:
            model = Task
            fields = (
                "id",
                "job",
                "status",
                "completed_at",
                "form_submission_data",
                "start_at",
                "end_at",
            )

    class InputSerializer(serializers.Serializer):
        schema = CustomFormDataJSONField()

    serializer_class = InputSerializer
    lookup_url_kwarg = "task_id"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Task.objects.filter(job__assign_to__user=self.request.user)
        qs = qs.filter(id=self.kwargs["task_id"])
        return qs

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        task = self.get_object()
        submited_task = submit_task_form(task, data)
        resp_data = self.OutputSerializer(submited_task).data
        return self.success_response(resp_data)

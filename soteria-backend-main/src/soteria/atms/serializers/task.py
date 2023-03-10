from rest_framework import serializers

from soteria.atms.models.task import Task
from soteria.atms.serializers.job import JobDetailOutputSerializer


class TaskDetailSerializer(serializers.ModelSerializer):
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
            "end_at"
        )

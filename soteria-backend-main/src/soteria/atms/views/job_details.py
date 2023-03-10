from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.fields import TimeZoneSerializerField
from soteria.api.views import TenantAPIView
from soteria.atms.models import Asset, Form, Job, JobType
from soteria.atms.serializers.job import JobDetailOutputSerializer
from soteria.atms.services.job import deactivate_job, update_job_details
from soteria.orgs.models import Location, OrganizationMember


class JobDetailGetUpdateDeleteAPI(TenantAPIView):
    class OutputSerializer(JobDetailOutputSerializer):
        pass

    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=200, required=False)
        description = serializers.CharField(max_length=300, required=False)
        job_type = serializers.PrimaryKeyRelatedField(
            queryset=JobType.objects.all(), required=False
        )
        asset = serializers.PrimaryKeyRelatedField(queryset=Asset.objects.all(), required=False)
        assign_to = serializers.PrimaryKeyRelatedField(
            queryset=OrganizationMember.objects.all(), required=False
        )
        location = serializers.PrimaryKeyRelatedField(
            queryset=Location.objects.all(), required=False
        )
        form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all(), required=False)
        weekdays = serializers.ListField(required=False)
        time_ranges = serializers.ListField(child=serializers.TimeField(), required=False)
        duration = serializers.CharField(required=False)
        timezone = TimeZoneSerializerField(required=False)

        class Meta:
            model = Job
            fields = (
                "name",
                "description",
                "asset",
                "assign_to",
                "form",
                "location",
                "job_type",
                "weekdays",
                "time_ranges",
                "duration",
                "timezone",
                "time_scale",
                "start_at",
                "end_at",
            )

        def validate_weekdays(self, value):
            for day in value:
                if day not in range(1, 8):
                    raise serializers.ValidationError(
                        _(
                            "Invalid weekday number, should be in range 1 to 7, where "
                            "Mon=1... Sun=7"
                        )
                    )

            return value

    UpdateOutputSerializer = OutputSerializer
    lookup_url_kwarg = "job_id"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Job.objects.all()
        qs = qs.filter(id=self.kwargs["job_id"])
        return qs

    def get(self, request, *args, **kwargs):
        Job = self.get_object()
        resp_data = self.OutputSerializer(Job).data
        return self.success_response(resp_data)

    def put(self, request, *args, **kwargs):
        job = self.get_object()
        serializer = self.InputSerializer(instance=job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        job = update_job_details(job, data)
        resp_data = self.UpdateOutputSerializer(job).data
        return self.success_response(resp_data)

    def delete(self, request, *args, **kwargs):
        job = self.get_object()
        deactivate_job(job)
        return self.success_response(
            data={"message": _("Job is deactivated successfully")},
            status=status.HTTP_200_OK,
        )

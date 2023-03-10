from rest_framework import serializers

from soteria.api.views import TenantAPIView
from soteria.reports.services.download_report import download_report, download_task_report


class DownloadReportAPI(TenantAPIView):
    class InputSerializer(serializers.Serializer):
        start_date = serializers.DateField()
        end_date = serializers.DateField()
        location_id = serializers.UUIDField(required=False)
        report_type = serializers.CharField()

        def validate(self, attrs):
            report_type = attrs["report_type"]
            if report_type not in ["csv", "excel"]:
                raise serializers.ValidationError("Report type must be csv or excel")
            return attrs

    serializer_class = InputSerializer

    def get(self, request, organization_id, report_id):
        serializer = self.get_serializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        report_data = download_report(report_id, organization_id, data)

        if report_data:
            return report_data
        else:
            return self.success_response(data={"message": "File does not exists"})


class DownloadTaskReportAPI(TenantAPIView):
    class InputSerializer(serializers.Serializer):
        report_type = serializers.CharField()

        def validate(self, attrs):
            report_type = attrs["report_type"]
            if report_type not in ["csv", "excel"]:
                raise serializers.ValidationError("Report type must be csv or excel")
            return attrs

    serializer_class = InputSerializer

    def get(self, *args, **kwargs):
        task_id = self.kwargs.get("task_id")
        serializer = self.get_serializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        data = download_task_report(task_id, data)
        if data:
            return data
        else:
            return self.success_response(data={"message": "File does not exists"})

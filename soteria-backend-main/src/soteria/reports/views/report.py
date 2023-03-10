from soteria.api.views import TenantAPIView
from soteria.models.report import Report
from soteria.reports.serializer.report_detail import ReportsDetailSerializer


class ReportDetailAPI(TenantAPIView):
    def get(self, request, *args, **kwargs):
        report = Report.objects.all()
        resp_data = ReportsDetailSerializer(report, many=True).data
        return self.success_response(resp_data)

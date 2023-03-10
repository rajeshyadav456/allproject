from django.urls import path

from soteria.reports.views.download_report import DownloadReportAPI, DownloadTaskReportAPI
from soteria.reports.views.report import ReportDetailAPI

urlpatterns = [
    path(
        "api/v1/organizations/<uuid:organization_id>/reports/",
        ReportDetailAPI.as_view(),
        name="reports-list",
    ),
    path(
        "api/v1/organizations/<uuid:organization_id>/reports/<int:report_id>/download/",
        DownloadReportAPI.as_view(),
        name="reports-download",
    ),
    path(
        "api/v1/organizations/<uuid:organization_id>/tasks/<uuid:task_id>/download/",
        DownloadTaskReportAPI.as_view(),
        name="task-reports-download",
    ),
]

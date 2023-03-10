import datetime
from io import BytesIO
from typing import Dict

import pandas as pd
from django.http import FileResponse

from soteria.atms.serializers.assets import Asset, AssetReportSerializer
from soteria.atms.serializers.job import Job, JobReporteSerializer
from soteria.atms.serializers.task import Task
from soteria.models.report import Report
from soteria.orgs.serializers.location import Location, LocationDetailSerializer

REPORT_TYPE = {
    "asset": {"model": Asset, "serializer": AssetReportSerializer},
    "location": {"model": Location, "serializer": LocationDetailSerializer},
    "job": {"model": Job, "serializer": JobReporteSerializer},
}


def download_report(report_id, organization_id, data: Dict):
    resp = None
    filters = {
        "created_at__date__lte": data["end_date"],
        "created_at__date__gte": data["start_date"],
    }
    qs = Report.objects.filter(id=report_id, organization__id=organization_id).first()
    if qs:
        report_name = qs.name
        column_mapping = qs.column_mapping
        if "location_id" in data and report_name != "location":
            filters["location_id"] = data["location_id"]
        elif "location_id" in data and report_name == "location":
            filters["id"] = data["location_id"]
        report_data = REPORT_TYPE[report_name]["model"].objects.filter(**filters)
        serializer_data = REPORT_TYPE[report_name]["serializer"](report_data, many=True).data
        df = pd.DataFrame(serializer_data)
        df.rename(columns=column_mapping, inplace=True)
        byte_obj = BytesIO()

        if data["report_type"] == "csv":
            df.to_csv(byte_obj, index=False)
            byte_obj.seek(0)
            resp = FileResponse(byte_obj, content_type="text/csv")
            resp[
                "Content-Disposition"
            ] = f'attachment; filename="{report_name}_{datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}.csv"'
        elif data["report_type"] == "excel":
            df.to_excel(byte_obj, index=False)
            byte_obj.seek(0)
            resp = FileResponse(byte_obj, content_type="text/xlsx")
            resp[
                "Content-Disposition"
            ] = f'attachment; filename="{report_name}_{datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}.xlsx"'
    return resp


def download_task_report(task_id, data: Dict):
    task_report = Task.objects.filter(id=task_id)
    report_type = data["report_type"]
    resp = None
    if task_report:
        data = task_report.values(
            "name",
            "job__name",
            "status",
            "completed_at",
            "form_submission_data",
            "start_at",
            "end_at",
        ).first()
        existing_columns = list(data.keys())
        columns = {field: (field).replace("_", " ").title() for field in existing_columns}
        task_df = pd.DataFrame(data, index=range(1))
        task_df["taskname"] = task_df["name"]
        fields_df = pd.DataFrame(data["form_submission_data"]["fields"])
        fields_df["value"] = fields_df["value"].apply(lambda x: x[0].get("value"))
        data = fields_df["label"]
        for i in data:
            task_df[i] = fields_df["value"]

        task_df.drop(["name"], axis=1, inplace=True)
        task_df.drop(["form_submission_data"], axis=1, inplace=True)

        if task_df["completed_at"].any():
            task_df["completed_at"] = task_df["completed_at"].apply(
                lambda a: pd.to_datetime(a).to_datetime64()
            )

        if task_df["start_at"].any():
            task_df["start_at"] = task_df["start_at"].apply(
                lambda a: pd.to_datetime(a).to_datetime64()
            )

        if task_df["end_at"].any():
            task_df["end_at"] = task_df["end_at"].apply(lambda a: pd.to_datetime(a).to_datetime64())

        task_df.columns = task_df.columns.str.removeprefix("form_submission_data.")
        task_df.rename(columns=columns, inplace=True)

        byte_obj = BytesIO()
        if report_type == "csv":
            task_df.to_csv(byte_obj, index=False)
            byte_obj.seek(0)
            resp = FileResponse(byte_obj, content_type="text/csv")
            resp[
                "Content-Disposition"
            ] = f'attachment; filename="task_{datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}.csv"'
        elif report_type == "excel":
            task_df.to_excel(byte_obj, index=False)
            byte_obj.seek(0)
            resp = FileResponse(byte_obj, content_type="text/xlsx")
            resp[
                "Content-Disposition"
            ] = f'attachment; filename="task_{datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}.xlsx"'
    return resp

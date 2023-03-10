import json

from soteria.atms.models.asset import Asset
from soteria.atms.models.job import Job
from soteria.models import Organization, Report
from soteria.orgs.models.location import Location


def get_field_mapping(model):
    return {field.name: (field.name).replace("_", " ").title() for field in model._meta.fields}


def create_report_templates(tenant_id):
    asset_column_mapping = get_field_mapping(Asset)
    location_column_mapping = get_field_mapping(Location)
    job_column_mapping = get_field_mapping(Job)

    # adding manually for foreign key data columns
    asset_column_mapping.update({"asset_name": "Asset Name", "location_name": "Location Name", "location_address": "Location Address", "asset_description": "Asset Description"})
    location_column_mapping.update({"organiztion_name": "Organiztion Name"})
    job_column_mapping.update({"location_name": "Location Name", "location_address": "Location Address", "asset_name": "Asset Name", "form_name": "Form Name", "job_type_name": "Job Type Name"})
    data = [
        {"name": "asset", "column_mapping": asset_column_mapping, "included_columns": asset_column_mapping.keys()},
        {"name": "location", "column_mapping": location_column_mapping, "included_columns": location_column_mapping.keys()},
        {"name": "job", "column_mapping": job_column_mapping, "included_columns": job_column_mapping.keys()},
    ]

    objects = []
    for i in data:
        report_template = Report.objects.filter(name=i["name"], organization=tenant_id).first()
        if not report_template:
            orgnization = Organization.objects.get(id=tenant_id)
            objects.append(Report(name=i["name"], organization=orgnization, column_mapping=i["column_mapping"], included_columns=json.dumps(list(i["included_columns"]))))
    if objects:
        Report.objects.bulk_create(objects)

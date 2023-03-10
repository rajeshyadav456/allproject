from django.urls import path

from soteria.atms.views.asset import AssetListCreateAPI
from soteria.atms.views.asset_details import AssetDetailGetUpdateDeleteAPI
from soteria.atms.views.asset_image import AssetImageUploadAPI
from soteria.atms.views.asset_type import AssetTypeListCreateAPI
from soteria.atms.views.asset_type_detail import AssetTypeDetailGetUpdateDeleteAPI
from soteria.atms.views.floor import FloorListAPI
from soteria.atms.views.form import FormSchemaListCreateAPI
from soteria.atms.views.form_detail import FormSchemaGetUpdateDeleteAPI
from soteria.atms.views.form_image import FormImageUploadAPI
from soteria.atms.views.job import JobListCreateAPI
from soteria.atms.views.job_details import JobDetailGetUpdateDeleteAPI
from soteria.atms.views.task import TaskListAPI
from soteria.atms.views.task_detail import TaskDetailAPI

urlpatterns = [
    path("api/v1/asset-types/", AssetTypeListCreateAPI.as_view(), name="asset-types"),
    path(
        "api/v1/asset-types/<uuid:asset_type_id>/",
        AssetTypeDetailGetUpdateDeleteAPI.as_view(),
        name="asset-types-detail",
    ),
    path("api/v1/assets/", AssetListCreateAPI.as_view(), name="assets"),
    path("api/v1/assets/image/", AssetImageUploadAPI.as_view(), name="assets-image"),
    path(
        "api/v1/assets/<uuid:asset_id>/",
        AssetDetailGetUpdateDeleteAPI.as_view(),
        name="asset-details",
    ),
    path(
        "api/v1/forms/",
        FormSchemaListCreateAPI.as_view(),
        name="forms",
    ),
    path(
        "api/v1/forms/<uuid:form_id>/",
        FormSchemaGetUpdateDeleteAPI.as_view(),
        name="form-details",
    ),
    path(
        "api/v1/forms/image/",
        FormImageUploadAPI.as_view(),
        name="form-image-upload",
    ),
    path(
        "api/v1/jobs/",
        JobListCreateAPI.as_view(),
        name="jobs",
    ),
    path(
        "api/v1/jobs/<uuid:job_id>/",
        JobDetailGetUpdateDeleteAPI.as_view(),
        name="job-details,",
    ),
    path("api/v1/floors/", FloorListAPI.as_view(), name="floor"),
    path("api/v1/dashboard/tasks/", TaskListAPI.as_view(), name="task-list"),
    path("api/v1/dashboard/tasks/<uuid:task_id>/", TaskDetailAPI.as_view(), name="task-detail"),
]

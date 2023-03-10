from django.urls import path

from soteria.staff.views.asset_qr import AssetQRDataAPI
from soteria.staff.views.asset_tasks import AssetTaskListAPI
from soteria.staff.views.task import TaskListAPI
from soteria.staff.views.task_detail import TaskDetailAPI
from soteria.staff.views.task_form_submit import TaskFormSubmitAPI

urlpatterns = [
    path("api/v1/tasks/", TaskListAPI.as_view(), name="tasks-list"),
    path("api/v1/tasks/<uuid:task_id>/", TaskDetailAPI.as_view(), name="task-details"),
    path(
        "api/v1/tasks/<uuid:task_id>/submit-form/",
        TaskFormSubmitAPI.as_view(),
        name="task-form-submit",
    ),
    path(
        "api/v1/assets/qr/",
        AssetQRDataAPI.as_view(),
        name="asset-qr-data",
    ),
    path(
        "api/v1/assets/<uuid:asset_id>/tasks/", AssetTaskListAPI.as_view(), name="assets-task-list"
    ),
]

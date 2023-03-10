from django.contrib import admin

from soteria.admin import DEFAULT_READONLY_FIELDS
from soteria.atms.models import Asset, AssetType, Floor, Form, Job, JobType, Task


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "created_at")
    readonly_fields = DEFAULT_READONLY_FIELDS
    search_fields = ("name",)
    ordering = ("created_at",)

    def title(self, obj):
        return f"Asset({obj.id}) : {obj.name}"


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ("title", "name", "created_at")
    readonly_fields = DEFAULT_READONLY_FIELDS
    search_fields = ("name",)

    def title(self, obj):
        return f"AssetType({obj.id}) : {obj.name}"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "job_id", "status", "name", "created_at")
    readonly_fields = DEFAULT_READONLY_FIELDS
    ordering = ("-created_at",)
    search_fields = ("name",)

    def title(self, obj):
        return f"Task({obj.id})"


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "asset_id",
        "name",
        "created_at",
    )
    ordering = ("-created_at",)
    readonly_fields = DEFAULT_READONLY_FIELDS

    def title(self, obj):
        return f"Job({obj.id}):({obj.name})"


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ("title", "name", "created_at")
    readonly_fields = DEFAULT_READONLY_FIELDS
    search_fields = ("name",)

    def title(self, obj):
        return f"JobType({obj.id}) : {obj.name}"


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    readonly_fields = DEFAULT_READONLY_FIELDS
    ordering = ("created_at",)

    def title(self, obj):
        return f"Form({obj.id} : {obj.name})"


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("title", "name", "created_at")
    readonly_fields = DEFAULT_READONLY_FIELDS
    search_fields = ("name",)

    def title(self, obj):
        return f"Floor({obj.id}) : {obj.name}"

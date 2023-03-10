from django.contrib import admin

from soteria.admin import DEFAULT_READONLY_FIELDS
from soteria.orgs.models import Location, OrganizationMember, OrganizationMemberLocation


# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "organization", "status", "created_at")
    list_display_links = ("title",)
    list_filter = ("status",)
    list_select_related = ("organization",)
    readonly_fields = DEFAULT_READONLY_FIELDS + ("organization",)
    search_fields = ("name",)

    def title(self, obj):
        return f"Location({obj.id}) : {obj.name}"


class OrganizationMemberLocationInline(admin.TabularInline):
    model = OrganizationMemberLocation
    max_num = 1
    fields = ("location",)
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(OrganizationMember)
class OrgnizationMemberAdmin(admin.ModelAdmin):
    search_fields = ("email",)
    list_display = ("title", "organization", "created_at", "role")
    readonly_fields = DEFAULT_READONLY_FIELDS + ("organization", "role")
    inlines = [OrganizationMemberLocationInline]

    def title(self, obj):
        return f"Organization Member({obj.id}) : {obj.email or obj.mobile})"

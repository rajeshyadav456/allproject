from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from soteria.models import (
    Domain,
    InvitationCode,
    Organization,
    Report,
    ResetPasswordTicket,
    User,
    UserOrganization,
)

DEFAULT_READONLY_FIELDS = (
    "created_by",
    "created_at",
    "updated_at",
    "updated_by",
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "email",
        "mobile",
        "mobile_verified",
        "email_verified",
        "date_joined",
    )
    readonly_fields = ("date_joined", "created_at", "updated_at", "updated_by")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "mobile",
                    "is_active",
                    "mobile_verified",
                    "email_verified",
                    "avatar_url",
                    "can_create_org",
                )
                + readonly_fields
            },
        ),
        (
            "Permissions options",
            {
                "classes": ("collapse",),
                "fields": ("is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
    )
    list_filter = ("is_active", "is_staff")
    search_fields = ("first_name", "last_name", "email", "mobile")

    def title(self, obj):
        return f"User({obj.id}) : {obj.username}"


@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    readonly_fields = ("user",)
    list_display = ("invitation_code", "is_used", "user")
    list_select_related = ("user",)
    add_form_template = "admin/invitation_code_add_form_template.html"

    def invitation_code(self, obj):
        return f"InvitationCode({obj.id}) : {obj.code}"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not obj:
            return readonly_fields
        return readonly_fields + ("code",)

    def has_add_permission(self, request):
        return super(admin.ModelAdmin, self).has_add_permission(request)


@admin.register(ResetPasswordTicket)
class ResetPasswordTicketAdmin(admin.ModelAdmin):
    readonly_fields = DEFAULT_READONLY_FIELDS + (
        "token",
        "expires_at",
        "user",
        "client_ip",
        "client_ua",
    )
    list_display = ("user", "expires_at", "created_at")


class DomainInLine(admin.TabularInline):
    model = Domain
    max_num = 1


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("title", "slug", "status", "created_at")
    list_display_links = ("title",)
    readonly_fields = DEFAULT_READONLY_FIELDS
    list_filter = ("status",)
    ordering = ("-id",)
    inlines = [DomainInLine]

    def title(self, obj):
        return f"Organization({obj.id}) : {obj.name}"


@admin.register(UserOrganization)
class UserOrganizationAdmin(admin.ModelAdmin):
    list_display = ("title",)
    readonly_fields = ("organization", "user")

    def title(self, obj):
        return f"UserOrganization({obj.id} : {obj.organization})"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("name",)
    readonly_fields = ("name", "organization")

    def title(self, obj):
        return f"Report({obj.id} : {obj.organization})"

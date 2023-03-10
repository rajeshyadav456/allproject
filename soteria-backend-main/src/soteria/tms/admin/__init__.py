from django.contrib import admin

from soteria.admin import DEFAULT_READONLY_FIELDS
from soteria.tms.models.ticket import Priority, Ticket, TicketActivity, TicketLabel, TicketType


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    readonly_fields = DEFAULT_READONLY_FIELDS
    search_fields = ("name",)
    ordering = ("created_at",)

    def title(self, obj):
        return f"TicketType({obj.id}):{obj.name}"


@admin.register(TicketLabel)
class TicketLabelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    readonly_fields = DEFAULT_READONLY_FIELDS
    search_fiedls = ("name",)
    ordering = ("created_at",)

    def title(self, obj):
        return f"TicketLabel({obj.id}):{obj.name}"


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    readonly_fields = DEFAULT_READONLY_FIELDS
    search_fields = ("name",)
    ordering = ("created_at",)

    def title(self, obj):
        return f"Priority({obj.id}): {obj.name}"


@admin.register(TicketActivity)
class TicketAcitivityAdmin(admin.ModelAdmin):
    list_display = ("ticket", "activity", "created_at")
    readonly_fields = DEFAULT_READONLY_FIELDS
    search_fields = ("name",)
    ordering = ("created_at",)

    def title(self, obj):
        return f"TicketActivity({obj.id}) : {obj.name}"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_diplay = ("name",)
    readonly_fields = DEFAULT_READONLY_FIELDS
    search_fields = ("name", "assign_to", "assing_by", "location")
    ordering = ("created_at",)

    def title(self, obj):
        return f"Ticket({self.id}):{self.name}"

from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "room",
        "check_in",
        "check_out",
        "guests",
        "created_at",
    )

    list_filter = (
        "room",
        "check_in",
        "check_out",
    )

    search_fields = (
        "full_name",
        "email",
        "phone",
    )

    readonly_fields = ("created_at",)

    ordering = ("-created_at",)

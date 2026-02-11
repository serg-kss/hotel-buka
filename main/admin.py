from django.contrib import admin
from .models import SiteSettings, SocialMedia, BookingRequest, RoomImage, Room, Amenity
from .admin_mixins import SingletonAdmin


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    pass


@admin.register(SocialMedia)
class SocialMediaAdmin(SingletonAdmin):
    pass


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "room",
        "check_in",
        "check_out",
        "status",
        "created_at",
    )
    list_filter = ("status", "room")
    search_fields = ("full_name", "email", "phone")


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "room_name_uk",
        "price",
        "capacity",
        "is_active",
        "order",
    )

    list_filter = ("is_active", "capacity")
    search_fields = ("room_name_uk", "room_name_en")
    prepopulated_fields = {"slug": ("room_name_en",)}

    inlines = [RoomImageInline]

    filter_horizontal = ("amenities",)

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = ("name_uk", "name_en", "icon_class")
    search_fields = ("name_uk", "name_en")
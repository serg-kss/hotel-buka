from django.contrib import admin
from .models import SiteSettings, SocialMedia, RoomImage, Room, Amenity, ContactMessages
from .admin_mixins import SingletonAdmin


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    pass


@admin.register(SocialMedia)
class SocialMediaAdmin(SingletonAdmin):
    pass

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


@admin.register(ContactMessages)
class ContactMessagesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
    )
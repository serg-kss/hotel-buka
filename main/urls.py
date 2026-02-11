from django.urls import path
from main import views
from .views import RoomListView


app_name = 'main'

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("rooms/", RoomListView.as_view(), name="rooms"),
    path("amenities/", views.amenities, name="amenities"),
    path("location/", views.location, name="location"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
    path("gallery/", views.gallery, name="gallery"),
    path("contact/", views.contact, name="contact"),
]
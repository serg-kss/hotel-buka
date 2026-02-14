from django.urls import path
from main import views
from .views import RoomListView, RoomDetailView, Contact, MainPageView


app_name = 'main'

urlpatterns = [
    path("", MainPageView.as_view(), name="index"),
    path("сottages/", RoomListView.as_view(), name="rooms"),
    path("сottages/<slug:slug>/", RoomDetailView.as_view(), name="room"),
    path("amenities/", views.amenities, name="amenities"),
    path("location/", views.location, name="location"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
    path("gallery/", views.gallery, name="gallery"),
    path("contact/", Contact.as_view(), name="contact"),
]
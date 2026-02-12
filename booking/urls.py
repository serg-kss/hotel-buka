from django.urls import path
from booking import views


app_name = 'booking'

urlpatterns = [
    path("booking/<slug:slug>/", views.BookingView.as_view(), name="booking"),
     path("success/", views.BookingSuccessView.as_view(), name="booking_success"),
]
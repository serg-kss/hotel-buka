from django.urls import path
from booking import views


app_name = 'booking'

urlpatterns = [
    path("booking/", views.booking, name="booking"),
]
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Room
from booking.models import Booking
from django.views.generic import DetailView


class BookingView(View):

    def get(self, request, slug):
        room = get_object_or_404(Room, slug=slug, is_active=True)
        return render(request, "booking/booking.html", {"room": room})

    def post(self, request, slug):
        room = get_object_or_404(Room, slug=slug, is_active=True)

        booking = Booking.objects.create(
            room=room,
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            check_in=request.POST.get("check_in"),
            check_out=request.POST.get("check_out"),
            guests=request.POST.get("guests"),
            message=request.POST.get("message"),
        )

        return redirect("booking:booking_success", pk=booking.pk)



class BookingSuccessView(DetailView):
    model = Booking
    template_name = "booking/booking_success.html"
    context_object_name = "booking"
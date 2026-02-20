from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Room
from booking.models import Booking
from django.views.generic import DetailView
from .forms import BookingForm


class BookingView(View):

    def get(self, request, slug):
        room = get_object_or_404(Room, slug=slug, is_active=True)
        form = BookingForm()

        return render(request, "booking/booking.html", {
            "room": room,
            "form_errors": None
        })

    def post(self, request, slug):
        room = get_object_or_404(Room, slug=slug, is_active=True)

        form = BookingForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            booking = Booking.objects.create(
                room=room,
                full_name=data["full_name"],
                email=data["email"],
                phone=data["phone"],
                check_in=data["check_in"],
                check_out=data["check_out"],
                guests=data["guests"],
                message=data.get("message", "")
            )

            return redirect("booking:booking_success", pk=booking.pk)

        # если есть ошибки — возвращаем их в шаблон
        return render(request, "booking/booking.html", {
            "room": room,
            "form_errors": form.errors
        })


class BookingSuccessView(DetailView):
    model = Booking
    template_name = "booking/booking_success.html"
    context_object_name = "booking"
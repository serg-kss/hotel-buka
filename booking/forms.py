from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            "full_name",
            "email",
            "phone",
            "check_in",
            "check_out",
            "guests",
            "message",
        ]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
        }

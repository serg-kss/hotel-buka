from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import date


class BookingForm(forms.Form):

    check_in = forms.DateField()
    check_out = forms.DateField()
    guests = forms.IntegerField(min_value=1, max_value=10)
    full_name = forms.CharField(min_length=3, max_length=100)
    email = forms.EmailField(max_length=150)
    phone = forms.CharField(min_length=8, max_length=20)
    message = forms.CharField(required=False, max_length=500)
    website = forms.CharField(required=False)  # honeypot

    # ---- ВАЛИДАЦИЯ ----

    def clean_check_in(self):
        check_in = self.cleaned_data["check_in"]
        if check_in < date.today():
            raise forms.ValidationError(
                _("Arrival date cannot be in the past.")
            )
        return check_in

    def clean(self):
        cleaned_data = super().clean()

        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        website = cleaned_data.get("website")

        # Honeypot
        if website:
            raise forms.ValidationError(_("Spam detected."))

        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError(
                    _("Departure date must be after arrival date.")
                )

        return cleaned_data

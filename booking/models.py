from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import Room

# Create your models here.
class Booking(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    check_in = models.DateField()
    check_out = models.DateField()

    guests = models.PositiveIntegerField(default=1)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = _("Бронювання")
        verbose_name_plural = _("Бронювання")

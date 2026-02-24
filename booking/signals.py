from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking


@receiver(post_save, sender=Booking)
def notify_admin_new_booking(sender, instance, created, **kwargs):
    if created:
        message = f"""
Нове бронювання!

Кімната: {instance.room.name}
Ім'я: {instance.full_name}
Email: {instance.email}
Телефон: {instance.phone}

Дата заїзду: {instance.check_in}
Дата виїзду: {instance.check_out}
Кількість гостей: {instance.guests}

Повідомлення:
{instance.message or "—"}

Створено: {instance.created_at}
        """

        send_mail(
            subject="Нове бронювання на сайті Wood Life",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["woodlife.karpatians@gmail.com"],
            fail_silently=False,
        )
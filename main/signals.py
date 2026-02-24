from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessages


@receiver(post_save, sender=ContactMessages)
def notify_admin_new_booking(sender, instance, created, **kwargs):
    if created:
        message = f"""
Нове повідомлення!

Ім'я: {instance.name}
Email: {instance.email}
Тема: {instance.subject}
Повідомлення: {instance.message}

Повідомлення:
{instance.message or "—"}

Створено: 
        """

        send_mail(
            subject="Нове Повідомлення на сайті Wood Life",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["woodlife.karpatians@gmail.com"],
            fail_silently=False,
        )
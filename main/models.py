from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import translation


class Room(models.Model):

    # --- Название ---
    room_name_uk = models.CharField(_("Назва номера (укр)"), max_length=200)
    room_name_en = models.CharField(_("Назва номера (англ)"), max_length=200)

    # --- Описание ---
    description_uk = models.TextField(_("Опис (укр)"))
    description_en = models.TextField(_("Опис (англ)"))

    @property
    def name(self):
        lang = translation.get_language()
        if lang == "uk":
            return self.room_name_uk
        return self.room_name_en

    @property
    def description(self):
        lang = translation.get_language()
        if lang == "uk":
            return self.description_uk
        return self.description_en

    # --- Цена ---
    price = models.DecimalField(_("Ціна"), max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(_("Знижка (%)"), default=0)

    # --- Площадь ---
    square = models.PositiveIntegerField(_("Площа (м²)"))

    # --- Вместимость ---
    capacity = models.PositiveIntegerField(_("Кількість гостей"), default=2)

    # --- Главное изображение ---
    main_image = models.ImageField(
        _("Головне фото"),
        upload_to="rooms/main/",
        blank=True,
        null=True
    )

    # --- Удобства ---
    amenities = models.ManyToManyField(
        "Amenity",
        verbose_name=_("Зручності"),
        blank=True
    )

    # --- SEO ---
    slug = models.SlugField(unique=True, blank=True)

    # --- Активность ---
    is_active = models.BooleanField(_("Активний"), default=True)

    # --- Сортировка ---
    order = models.PositiveIntegerField(default=0)

    # --- Даты ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.room_name_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.room_name_uk

    class Meta:
        verbose_name = _("Номер")
        verbose_name_plural = _("Номери")
        ordering = ["order"]

class RoomImage(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        _("Фото"),
        upload_to="rooms/gallery/"
    )

    def __str__(self):
        return f"{self.room.room_name_uk} image"

    class Meta:
        verbose_name = _("Фото номера")
        verbose_name_plural = _("Фото номерів")


class Amenity(models.Model):

    name_uk = models.CharField(_("Назва (укр)"), max_length=100)
    name_en = models.CharField(_("Назва (англ)"), max_length=100)

    @property
    def name(self):
        lang = translation.get_language()
        if lang == "uk":
            return self.name_uk
        return self.name_en


    icon_class = models.CharField(
        _("CSS іконка (bi class)"),
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.name_uk

    class Meta:
        verbose_name = _("Зручність")
        verbose_name_plural = _("Зручності")

class ContactMessages(models.Model):

    name = models.CharField(_("Client's name"), max_length=20)
    email = models.EmailField("Email")
    subject = models.CharField(_("Subject"), max_length=200)
    message = models.TextField(_("Message"))

    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name = _("Повідомлення")
        verbose_name_plural = _("Повідомлення")

class SiteSettings(models.Model):

    address_uk = models.TextField(_("Address (Ukrainian)"))
    address_en = models.TextField(_("Address (English)"))

    city_uk = models.TextField(_("City (Ukrainian)"), blank=True)
    city_en = models.TextField(_("City (English)"), blank=True)

    phone = models.CharField(_("Phone"), max_length=50)
    email = models.EmailField(_("Email"))

    check_in = models.CharField(_("Check-in time"), max_length=50, blank=True)
    check_out = models.CharField(_("Check-out time"), max_length=50, blank=True)

    google_maps_url = models.TextField(_("Google Maps link"), blank=True)

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")


class SocialMedia(models.Model):

    twitter = models.CharField("Twitter (X)", max_length=100, blank=True)
    instagram = models.CharField("Instagram", max_length=100, blank=True)
    facebook = models.CharField("Facebook", max_length=100, blank=True)
    linkedin = models.CharField("Linked In", max_length=100, blank=True)

    def __str__(self):
        return "Social Media"

    class Meta:
        verbose_name = _("Social Media")
        verbose_name_plural = _("Social Media")
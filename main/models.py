from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import translation


class HomeSEO(models.Model):

    # Ukrainian
    title_uk = models.CharField("Title (UK)", max_length=255, blank=True)
    description_uk = models.TextField("Description (UK)", blank=True)

    # English
    title_en = models.CharField("Title (EN)", max_length=255, blank=True)
    description_en = models.TextField("Description (EN)", blank=True)

    og_image = models.ImageField("OG Image", upload_to="seo/", blank=True)

    def __str__(self):
        return "SEO"


class Testimonials(models.Model):
    name_uk = models.CharField(_("Name"), max_length=30, default="")
    message_uk = models.TextField(_("Message"), default="")

    name_en = models.CharField(_("Name_en"), max_length=30, default="")
    message_en = models.TextField(_("Message_en"), default="")

    @property
    def name(self):
        lang = translation.get_language()
        if lang == "uk":
            return self.name_uk
        return self.name_en

    @property
    def message(self):
        lang = translation.get_language()
        if lang == "uk":
            return self.message_uk
        return self.message_en

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Коментар")
        verbose_name_plural = _("Коментарі")


class Room(models.Model):

    room_name_uk = models.CharField(_("Назва котеджу (укр)"), max_length=200)
    room_name_en = models.CharField(_("Назва котеджу (англ)"), max_length=200)

    description_uk = models.TextField(_("Опис (укр)"))
    description_en = models.TextField(_("Опис (англ)"))

    sub_title_uk = models.CharField(_("Текст під назвою (укр)"), max_length=200, default='')
    sub_title_en = models.CharField(_("Текст під назвою (англ)"), max_length=200, default='')

    lable_capacity_uk = models.CharField(_("Кількіть людей прописом (укр)"), max_length=100, default='')
    lable_capacity_en = models.CharField(_("Кількіть людей прописом (англ)"), max_length=100, default='')

    comment_uk = models.TextField(_("Коментар (укр)"), default='')
    comment_en = models.TextField(_("Коментар (англ)"), default='')

    comment_name_uk = models.CharField(_("Коментар Імʼя (укр)"), max_length=100, default='')
    comment_name_en = models.CharField(_("Коментар Імʼя (англ)"), max_length=100, default='')

    pets_uk = models.CharField(_("Тварини (укр)"), max_length=100, default='')
    pets_en = models.CharField(_("Тварини (англ)"), max_length=100, default='')

    housekeeping_uk = models.CharField(_("Прибирання в котеджі (укр)"), max_length=100, default='')
    housekeeping_en = models.CharField(_("Прибирання в котеджі (англ)"), max_length=100, default='')

    def get_translated_field(self, field_base):
        lang = translation.get_language()
        field_name = f"{field_base}_{lang}"
        return getattr(self, field_name, "")
    
    @property
    def housekeeping(self):
        return self.get_translated_field("housekeeping")        

    @property
    def pets(self):
        return self.get_translated_field("pets")

    @property
    def comment_name(self):
        return self.get_translated_field("comment_name")

    @property
    def comment(self):
        return self.get_translated_field("comment")

    @property
    def lable_capacity(self):
        return self.get_translated_field("lable_capacity")

    @property
    def sub_title(self):
        return self.get_translated_field("sub_title")

    @property
    def name(self):
        return self.get_translated_field("room_name")

    @property
    def description(self):
        return self.get_translated_field("description")


    # --- Цена ---
    price = models.DecimalField(_("Ціна"), max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(_("Знижка (%)"), default=0)

    # --- Площадь ---
    square = models.PositiveIntegerField(_("Площа (м²)"))

    # --- Вместимость ---
    capacity = models.PositiveIntegerField(_("Кількість гостей"), default=2)

    has_generator = models.BooleanField(
        _("Наявність генератора"),
        default=False
    )

    # --- Главное изображение ---
    main_image = models.ImageField(
        _("Головне фото"),
        upload_to="hotel/",
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
        verbose_name = _("Котедж")
        verbose_name_plural = _("Котеджі")
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
        verbose_name = _("Фото котеджу")
        verbose_name_plural = _("Фото котеджів")


class Amenity(models.Model):

    class Category(models.TextChoices):
        SLEEPING = "sleeping", _("Sleeping")
        TECHNOLOGY = "technology", _("Technology")
        COMFORT = "comfort", _("Comfort")
        BATHROOM = "bathroom", _("Bathroom")

    name_uk = models.CharField(_("Назва (укр)"), max_length=100)
    name_en = models.CharField(_("Назва (англ)"), max_length=100)

    category = models.CharField(
        _("Категорія"),
        max_length=20,
        choices=Category.choices,
        default=Category.COMFORT
    )

    icon_class = models.CharField(
        _("CSS іконка (bi class)"),
        max_length=100,
        blank=True
    )

    @property
    def name(self):
        lang = translation.get_language()
        if lang == "uk":
            return self.name_uk
        return self.name_en

    def __str__(self):
        return f"{self.name_uk} ({self.get_category_display()})"

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
        verbose_name = _("Настройка сайту")
        verbose_name_plural = _("Настройки сайту")


class SocialMedia(models.Model):

    twitter = models.CharField("Twitter (X)", max_length=150, blank=True, default="")
    instagram = models.CharField("Instagram", max_length=150, blank=True, default="")
    facebook = models.CharField("Facebook", max_length=150, blank=True, default="")
    linkedin = models.CharField("Linked In", max_length=150, blank=True, default="")
    youtube = models.CharField("YouTube", max_length=200, blank=True, default="")

    def __str__(self):
        return "Соц-мережі"

    class Meta:
        verbose_name = _("Соц-мережі")
        verbose_name_plural = _("Соц-мережі")


class GalleryMainPage(models.Model):
    img = models.ImageField(
        _("Фото"),
        upload_to="gal/main/",
        blank=True,
        null=True
    )
    alt_uk = models.CharField(_("Опис (укр)"), max_length=100, default="Фото Wood Life")
    alt_en = models.CharField(_("Опис (en)"), max_length=100, default="Photo Wood Life")
    class Meta:
        verbose_name = _("Фото головна сторінка")
        verbose_name_plural = _("Фото головна сторінка")

    def __str__(self):
        return f"Фото #{self.id}"
    
    
class GalleryPage(models.Model):
    class Category(models.TextChoices):
        ROOMS = "rooms", _("Rooms")
        AMENITIES = "amenities", _("Amenities")
        INTERIOR = "interior", _("Interior")
        EXTERIOR = "exterior", _("Exterior")

    img = models.ImageField(
        _("Фото"),
        upload_to="gal/gal/",
        blank=True,
        null=True
    )

    category = models.CharField(
        _("Категорія"),
        max_length=20,
        choices=Category.choices,
        default=Category.ROOMS
    )   

    alt_uk = models.CharField(_("Опис (укр)"), max_length=100, default="Фото Wood Life")
    alt_en = models.CharField(_("Опис (en)"), max_length=100, default="Photo Wood Life")
    class Meta:
        verbose_name = _("Фото галерея")
        verbose_name_plural = _("Фото галерея")

    def __str__(self):
        return f"Фото #{self.id}"
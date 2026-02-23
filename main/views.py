import random
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from .models import Room, ContactMessages, Testimonials, GalleryMainPage, GalleryPage
from django.db import DatabaseError
from collections import defaultdict
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


@method_decorator(cache_page(60 * 30), name="dispatch")
class MainPageView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            rooms = []
            testimonials = Testimonials.objects.all()
            photo = GalleryMainPage.objects.all()
            rooms_qs = Room.objects.all()
            count = rooms_qs.count()
            if count > 3:
                random_indexes = random.sample(range(count), 3)
                rooms = [rooms_qs[i] for i in random_indexes]
            else:
                rooms = rooms_qs
        except DatabaseError:
            testimonials = []
            photo = []
            rooms = []

        context["testimonials"] = testimonials
        context["photo"] = photo
        context["rooms"] = rooms
        context["count"] = count
        return context


@method_decorator(cache_page(60 * 30), name="dispatch")
class RoomListView(ListView):
    model = Room
    template_name = "main/rooms.html"
    context_object_name = "rooms"

    def get_queryset(self):
        queryset = (
            Room.objects
            .filter(is_active=True)
            .prefetch_related("amenities")
        )

        # --- ФИЛЬТР ПО ЦЕНЕ ---
        price = self.request.GET.get("price")

        if price == "100-200":
            queryset = queryset.filter(price__gte=100, price__lte=200)
        elif price == "200-350":
            queryset = queryset.filter(price__gte=200, price__lte=350)
        elif price == "350+":
            queryset = queryset.filter(price__gte=350)

        # --- ФИЛЬТР ПО КОЛ-ВУ ГОСТЕЙ ---
        capacity = self.request.GET.get("capacity")

        if capacity == "1-2":
            queryset = queryset.filter(capacity__gte=1, capacity__lte=2)
        elif capacity == "3-4":
            queryset = queryset.filter(capacity__gte=3, capacity__lte=4)
        elif capacity == "5+":
            queryset = queryset.filter(capacity__gte=5)

        # --- СОРТИРОВКА ---
        sort = self.request.GET.get("sort")

        if sort == "price_asc":
            queryset = queryset.order_by("price")
        elif sort == "price_desc":
            queryset = queryset.order_by("-price")
        elif sort == "size":
            queryset = queryset.order_by("-square")
        else:
            queryset = queryset.order_by("order")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        total_rooms = queryset.count()
        limit = int(self.request.GET.get("limit", 6))

        context["rooms"] = queryset[:limit]
        context["limit"] = limit
        context["total_rooms"] = total_rooms
        context["has_more"] = limit < total_rooms

        # чтобы select сохраняли выбранные значения
        context["current_price"] = self.request.GET.get("price", "")
        context["current_capacity"] = self.request.GET.get("capacity", "")
        context["current_sort"] = self.request.GET.get("sort", "")

        return context


class RoomDetailView(DetailView):
    model = Room
    template_name = "main/room.html"
    context_object_name = "room"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object

        grouped_amenities = defaultdict(list)

        for amenity in room.amenities.all():
            grouped_amenities[amenity.category].append(amenity)

        context["grouped_amenities"] = dict(grouped_amenities)

        return context

@vary_on_headers("Accept-Language")
@cache_page(60 * 30)
def amenities(request):
    return render(request, 'main/amenities.html')


@vary_on_headers("Accept-Language")
@cache_page(60 * 30)
def location(request):
    return render(request, 'main/location.html')


@vary_on_headers("Accept-Language")
@cache_page(60 * 30)
def terms(request):
    return render(request, 'main/terms.html')


@vary_on_headers("Accept-Language")
@cache_page(60 * 30)
def privacy(request):
    return render(request, 'main/privacy.html')


@method_decorator(cache_page(60 * 30), name="dispatch")
class GalleryView(TemplateView):
    template_name = "main/gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            photo = GalleryPage.objects.all()
            total_photo = photo.count()
            limit = int(self.request.GET.get("limit", 9))
        except DatabaseError:
            photo = []
        

        context["photo"] = photo[:limit]
        context["limit"] = limit
        context["total_rooms"] = total_photo
        context["has_more"] = limit < total_photo
        return context
class Contact(View):

    def get(self, request):
        return render(request, "main/contact.html")
    
    def post(self, request):
        ContactMessages.objects.create(
            name = request.POST.get("name"),
            email = request.POST.get("email"),
            subject = request.POST.get("subject"),
            message = request.POST.get("message")
        )
        messages.success(request, _("Message sent successfully! Thank you 🙌"))
        return redirect("main:index")
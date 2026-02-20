from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils.translation import activate
from django.conf import settings
from .models import Room


class MultilingualSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def get_languages(self):
        return [lang[0] for lang in settings.LANGUAGES]

    def alternates(self, obj):
        alternates = []
        for lang in self.get_languages():
            activate(lang)
            alternates.append({
                "location": self.location(obj),
                "lang_code": lang
            })
        return alternates


class StaticViewSitemap(MultilingualSitemap):

    def items(self):
        return ["main:index", "main:location", "main:rooms"]

    def location(self, item):
        return reverse(item)


class RoomSitemap(MultilingualSitemap):

    priority = 0.7

    def items(self):
        return Room.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

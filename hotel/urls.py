from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.views.i18n import set_language
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import get_language_from_request
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import StaticViewSitemap, RoomSitemap


def root_redirect(request):
    lang = get_language_from_request(request)
    if lang not in dict(settings.LANGUAGES):
        lang = settings.LANGUAGE_CODE
    return redirect(f"/{lang}/", permanent=True)


sitemaps = {
    "static": StaticViewSitemap,
    "rooms": RoomSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),
    path("", root_redirect),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
        ),
    ),
]


urlpatterns += i18n_patterns(
    path("", include(("main.urls", "main"), namespace="main")),
    path("", include(("booking.urls", "booking"), namespace="booking")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps, "template_name": "sitemap.xml",}, name="django.contrib.sitemaps.views.sitemap"),

    prefix_default_language=True,
)

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)


#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

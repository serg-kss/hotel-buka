from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.utils.translation import get_language_from_request
from django.shortcuts import redirect
from django.views.i18n import set_language
from django.views.static import serve


def root_redirect(request):
    lang = get_language_from_request(request)
    if lang not in dict(settings.LANGUAGES):
        lang = settings.LANGUAGE_CODE
    return redirect(f"/{lang}/", permanent=True)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
    ),
]

urlpatterns += i18n_patterns(
    path("", include(("main.urls", "main"), namespace="main")),
    path("", include(("booking.urls", "booking"), namespace="booking")),
    prefix_default_language=True,
)

# редирект корня
urlpatterns += [
    path("", root_redirect),
]

# 🔥 КОСТЫЛЬ ДЛЯ MEDIA (в самом конце!)
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {
        "document_root": settings.MEDIA_ROOT,
    }),
]
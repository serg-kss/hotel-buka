from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.views.i18n import set_language
from django.utils.translation import get_language


def root_redirect(request):
    lang = get_language() or "en"
    return redirect(f"/{lang}/")


urlpatterns = [
    path("", root_redirect),
    path("admin/", admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),
]

urlpatterns += i18n_patterns(
    path("", include(("main.urls", "main"), namespace="main")),
    path("", include(("booking.urls", "booking"), namespace="booking")),
    prefix_default_language=True,
)
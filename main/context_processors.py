from django.utils import translation
from .models import SiteSettings, SocialMedia


def site_settings(request):
    settings = SiteSettings.objects.first()
    social = SocialMedia.objects.first()

    lang = translation.get_language()

    if settings:
        if lang == "uk":
            address = settings.address_uk or ""
            city = settings.city_uk or ""
        else:
            address = settings.address_en or ""
            city = settings.city_en or ""

        site_map = settings.google_maps_url or ""
        site_phone = settings.phone or ""
        site_email = settings.email or ""
        site_check_in = settings.check_in or ""
        site_check_out = settings.check_out or ""
    else:
        address = ""
        city = ""
        site_map = ""
        site_phone = ""
        site_email = ""
        site_check_in = ""
        site_check_out = ""

    site_instagram = getattr(social, "instagram", "")
    site_facebook = getattr(social, "facebook", "")
    site_twitter = getattr(social, "twitter", "")
    site_linkedin = getattr(social, "linkedin", "")

    return {
        "site_address": address,
        "site_city": city,
        "site_map": site_map,
        "site_phone": site_phone,
        "site_email": site_email,
        "site_check_in": site_check_in,
        "site_check_out": site_check_out,
        "site_instagram": site_instagram,
        "site_facebook": site_facebook,
        "site_twitter": site_twitter,
        "site_linkedin": site_linkedin,
    }

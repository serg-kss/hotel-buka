from django.utils import translation
from .models import SiteSettings, SocialMedia, HomeSEO


def seo_context(request):
    seo = HomeSEO.objects.first()
    lang = translation.get_language()

    if seo:
        if lang == "uk":
            title = seo.title_uk
            description = seo.description_uk
        else:
            title = seo.title_en
            description = seo.description_en

        og_image = seo.og_image.url if seo.og_image else ""
    else:
        title = "Wood Life"
        description = ""
        og_image = ""

    return {
        "seo_title": title,
        "seo_description": description,
        "seo_og_image": og_image,
    }


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
    site_youtube = getattr(social, "youtube", "")

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
        "site_youtube": site_youtube,
    }

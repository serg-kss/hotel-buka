from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def rooms(request):
    return render(request, 'main/rooms.html')

def amenities(request):
    return render(request, 'main/amenities.html')

def location(request):
    return render(request, 'main/location.html')

def terms(request):
    return render(request, 'main/terms.html')

def privacy(request):
    return render(request, 'main/privacy.html')

def gallery(request):
    return render(request, 'main/gallery.html')

def contact(request):
    return render(request, 'main/contact.html')
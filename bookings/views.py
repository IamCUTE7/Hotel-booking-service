from django.http import HttpResponse


def index(request):  # Http Response
    return HttpResponse("App page for hotel bookings")

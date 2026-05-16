from django.urls import path

from . import views

urlpatterns = [path("bookings/", views.index), path("", views.index)]

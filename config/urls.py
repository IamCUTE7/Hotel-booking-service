"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from bookings.booking_views import (
    BookingDeleteView,
    BookingListCreateView,
    BookingUpdateView,
)
from bookings.room_views import RoomDeleteView, RoomListCreateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/bookings/list/", BookingListCreateView.as_view()),
    path("api/v1/bookings/create/", BookingListCreateView.as_view()),
    path("api/v1/bookings/<int:pk>/delete/", BookingDeleteView.as_view()),
    path("api/v1/bookings/<int:pk>/update/", BookingUpdateView.as_view()),
    path("api/v1/rooms/list/", RoomListCreateView.as_view()),
    path("api/v1/rooms/create/", RoomListCreateView.as_view()),
    path("api/v1/rooms/<int:pk>/delete/", RoomDeleteView.as_view()),
]

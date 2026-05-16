from rest_framework import serializers

from bookings.models import Booking, Room


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class BookingUpdateSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

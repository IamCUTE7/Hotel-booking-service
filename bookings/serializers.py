from rest_framework import serializers

from bookings.models import Booking


class BookingModel:
    def __init__(self, id, room):
        self.id = id
        self.room = room


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    # id = serializers.IntegerField(read_only=True)
    # room = serializers.CharField(max_length=50)
    # start_date = serializers.DateField()
    # end_date = serializers.DateField()

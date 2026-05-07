from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking
from .serializers import BookingSerializer


class BookingCreateView(APIView):
    def get(self, request):
        objects = Booking.objects.all()
        serializer = BookingSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_post = Booking.objects.create(
            room=request.data["room"], start_date=request.data["start_date"], end_date=request.data["end_date"]
        )

        return Response({"post": BookingSerializer(new_post).data})

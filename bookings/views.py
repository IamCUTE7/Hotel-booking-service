from loguru import logger
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer
from .services.booking_service import create_booking


class BookingListCreateView(APIView):
    def get(self, request):
        room_id = request.query_params.get("room_id")

        if room_id is None:
            logger.warning("Booking list failed: room_id is missing")
            return Response({"error": "room_id is required"}, status=400)

        bookings = Booking.objects.filter(room_id=room_id).order_by("start_date")
        serializer = BookingSerializer(bookings, many=True)

        logger.info("Booking list returned: room_id={}, count={}", room_id, len(serializer.data))

        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = create_booking(
                room_id=serializer.validated_data["room"].id,
                start_date=serializer.validated_data["start_date"],
                end_date=serializer.validated_data["end_date"],
            )
        except ValueError as error:
            logger.warning("Booking creation failed: error={}", error)
            return Response({"error": str(error)}, status=400)

        logger.info("Booking created via API: booking_id={}", booking.id)

        return Response({"booking_id": booking.id})


class BookingDeleteView(APIView):
    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            logger.warning("Booking deletion failed: booking_id={} not found", pk)
            return Response({"error": "object does not exist"}, status=404)

        booking.delete()

        logger.info("Booking deleted via API: booking_id={}", pk)

        return Response({"booking_id": pk, "status": "deleted"})


class BookingUpdateView(APIView):
    def put(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            logger.warning("Booking update failed: booking_id={}", pk)
            return Response({"error": "object does not exist"}, status=404)

        serializer = BookingSerializer(instance=booking, data=request.data)

        serializer.is_valid(raise_exception=True)
        updated_booking = serializer.save()

        logger.info("Booking updated via API: booking_id={}", pk)

        return Response(BookingSerializer(updated_booking).data)


class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all()

        sort = self.request.query_params.get("sort")
        order = self.request.query_params.get("order", "asc")

        allowed_sort_fields = {
            "price": "price_per_night",
            "created_at": "created_at",
        }

        if sort in allowed_sort_fields:
            order_prefix = "-" if order == "desc" else ""
            queryset = queryset.order_by(f"{order_prefix}{allowed_sort_fields[sort]}")

        return queryset


class RoomDeleteView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def destroy(self, request, *args, **kwargs):
        room = self.get_object()
        room_id = room.id
        room.delete()

        logger.info("Room deleted via API: room_id={}", room_id)

        return Response({"room_id": room_id, "status": "deleted"})

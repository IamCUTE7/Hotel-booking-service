from loguru import logger
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BookingSerializer, BookingUpdateSerializer
from .services.booking_service import booking_service


class BookingListCreateView(APIView):
    def get(self, request):
        room_id = request.query_params.get("room_id")

        if not room_id:
            logger.warning("Booking list failed: room_id is missing")
            return Response({"error": "room_id is required"}, status=400)

        bookings = booking_service.get_bookings_by_room_id(room_id)
        serializer = BookingSerializer(bookings, many=True)

        logger.info("Booking list returned: room_id={}, count={}", room_id, len(serializer.data))

        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = booking_service.create_booking(
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
            booking_service.delete_booking(pk)
        except ValueError as error:
            logger.warning("Booking deletion failed: booking_id={}, error={}", pk, error)
            return Response({"error": "object does not exist"}, status=404)

        logger.info("Booking deleted via API: booking_id={}", pk)

        return Response({"booking_id": pk, "status": "deleted"})


class BookingUpdateView(APIView):
    def put(self, request, pk):
        serializer = BookingUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            updated_booking = booking_service.update_booking(
                booking_id=pk,
                start_date=serializer.validated_data["start_date"],
                end_date=serializer.validated_data["end_date"],
            )
        except ValueError as error:
            logger.warning("Booking update failed: booking_id={}, error={}", pk, error)

            return Response({"error": str(error)}, status=400)

        logger.info("Booking updated via API: booking_id={}", pk)

        return Response(BookingSerializer(updated_booking).data)

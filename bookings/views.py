from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer


class BookingListCreateView(APIView):
    def get(self, request):
        objects = Booking.objects.all()
        serializer = BookingSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"booking_id": serializer.instance.id})


class BookingDeleteView(APIView):
    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({"error": "object does not exist"}, status=404)

        booking.delete()

        return Response({"booking_id": pk, "status": "deleted"})


class BookingUpdateView(APIView):
    def put(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({"error": "object does not exist"}, status=404)

        serializer = BookingSerializer(instance=booking, data=request.data)

        serializer.is_valid(raise_exception=True)
        updated_booking = serializer.save()

        return Response(BookingSerializer(updated_booking).data)


class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all()

        sort = self.request.query_params.get("sort")
        order = self.request.query_params.get("order", "asc")

        allowed_sort_fields = {
            "price": "price",
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

        return Response({"room_id": room_id, "status": "deleted"})

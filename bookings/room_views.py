from loguru import logger
from rest_framework import generics
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer


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

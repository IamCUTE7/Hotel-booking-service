import pytest

from bookings.models import Booking, Room

pytestmark = pytest.mark.django_db


def test_create_room(api_client):
    response = api_client.post(
        "/api/v1/rooms/create/",
        {
            "description": "Sea view room",
            "price_per_night": "120.00",
        },
        format="json",
    )

    assert response.status_code == 201
    assert Room.objects.count() == 1
    assert Room.objects.get().description == "Sea view room"


def test_list_rooms_sorted_by_price_asc(api_client):
    cheap = Room.objects.create(description="Cheap", price_per_night="50.00")
    expensive = Room.objects.create(description="Expensive", price_per_night="150.00")

    response = api_client.get("/api/v1/rooms/list/?sort=price&order=asc")

    assert response.status_code == 200
    ids = [room["id"] for room in response.json()]
    assert ids == [cheap.id, expensive.id]


def test_delete_room_deletes_bookings(api_client):
    room = Room.objects.create(description="Room", price_per_night="100.00")
    Booking.objects.create(room=room, start_date="2026-06-01", end_date="2026-06-03")

    response = api_client.delete(f"/api/v1/rooms/{room.id}/delete/")

    assert response.status_code == 200
    assert response.json() == {"room_id": room.id, "status": "deleted"}
    assert Room.objects.count() == 0
    assert Booking.objects.count() == 0


def test_create_booking(api_client):
    room = Room.objects.create(description="Room", price_per_night="100.00")

    response = api_client.post(
        "/api/v1/bookings/create/",
        {
            "room": room.id,
            "start_date": "2026-06-01",
            "end_date": "2026-06-03",
        },
        format="json",
    )

    assert response.status_code == 200
    assert Booking.objects.count() == 1
    assert response.json()["booking_id"] == Booking.objects.get().id


def test_list_bookings_filtered_by_room_id_sorted_by_start_date(api_client):
    room = Room.objects.create(description="Room", price_per_night="100.00")
    other_room = Room.objects.create(description="Other", price_per_night="90.00")

    second = Booking.objects.create(room=room, start_date="2026-06-10", end_date="2026-06-12")
    first = Booking.objects.create(room=room, start_date="2026-06-01", end_date="2026-06-03")
    Booking.objects.create(room=other_room, start_date="2026-06-05", end_date="2026-06-07")

    response = api_client.get(f"/api/v1/bookings/list/?room_id={room.id}")

    assert response.status_code == 200
    ids = [booking["id"] for booking in response.json()]
    assert ids == [first.id, second.id]


def test_delete_booking(api_client):
    room = Room.objects.create(description="Room", price_per_night="100.00")
    booking = Booking.objects.create(room=room, start_date="2026-06-01", end_date="2026-06-03")

    response = api_client.delete(f"/api/v1/bookings/{booking.id}/delete/")

    assert response.status_code == 200
    assert response.json() == {"booking_id": booking.id, "status": "deleted"}
    assert Booking.objects.count() == 0


def test_delete_missing_booking_returns_404(api_client):
    response = api_client.delete("/api/v1/bookings/999/delete/")

    assert response.status_code == 404
    assert response.json() == {"error": "object does not exist"}

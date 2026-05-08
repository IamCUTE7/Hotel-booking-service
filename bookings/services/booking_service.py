# business logic
from bookings.models import Booking


def create_booking(room_id, start_date, end_date):
    if start_date >= end_date:
        raise ValueError("Invalid dates")

    if not check_availability(room_id, start_date, end_date):
        raise ValueError("The room is occupied")

    return Booking.objects.create(room_id=room_id, start_date=start_date, end_date=end_date)


def check_availability(room_id, start_date, end_date, exclude_booking_id=None):  # check room status
    existing_booking = Booking.objects.filter(
        room_id=room_id, start_date__lt=end_date, end_date__gt=start_date
    )  # particular booking

    if exclude_booking_id:
        existing_booking = existing_booking.exclude(id=exclude_booking_id)

    if existing_booking.exists():
        return False

    return True


def get_bookings(*room_ids):  # see one/multiple bookings
    return Booking.objects.filter(room_id__in=room_ids)


def delete_booking(booking_id):
    deletion = Booking.objects.get(id=booking_id)

    if not deletion:
        raise ValueError("No such booking")

    deletion.delete()
    return True


def update_booking(booking_id, start_date, end_date):
    if start_date >= end_date:
        raise ValueError("Invalid dates")

    try:
        initial_booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        raise ValueError("No such booking")

    if not check_availability(initial_booking.room_id, start_date, end_date, exclude_booking_id=booking_id):
        raise ValueError("Room is occupied for these dates")

    initial_booking.start_date = start_date
    initial_booking.end_date = end_date

    initial_booking.save(update_fields=["start_date", "end_date"])

    return initial_booking

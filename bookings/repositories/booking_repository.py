from bookings.models import Booking


class BookingRepository:
    def create_booking(self, room_id, start_date, end_date):
        return Booking.objects.create(
            room_id=room_id,
            start_date=start_date,
            end_date=end_date,
        )

    def get_booking_by_id(self, booking_id):
        return Booking.objects.get(id=booking_id)

    def get_bookings_by_room_id(self, room_id):
        return Booking.objects.filter(room_id=room_id).order_by("start_date")

    def get_overlapping_bookings(
        self,
        room_id,
        start_date,
        end_date,
        exclude_booking_id=None,
    ):
        bookings = Booking.objects.filter(
            room_id=room_id,
            start_date__lt=end_date,
            end_date__gt=start_date,
        )

        if exclude_booking_id:
            bookings = bookings.exclude(id=exclude_booking_id)

        return bookings

    def update_booking_dates(self, booking, start_date, end_date):
        booking.start_date = start_date
        booking.end_date = end_date
        booking.save(update_fields=["start_date", "end_date"])

        return booking

    def delete_booking(self, booking):
        booking.delete()


booking_repository = BookingRepository()

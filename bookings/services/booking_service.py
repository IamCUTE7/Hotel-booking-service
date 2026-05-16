from loguru import logger

from bookings.models import Booking


class BookingService:
    def create_booking(self, room_id, start_date, end_date):
        if start_date >= end_date:
            logger.warning(
                "invalid booking dates: room_id={}, start_date={}, end_date={}", room_id, start_date, end_date
            )

            raise ValueError("Invalid dates")

        if not self.check_availability(room_id, start_date, end_date):
            logger.warning(
                "The room is occupied: room_id={}, start_date={}, end_date={}", room_id, start_date, end_date
            )

            raise ValueError("The room is occupied")

        logger.info("Booking created! room_id={}, start_date={}, end_date={}", room_id, start_date, end_date)

        return Booking.objects.create(room_id=room_id, start_date=start_date, end_date=end_date)

    def get_bookings_by_room_id(self, room_id):
        return Booking.objects.filter(room_id=room_id).order_by("start_date")

    def check_availability(self, room_id, start_date, end_date, exclude_booking_id=None):  # check room status
        existing_booking = Booking.objects.filter(
            room_id=room_id, start_date__lt=end_date, end_date__gt=start_date
        )  # particular booking

        if exclude_booking_id:
            existing_booking = existing_booking.exclude(id=exclude_booking_id)

        if existing_booking.exists():
            logger.warning(
                "The room is occupied for these dates: room_id={}, start_date={}, end_date={}",
                room_id,
                start_date,
                end_date,
            )

            return False

        return True

    def get_bookings(self, *room_ids):  # see one/multiple bookings
        return Booking.objects.filter(room_id__in=room_ids)

    def delete_booking(self, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            logger.warning("Such booking does not exist: booking_id={}", booking_id)
            raise ValueError("No such booking")

        booking.delete()

        logger.info("The booking has been deleted: booking_id={}", booking_id)

        return True

    def update_booking(self, booking_id, start_date, end_date):
        if start_date >= end_date:
            logger.warning(
                "cannot update - invalid booking dates: booking_id={}, start_date={}, end_date={}",
                booking_id,
                start_date,
                end_date,
            )

            raise ValueError("Invalid dates")

        try:
            initial_booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            logger.warning("Such booking does not exist: booking_id={}", booking_id)

            raise ValueError("No such booking")

        if not self.check_availability(initial_booking.room_id, start_date, end_date, exclude_booking_id=booking_id):
            raise ValueError("Room is occupied for these dates")

        initial_booking.start_date = start_date
        initial_booking.end_date = end_date

        initial_booking.save(update_fields=["start_date", "end_date"])

        logger.info(
            "The booking has been updated: room_id={}, start_date={}, end_date={}", booking_id, start_date, end_date
        )

        return initial_booking


booking_service = BookingService()

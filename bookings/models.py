from django.db import models


class Room(models.Model):
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.id} - {self.price_per_night}"

    class Meta:
        ordering = ["-price_per_night", "id"]


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Booking {self.id} ({self.start_date} - {self.end_date})"

    class Meta:
        ordering = ["-start_date"]

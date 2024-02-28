from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    source = models.CharField(max_length=100,default = 'Mumbai')  # Source airport
    destination = models.CharField(max_length=100, default = 'Mumbai')  # Destination airport
    departure_date = models.DateField()
    departure_time = models.TimeField()
    total_seats = models.IntegerField(default=60)
    price = models.DecimalField(max_digits=8, decimal_places=2,default = 1000)  # Add price field
    available_seats = models.IntegerField(default = 60)
    def __str__(self):
        return f"{self.flight_number} - {self.source} to {self.destination}"

    # Add other flight details
    # def available_seats(self):
    #     # Calculate the number of available seats based on existing bookings
    #     booked_seats = self.booking_set.count()
    #     return self.total_seats - booked_seats



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2 , default = 0)
    date_booked = models.DateTimeField(auto_now_add=True )

    def __str__(self):
        return f"{self.quantity} tickets for {self.flight} - {self.date_booked}"
    # Add other booking details 
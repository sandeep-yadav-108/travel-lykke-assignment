from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TravelOption(models.Model):
    TRAVEL_TYPES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]
    
    travel_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.type} from {self.source} to {self.destination}"
    
    @property
    def is_low_stock(self):
        """Check if seats are running low (less than or equal to 10)"""
        return self.available_seats <= 10 and self.available_seats > 0
    
    @property
    def is_sold_out(self):
        """Check if completely sold out"""
        return self.available_seats == 0
    
    @property
    def urgency_level(self):
        """Return urgency level based on available seats"""
        if self.available_seats == 0:
            return 'sold-out'
        elif self.available_seats <= 5:
            return 'critical'
        elif self.available_seats <= 15:
            return 'low'
        elif self.available_seats <= 50:
            return 'medium'
        else:
            return 'high'
    
    @property
    def estimated_capacity(self):
        """Estimate original capacity based on travel type"""
        capacity_map = {
            'flight': 150,
            'train': 200,
            'bus': 50
        }
        return capacity_map.get(self.type, 100)
    
    @property
    def occupancy_percentage(self):
        """Calculate how full the transport is"""
        booked_seats = self.estimated_capacity - self.available_seats
        return (booked_seats / self.estimated_capacity) * 100

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    
    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.username}"

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from booking.models import TravelOption

class Command(BaseCommand):
    help = 'Create sample travel options for testing'

    def handle(self, *args, **options):
        TravelOption.objects.all().delete()
        
        sample_data = [
            {
                'type': 'flight',
                'source': 'New York',
                'destination': 'Los Angeles',
                'date_time': timezone.now() + timedelta(days=7),
                'price': 299.99,
                'available_seats': 150
            },
            {
                'type': 'flight',
                'source': 'Chicago',
                'destination': 'Miami',
                'date_time': timezone.now() + timedelta(days=5),
                'price': 249.99,
                'available_seats': 120
            },
            {
                'type': 'flight',
                'source': 'San Francisco',
                'destination': 'Seattle',
                'date_time': timezone.now() + timedelta(days=3),
                'price': 179.99,
                'available_seats': 100
            },
            
            {
                'type': 'train',
                'source': 'Boston',
                'destination': 'Washington DC',
                'date_time': timezone.now() + timedelta(days=2),
                'price': 89.99,
                'available_seats': 200
            },
            {
                'type': 'train',
                'source': 'New York',
                'destination': 'Philadelphia',
                'date_time': timezone.now() + timedelta(days=1),
                'price': 45.99,
                'available_seats': 180
            },
            
            {
                'type': 'bus',
                'source': 'Dallas',
                'destination': 'Houston',
                'date_time': timezone.now() + timedelta(days=4),
                'price': 25.99,
                'available_seats': 50
            },
            {
                'type': 'bus',
                'source': 'Las Vegas',
                'destination': 'Phoenix',
                'date_time': timezone.now() + timedelta(days=6),
                'price': 35.99,
                'available_seats': 45
            },
            {
                'type': 'bus',
                'source': 'Denver',
                'destination': 'Salt Lake City',
                'date_time': timezone.now() + timedelta(days=8),
                'price': 55.99,
                'available_seats': 40
            }
        ]
        
        for data in sample_data:
            TravelOption.objects.create(**data)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(sample_data)} travel options')
        )

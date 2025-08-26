from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import TravelOption, Booking

class TravelOptionModelTest(TestCase):
    def setUp(self):
        self.travel_option = TravelOption.objects.create(
            type='flight',
            source='New York',
            destination='Los Angeles',
            date_time=timezone.now() + timedelta(days=7),
            price=Decimal('299.99'),
            available_seats=150
        )
    
    def test_travel_option_creation(self):
        self.assertEqual(self.travel_option.type, 'flight')
        self.assertEqual(self.travel_option.source, 'New York')
        self.assertEqual(self.travel_option.destination, 'Los Angeles')
        self.assertEqual(self.travel_option.price, Decimal('299.99'))
        self.assertEqual(self.travel_option.available_seats, 150)
    
    def test_travel_option_string_representation(self):
        expected = "flight from New York to Los Angeles"
        self.assertEqual(str(self.travel_option), expected)

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.travel_option = TravelOption.objects.create(
            type='train',
            source='Boston',
            destination='Washington DC',
            date_time=timezone.now() + timedelta(days=2),
            price=Decimal('89.99'),
            available_seats=200
        )
        self.booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2,
            total_price=Decimal('179.98')
        )
    
    def test_booking_creation(self):
        self.assertEqual(self.booking.user, self.user)
        self.assertEqual(self.booking.travel_option, self.travel_option)
        self.assertEqual(self.booking.number_of_seats, 2)
        self.assertEqual(self.booking.total_price, Decimal('179.98'))
        self.assertEqual(self.booking.status, 'confirmed')
    
    def test_booking_string_representation(self):
        expected = f"Booking {self.booking.booking_id} by testuser"
        self.assertEqual(str(self.booking), expected)

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.travel_option = TravelOption.objects.create(
            type='bus',
            source='Dallas',
            destination='Houston',
            date_time=timezone.now() + timedelta(days=4),
            price=Decimal('25.99'),
            available_seats=50
        )
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Travel Lykke')
    
    def test_travel_options_view(self):
        response = self.client.get(reverse('travel_options'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Available Travel Options')
        self.assertContains(response, 'Dallas')
        self.assertContains(response, 'Houston')
    
    def test_travel_options_filter_by_type(self):
        response = self.client.get(reverse('travel_options') + '?type=bus')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dallas')
    
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
    
    def test_register_view_post(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_required_for_booking(self):
        response = self.client.get(reverse('book_travel', kwargs={'travel_id': self.travel_option.travel_id}))
        self.assertEqual(response.status_code, 302)
    
    def test_booking_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('book_travel', kwargs={'travel_id': self.travel_option.travel_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book Travel')
    
    def test_my_bookings_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Bookings')

class BookingLogicTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.travel_option = TravelOption.objects.create(
            type='flight',
            source='San Francisco',
            destination='Seattle',
            date_time=timezone.now() + timedelta(days=3),
            price=Decimal('179.99'),
            available_seats=5
        )
    
    def test_successful_booking(self):
        self.client.login(username='testuser', password='testpass123')
        initial_seats = self.travel_option.available_seats
        
        response = self.client.post(reverse('book_travel', kwargs={'travel_id': self.travel_option.travel_id}), {
            'seats': 2
        })
        
        self.assertEqual(response.status_code, 302)
        
        booking = Booking.objects.get(user=self.user, travel_option=self.travel_option)
        self.assertEqual(booking.number_of_seats, 2)
        self.assertEqual(booking.total_price, Decimal('359.98'))
        
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, initial_seats - 2)
    
    def test_booking_exceeds_available_seats(self):
        self.client.login(username='testuser', password='testpass123')
        initial_seats = self.travel_option.available_seats
        
        response = self.client.post(reverse('book_travel', kwargs={'travel_id': self.travel_option.travel_id}), {
            'seats': 10
        })
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(Booking.objects.filter(user=self.user).count(), 0)
        
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, initial_seats)
    
    def test_booking_cancellation(self):
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2,
            total_price=Decimal('359.98')
        )
        
        self.travel_option.available_seats -= 2
        self.travel_option.save()
        initial_seats = self.travel_option.available_seats
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('cancel_booking', kwargs={'booking_id': booking.booking_id}))
        
        self.assertEqual(response.status_code, 302)
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')
        
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, initial_seats + 2)

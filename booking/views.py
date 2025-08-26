from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from .models import TravelOption, Booking
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'booking/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'booking/register.html', {'form': form})

def travel_options(request):
    options = TravelOption.objects.all()
    
    travel_type = request.GET.get('type')
    if travel_type:
        options = options.filter(type=travel_type)
    
    source = request.GET.get('source')
    if source:
        options = options.filter(source__icontains=source)
    
    destination = request.GET.get('destination')
    if destination:
        options = options.filter(destination__icontains=destination)
    
    date = request.GET.get('date')
    if date:
        options = options.filter(date_time__date=date)
    
    return render(request, 'booking/travel_options.html', {'options': options})

@login_required
def book_travel(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)
    
    if request.method == 'POST':
        seats = int(request.POST.get('seats', 1))
        
        if seats <= travel_option.available_seats:
            total_price = travel_option.price * seats
            
            booking = Booking.objects.create(
                user=request.user,
                travel_option=travel_option,
                number_of_seats=seats,
                total_price=total_price
            )
            
            travel_option.available_seats -= seats
            travel_option.save()
            
            messages.success(request, f'Booking confirmed! Booking ID: {booking.booking_id}')
            return redirect('my_bookings')
        else:
            messages.error(request, 'Not enough seats available!')
    
    return render(request, 'booking/book_travel.html', {'travel_option': travel_option})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    if booking.status == 'confirmed':
        booking.status = 'cancelled'
        booking.save()
        
        travel_option = booking.travel_option
        travel_option.available_seats += booking.number_of_seats
        travel_option.save()
        
        messages.success(request, 'Booking cancelled successfully!')
    else:
        messages.error(request, 'This booking is already cancelled!')
    
    return redirect('my_bookings')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def travel_detail(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)
    return render(request, 'booking/travel_detail.html', {'travel_option': travel_option})

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'booking/profile.html')

# Create your views here.
from .models import Flight, Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'user_login.html', {'form': form})




def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('user_login')  # Redirect to login page after successful sign up
    else:
        form = UserCreationForm()
    return render(request, 'user_signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

def home(request):
    return render(request, 'home.html')

# In views.py



def search_flights(request):
    if request.method == 'POST':
        # Retrieve search parameters from the form
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        # Query the Flight model to retrieve matching flights
        flights = Flight.objects.filter(departure_date=date, departure_time=time)
        # Pass the search results to the template for rendering
        return render(request, 'search_flights.html', {'flights': flights})
    else:
        # Render the search form
        return render(request, 'search_flights.html')



def book_flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    if request.method == 'POST':
        # Retrieve booking details from the form
        # For simplicity, let's assume the user can only book one ticket at a time
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= flight.available_seats:
            # Create a new booking
            booking = Booking.objects.create(
                flight=flight,
                user=request.user,
                quantity=quantity,
                total_price=flight.price * quantity
            )
            # Update available seats for the flight
            flight.available_seats -= quantity
            flight.save()
            # Redirect to a page confirming the booking
            return redirect('booking_confirmation', booking_id=booking.id)
        else:
            # Return an error message if there are not enough available seats
            error_message = f"Not enough available seats for {flight.flight_number}. Available seats: {flight.available_seats}"
            return render(request, 'booking_error.html', {'flight': flight,'error_message':error_message})
    else:
        return render(request, 'booking_form.html', {'flight': flight})


from django.shortcuts import render, get_object_or_404


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})


def my_bookings(request):
    # Retrieve bookings for the current user
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

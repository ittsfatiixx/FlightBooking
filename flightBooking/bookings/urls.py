# In urls.py

from django.urls import path
from .views import *

urlpatterns = [
      path('', home, name='home'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('signup/', user_signup, name='user_signup'),
    path('search/', search_flights, name='search_flights'),
    path('book/<int:flight_id>/', book_flight, name='book_flight'),
    path('booking_confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('my_bookings/', my_bookings, name='my_bookings'),
    
    # Add other URLs as needed
]

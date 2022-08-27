from django.urls import path, include

urlpatterns = [
    path('movies', include('movies.urls')),
    path('reviews', include('reviews.urls')),
    path('users',include('users.urls')),
    path('Reserve', include('reservations.urls'))
]

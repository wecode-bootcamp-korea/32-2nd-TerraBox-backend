from django.urls import path, include

urlpatterns = [
    path('Reserve', include('reservations.urls'))
]

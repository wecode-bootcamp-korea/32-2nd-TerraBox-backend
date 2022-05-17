from django.urls import path
from reservations.views import ReserveView

urlpatterns = [
    path('', ReserveView.as_view())
]

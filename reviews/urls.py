from django.urls import path
from .views      import MoviePostDetailView

urlpatterns = [
    path('/<int:moviepost_id>',MoviePostDetailView.as_view())
]

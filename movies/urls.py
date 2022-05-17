from django.urls import path
from .views import ProductListView,MovieDetailView

urlpatterns = [
    path('',ProductListView.as_view()),
    path('/<int:movie_id>',MovieDetailView.as_view())
]

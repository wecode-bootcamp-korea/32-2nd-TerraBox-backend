from django.urls import path, include
from .views import ProductListView

urlpatterns = [
    path('',ProductListView.as_view()),
    path('/<int:movie_id>/reviews',include('reviews.urls'))
]

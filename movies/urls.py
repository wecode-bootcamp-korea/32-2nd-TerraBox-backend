from django.urls   import path, include
from .views        import ProductListView,MovieDetailView
from reviews.views import MoviePostView

urlpatterns = [
    path('',ProductListView.as_view()),
    path('/<int:movie_id>',MovieDetailView.as_view()),
    path('/<int:movie_id>/movieposts',MoviePostView.as_view()),
]

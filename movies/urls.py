from django.urls   import path
from .views        import ProductListView,MovieDetailView
from reviews.views import MoviePostView, MoviePostDetailView

urlpatterns = [
    path('',ProductListView.as_view()),
    path('/<int:movie_id>',MovieDetailView.as_view()),
    path('/<int:movie_id>/movieposts',MoviePostView.as_view()),
    path('/<int:movie_id>/movieposts/<int:moviepost_id>',MoviePostDetailView.as_view())
]

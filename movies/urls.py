from django.urls   import path
from .views        import ProductListView, MovieDetailView
from reviews.views import (
    MoviePostView,
    MoviePostDetailView,
    MoviePostLike,
    ReviewView,
    ReviewDetailView,
    ReviewLike,
)

urlpatterns = [
    path('',ProductListView.as_view()),
    path('/<int:movie_id>',MovieDetailView.as_view()),
    path('/<int:movie_id>/movieposts',MoviePostView.as_view()),
    path('/<int:movie_id>/movieposts/<int:moviepost_id>',MoviePostDetailView.as_view()),
    path('/<int:movie_id>/movieposts/<int:moviepost_id>/like',MoviePostLike.as_view()),
    path('/<int:movie_id>/reviews',ReviewView.as_view()),
    path('/<int:movie_id>/reviews/<int:review_id>',ReviewDetailView.as_view()),
    path('/<int:movie_id>/reviews/<int:review_id>/like',ReviewLike.as_view()),
]
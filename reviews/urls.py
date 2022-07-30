from django.urls   import path
from reviews.views import (
    UserMoviePostView,
    UserMovieReviewView
)

urlpatterns = [
    path('/usermoviereviews',UserMovieReviewView.as_view()),
    path('/usermovieposts',UserMoviePostView.as_view()),
]
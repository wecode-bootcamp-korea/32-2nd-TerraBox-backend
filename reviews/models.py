from django.db import models
from core.models   import TimeStampedModel

class MovieReview(TimeStampedModel):
    movie        = models.ForeignKey('movies.Movie',on_delete=models.CASCADE)
    user         = models.ForeignKey('users.USER',on_delete=models.CASCADE)
    content      = models.CharField(max_length=1000)
    images_url   = models.CharField(max_length=1000)
    storage_path = models.CharField(max_length=1000)
    likes        = models.ManyToManyField('users.USER',related_name='likes',through='UserReviewLike')
    comments     = models.ManyToManyField('users.USER',related_name='comments',through='UserReviewComment')

    class Meta:
        db_table = 'movie_reviews'

class UserReviewLike(TimeStampedModel):
    review        = models.ForeignKey('MovieReview',on_delete=models.CASCADE)
    user          = models.ForeignKey('users.USER',on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_review_likes'

class UserReviewComment(TimeStampedModel):
    review        = models.ForeignKey('MovieReview',on_delete=models.CASCADE)
    user          = models.ForeignKey('users.USER',on_delete=models.CASCADE)
    content       = models.CharField(max_length=1000)

    class Meta:
        db_table = 'user_review_comments'
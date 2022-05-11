from django.db   import models

from core.models   import TimeStampedModel

class Reservation(TimeStampedModel):
    user          = models.ForeignKey("users.User",on_delete=models.CASCADE)
    movie_theater = models.ForeignKey("movies.MovieTheater",on_delete=models.CASCADE)
    price         = models.PositiveIntegerField()
    type          = models.CharField(max_length=20)
    seat          = models.ForeignKey('movies.Seat',on_delete=models.CASCADE,null=True)


    class Meta:
        db_table = 'reservations'


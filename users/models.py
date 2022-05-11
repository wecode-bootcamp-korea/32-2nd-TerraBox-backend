from django.db   import models
from core.models import TimeStampedModel

class User(TimeStampedModel):
    kakao_id = models.PositiveBigIntegerField(unique=True)
    nickname = models.CharField(max_length=50)
    name     = models.CharField(max_length=50)
    birthday = models.CharField(max_length=50)
    reservations = models.ManyToManyField("movies.MovieTheater",related_name='reservations',through='reservations.Reservation')

    class Meta:
        db_table = 'users'
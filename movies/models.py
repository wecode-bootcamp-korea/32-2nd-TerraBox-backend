from django.db   import models
import enum

class Price(enum.Enum):
    ADULT    = 12000
    TEENAGER = 9000
    KID      = 5000

import enum

class Price(enum.Enum):
    ADULT    = 12000
    TEENAGER = 9000
    KID      = 5000

class Movie(models.Model):
    name           = models.CharField(max_length=50)
    eng_name       = models.CharField(max_length=100)
    description    = models.CharField(max_length=500)
    detail_text    = models.CharField(max_length=500)
    age_grade      = models.CharField(max_length=500)
    is_subtitle    = models.BooleanField()
    screening_type = models.PositiveIntegerField()
    preview_url    = models.CharField(max_length=500)
    running_time   = models.PositiveIntegerField()
    theaters       = models.ManyToManyField('movies.Theater',through='movies.MovieTheater')


    class Meta:
        db_table = 'movies'

class WatchPoint(models.Model):
    movie         = models.OneToOneField('Movie',on_delete=models.CASCADE)
    director      = models.PositiveIntegerField()
    actor         = models.PositiveIntegerField()
    visual_beauty = models.PositiveIntegerField()
    ost           = models.PositiveIntegerField()
    story         = models.PositiveIntegerField()

    class Meta:
        db_table = 'watch_points'

class MovieImage(models.Model):
    movie        = models.ForeignKey('Movie',on_delete=models.CASCADE)
    storage_path = models.CharField(max_length=500,null=True)
    stillcut_url = models.CharField(max_length=500)

    class Meta:
        db_table = 'movie_images'

class WatchCount(models.Model):
    movie    = models.ForeignKey('Movie',on_delete=models.CASCADE)
    day_time = models.DateField()
    count    = models.PositiveIntegerField()

    class Meta:
        db_table = 'watch_counts'

class Region(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'regions'

class Theater(models.Model):
    region     = models.ForeignKey('Region',on_delete=models.CASCADE)
    name       = models.CharField(max_length=100)
    latitude   = models.CharField(max_length=100)
    longtitude = models.CharField(max_length=100)

    class Meta:
        db_table = 'theaters'


class Room(models.Model):
    theater = models.ForeignKey('Theater',on_delete=models.CASCADE)
    name    = models.CharField(max_length=100)

    class Meta:
        db_table = 'rooms'

class Seat(models.Model):
    room          = models.ForeignKey('Room',on_delete=models.CASCADE)
    seat_location = models.CharField(max_length=10)

    class Meta:
        db_table = 'seats'


class MovieTheater(models.Model):
    movie      = models.ForeignKey('movies.Movie',on_delete=models.CASCADE)
    theater    = models.ForeignKey('Theater',on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    room       = models.ForeignKey('Room',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'movie_theaters'
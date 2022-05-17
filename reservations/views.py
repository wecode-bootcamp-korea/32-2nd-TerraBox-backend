import json
import datetime

from django.utils.dateformat import DateFormat
from django.http             import JsonResponse
from django.views            import View
from django.db.models        import Q
from django.db.models        import Count
from django.db.models        import Case, When
from core.decorators         import access_token_check

from movies.models import Movie, MovieTheater, Theater, Seat, Region, Room, Price
from .models       import Reservation

def calculate_end_time(start_time, running_time):
    H, M = divmod(running_time, 60)
    return datetime.datetime.strftime(start_time + datetime.timedelta(hours=H, minutes=M), "%H:%M")

def calculate_start_time(start_time):
    return datetime.datetime.strftime(start_time, "%H:%M")

def json_default(value): 
    if isinstance(value, datetime.date): 
        return value.strftime('%Y-%m-%d') 
    raise TypeError('not JSON serializable') 
data = {'date': datetime.date.today()} 
json_data = json.dumps(data, default=json_default)

class MovieListView(View):
    def get(self, request):

        movies = Movie.objects.all()

        movie_list = [{
            'movie_id'     : movie.id,
            'movie_name'   : movie.name,
            'age_grade'    : movie.age_grade,
        } for movie in movies]

        return JsonResponse({'movies' : movie_list}, status=200)


class RegionListView(View):
    def get(self, request):
        regions = Region.objects.all()
        region_list = [{
            'region_id'   : region.id,
            'region_name' : region.name,
            'theaters'    : [
            {
                'theater_id'   : theater.id,
                'theater_name' : theater.name
            }for theater in Theater.objects.filter(region=region)]
        } for region in regions]

        return JsonResponse({'regions' : region_list}, status=200)


class MovieTheaterListView(View):
    def get(self, request):
        movie_id   = request.GET.get("movie_id")
        theater_id = request.GET.get("theater_id")

        q = Q()

        if movie_id:
            q &= Q(movie_id__in = movie_id)

        if theater_id:
            q &= Q(theater_id__in = theater_id)

        movietheaters = MovieTheater.objects.filter(q).annotate(reserved_seat_count  = Count('reservation__id')
        )

        movie_theater_list = [{
            'timetable_id'     : movietheater.id,
            'start_time'       : calculate_start_time(movietheater.start_time),
            'end_time'         : calculate_end_time(movietheater.start_time, movietheater.movie.running_time),
            'movies_id'        : movietheater.movie.id,
            'movies_name'      : movietheater.movie.name,
            'tatal_seat_count' : 40,
            'able_seat_count'  : 40 - int(movietheater.reserved_seat_count),
            'screening_type'   : movietheater.movie.screening_type,
            'is_subtitle'      : movietheater.movie.is_subtitle,
            'theater_id'       : movietheater.theater.id,
            'theater_name'     : movietheater.theater.name,
            'room_name'        : movietheater.room.name
        }for movietheater in movietheaters]

        return JsonResponse({'timetable' : movie_theater_list}, status=200)


class UserTypeListView(View):
    def get(self, request):
        return JsonResponse({'price_list' : [{price.name : price.value}for price in Price]}, status=200)


class SeatListView(View):
    def get(self, request):
        movietheater_id = request.GET.get("movietheater_id")

        room          = Room.objects.get(movietheater = movietheater_id)
        reserved_seat = Seat.objects.filter(Q(room_id=room.id), 
        #Q(reservation__movie_theater_id=movietheater_id), 
        Q(reservation__movie_theater_id=movietheater_id)
        | Q(reservation__movie_theater_id__isnull=True)).annotate(
            is_reserved = Case(When(
                reservation__id__isnull=False, 
                reservation__movie_theater_id=movietheater_id, then=True), 
                default=False))

    

        seats_list = {
            'room_id'    : room.id,
            'room_name'  : room.name,
            'seats'  : [{
                'id'   : seat.id,
                'location' : seat.seat_location,
                'is_reserved' : seat.is_reserved
            }for seat in reserved_seat]
        }

        return JsonResponse({'seats_list' : seats_list}, status=200)


class ReserveView(View):
    @access_token_check
    def post(self, request):
        datas      = json.loads(request.body)

        for data in datas:
            if Reservation.objects.filter(movie_theater_id = data["movie_theater_id"], seat_id = data['seat_id']).exists():
                return JsonResponse({'message' : 'ALREADY_EXIST'}, status=409)

            Reservation.objects.create(
                user_id          = request.user,
                movie_theater_id = data["movie_theater_id"],
                type             = data['type'],
                price            = Price[data['type']].value,
                seat_id          = data['seat_id']
            )

        return JsonResponse({'message' : '예매가 완료되었습니다.'}, status=201)
import json
import datetime

from django.utils.dateformat import DateFormat
from django.http             import JsonResponse
from django.views            import View
from django.db.models        import Q
from django.db.models        import Count
from django.db.models        import Case, When

from movies.models import Movie, MovieTheater, Theater, Seat, Region, Room, Price
from users.models  import User
from .models       import Reservation

def json_default(value): 
    if isinstance(value, datetime.date): 
        return value.strftime('%Y-%m-%d') 
    raise TypeError('not JSON serializable') 
data = {'date': datetime.date.today()} 
json_data = json.dumps(data, default=json_default)



class MovieListView(View):
    def get(self, request)
        start_time = request.GET.get("start_date") #"2022-05-01"
        end_time   = request.GET.get("start_date") #"2022-05-02"

        movies = Movie.objects.all().annotate(
            is_avaliable = Case(
                When(
                    movietheater__start_time__gte=start_time, 
                    movietheater__start_time__lte=end_time, 
                then=True), 
                default=False
            )
        ).distinct()

        movie_list = [{
            'movie_id'     : movie.id,
            'movie_name'   : movie.name,
            'age_grade'    : movie.age_grade,
            'is_avaliable' : movie.is_avaliable
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

        movietheaters = MovieTheater.objects.filter(q).annotate(
            total_seat_count = Count('room__seat__id'),
            able_seat_count  = Count('reservation__id')
        )

        movie_theater_list = [{
            'timetable_id'     : movietheater.id,
            'start_time'       : movietheater.start_time,
            'end_time'         : movietheater.end_time,
            'movies_id'        : movietheater.movie.id,
            'movies_name'      : movietheater.movie.name,
            'tatal_seat_count' : movietheater.total_seat_count,
            'able_seat_count'  : int(movietheater.total_seat_count) - int(movietheater.able_seat_count),
            'screening_type'   : movietheater.movie.screening_type,
            'is_subtitle'      : movietheater.movie.is_subtitle,
            'theater_id'       : movietheater.theater.id,
            'theater_name'     : movietheater.theater.name,
            'room_name'        : movietheater.room.name
        }for movietheater in movietheaters]

        return JsonResponse({'timetable' : timetable_list}, status=200)

class UserTypeListView(View):
    def get(self, request):
        return JsonResponse([{price.name : price.value} for price in Price], status=200)

class SeatListView(View):
    def get(self, request):
        movietheater_id = request.GET.get("movietheater_id")

        room          = Room.objects.get(movietheater = movietheater_id)
        reserved_seat = Seat.objects.filter(room_id=room.id).annotate(is_reserved = Case(When(reservation__id__isnull=False, reservation__movie_theater_id=movietheater_id, then=False), default=True))

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
    def post(self, request):
        data      = json.loads(request.body)
        user_type = Price[data['type']]

        if Reservation.objects.filter(movie_theater_id = data["movie_theater_id"], seat_id = seat_id).exists():
            return JsonResponse({'message' : 'ALREADY_EXIST'}, status=409)

        Reservation.objects.create(
            user_id          = request.user.id,
            movie_theater_id = movie_theater_id,
            user_type        = user_type.name,
            price            = user_type.value,
            seat_id          = seat_id
        )

        return JsonResponse({'message' : '예매가 완료되었습니다.'}, status=201)

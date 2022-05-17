import json
import enum, datetime

from django.utils.dateformat import DateFormat
from django.http             import JsonResponse
from django.views            import View
from django.db.models        import Q
from django.db.models        import Count
from django.db.models        import Case, When


from movies.models import Movie, MovieTheater, Theater, Seat, Region, Room
from users.models  import User
from       .models import Reservation

from .models import Reservation

class Price(enum.Enum):
    ADULT    = 12000
    TEENAGER = 9000
    KID      = 5000

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


#json 모듈은 data를 받아서 그 데이터 구조를 따라 iteration을 돌면서 내부 value들을 json string으로 변환하려고 할 것이다.
#그 와중에 date 타입 변수가 끼어들면서 당장 문자열로 변환할 수 없게 되면서 Type Error를 내는 것이다. 
#default로 내가 함수를 지정해 놓았다면, 이 순간 문제를 일으키는 value를 가지고 default 함수에 던져서 해결할 수 있는 건 해결하는 것 

class ReserveView(View):

    def post(self, request):
    # get으로 받아온 데이터를 post방식으로 예매된 데이터를 reservations테이블에 데이터 저장하기 위한 코드
    # 영화관이랑 영화 매칭이 벗어나는지 검증하고 벗어나면 오류
    # 검증 완료시 reservation에 데이터 objects.create로 넣어주기
    # 성공시 SUCCESS 메세지 보내주면서 201, 나머지 키에러 등 작업        
        try :
            user             = request.user
            data             = json.loads(request.body)
            movie_theater_id = data['movie_theater_id']
            user_type        = data['type']
            seat_id          = Seat.objects.get(id = seat_id).seat

            if Reservation.objects.filter(user_id=user.id, movie_theater_id=movie_theater_id).exists():
                return JsonResponse({'message' : 'ALREADY_EXIST'}, status=400)

            Reservation.objects.create(
                user_id          = user.id,
                movie_theater_id = movie_theater_id,
                user_type        = user_type,
                price            = user_type * Price,
                seat_id          = seat_id
            )
            return JsonResponse({'message' : '예매가 완료되었습니다.'}, status=201)
        
        except Reservation.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_SCHEDULE'}, status=400)


    def get(self, request):
        #예매 페이지 화면에서 DB에 필요한 데이터를 보내주기위해 get 사용
        # 오늘날짜, 영화id, 영화관id, 소비자가 리스트 출력
        # 각 list는 get_함수에서 뽑아온 데이터로 뽑아주기
        # 결과값으로 각 데이터 리스트 출력 
        today      = datetime.date.today()
        movie_id   = request.GET.get('movie_id', None)
        theater_id = request.GET.get('theater_id', None)
        movietheater_id = request.GET.get('movietheater_id', None)
        user_price = request.GET.get(None)

        movie_list            = self.get_movies()
        region_list           = self.get_regions()
        timetable_list        = self.get_timetable(movie_id, theater_id)
        user_price            = self.get_user_price(user_price)
        seat_list             = self.get_user_seat(movietheater_id)


        result = {
            'date'                 : today,
            'movies_list'          : movie_list['movie'],
            'regions_list'         : region_list['region'],
            'schedules_list'       : timetable_list['timetable'],
            'user_price'           : user_price['user_price'],
            'seat_list'            : seat_list['seats_list']
        }
        return JsonResponse(result, status=200)


#영화 리스트
    def get_movies(self):

        movies = Movie.objects.all()

        movie_list = [{
            'movie_id'   : movie.id,
            'movie_name' : movie.name,
            'age_grade'  : movie.age_grade
        } for movie in movies]

        return {'movie' : movie_list}

#영화관 리스트
    def get_regions(self):

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

        return {'region' : region_list}

#시간표 리스트
#영화와 영화관 선택한 시간표가 나올수 있게 Q객체 사용
    def get_timetable(self, movie_id, theater_id):

        timetable = Q()

        if movie_id:
            timetable &= Q(movie_id__in = movie_id)

        if theater_id:
            timetable &= Q(theater_id__in = theater_id)

        movietheaters = MovieTheater.objects.filter(timetable).annotate(total_seat_count=Count('room__seat__id'),able_seat_count=Count('reservation__id'))

        timetable_list = [{
            'timetable_id'     : movietheater.id,
            'start_time'       : calculate_start_time(movietheater.start_time),
            'end_time'         : calculate_end_time(movietheater.start_time, movietheater.movie.running_time),
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

        return {'timetable' : timetable_list}


#front에서 요청한 이용자 타입별 가격 리스트
#테이블로 만들어져 있지않아서 get_user_price 함수로 get 호출시 보내주기로 함 
    def get_user_price(self, timetable):
    
        timetable_seat = Q()

        if timetable:
            timetable_seat &= Q(movietheater_id__in = timetable)


        user_price = [{

            'ADULT'        : 12000,
            'TEENAGER'     : 9000,
            'KID'          : 5000
        }]

        return {'user_price' : user_price}


    def get_user_seat(self, movietheater_id):
    
        # timetable = Q()

        # if movietheater_id:
        #     timetable &= Q()

        room            = Room.objects.get(movietheater = movietheater_id)
        #reserved_seat    = Seat.objects.filter(room_id=room.id).annotate(is_reserved = Case(When(reservation__id__isnull=True, reservation__movie_theater_id=movietheater_id, then=False), default=True))
        reserved_seat    = Seat.objects.filter(room_id=room.id).annotate(is_reserved = Case(When(reservation__id__isnull=True, then=False), default=True))
        seats_list = {
            'room_id'    : room.id,
            'room_name'  : room.name,
            'seats'  : [{
                'id'   : seat.id,
                'location' : seat.seat_location,
                'is_reserved' : seat.is_reserved
            }for seat in reserved_seat]
        }

        return {'seats_list' : seats_list}
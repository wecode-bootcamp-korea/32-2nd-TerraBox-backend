from django.urls import path
from reservations.views import MovieListView, RegionListView, MovieTheaterListView, UserTypeListView, SeatListView, ReserveView

urlpatterns = [
    path('/movie', MovieListView.as_view()),
    path('/region', RegionListView.as_view()),
    path('/movietheater', MovieTheaterListView.as_view()),
    path('/price', UserTypeListView.as_view()),
    path('/seatlist', SeatListView.as_view()),
    path('', ReserveView.as_view()),

    

]

from django.http      import JsonResponse
from django.views     import View
from .models          import Movie, MovieImage

class ProductListView(View):
    """
    사용처
    -메인페이지의 캐러셀에 사용

    반환
    -영화 리스트를 반환
    """


    def get(self,requests):
        
        movies_list = Movie.objects.all().prefetch_related('movieimage_set')
        result = [{
            'id'          :movie.id,
            'name'        :movie.name,
            'stillcut_url':[movie.stillcut_url for movie in movie.movieimage_set.all()][0]
        } for movie in movies_list]
                
        return JsonResponse({"result":result},status = 200)



from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count

from movies.models    import Movie, MovieImage
from reviews.models   import MoviePost

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


class MovieDetailView(View):
    def get(self,request,movie_id):
        movie = Movie.objects.prefetch_related('movieimage_set').get(id=movie_id)
        movieposts = MoviePost.objects.filter(movie=movie).select_related('user').annotate(like_count = Count('userpostlike'))
        
        result = {
                'id'            : movie.id,
                'name'          : movie.name,
                'eng_name'      : movie.eng_name,
                'description'   : movie.description,
                'stillcut_urls' : [image.stillcut_url for image in movie.movieimage_set.all()],
                'preview_url'   : movie.preview_url,
                'movieposts_count' : movie.moviepost_set.all().count(),
                'movieposts'    : [{
                    'movie_name' : movie.name,
                    'user_name'  : moviepost.user.nickname,
                    'content'    : moviepost.content,
                    'images_url' : moviepost.images_url,
                    
                    }for moviepost in movieposts]
            } 
        
        return JsonResponse({'result':result}, status=200)

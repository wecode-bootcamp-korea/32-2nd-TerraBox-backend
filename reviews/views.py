import uuid
import boto3

from django.views       import View
from django.http        import JsonResponse

from TerraBox.settings  import (
                        AWS_ACCESS_KEY_ID,
                        AWS_SECRET_ACCESS_KEY,
                        AWS_STORAGE_BUCKET_NAME,
                        S3_IMAGE_URL
                        )
# from core               import decorators
from reviews.models     import MoviePost
from movies.models      import Movie
from users.models       import User

        
class MoviePostDetailView(View):
    def get(self,request,movie_id,moviepost_id):
        moviepost = MoviePost.objects.select_related('user').get(id=moviepost_id)
        movie = Movie.objects.get(id=movie_id)
        moviepost = {
            "movie_name" : movie.name,
            "user"       : moviepost.user.nickname,
            "content"    : moviepost.content,
            "image_url"  : moviepost.images_url,
        }
        
        return JsonResponse({"moviepost":moviepost}, status=201)

    #decorator
    def post(self,request,movie_id,moviepost_id): #아니 왜 form은 put안돼나요?
        try:
            image_file = request.FILES.__getitem__('image')
            content    = request.POST['content']
            # user     = request.user #decorator
            user       = User.objects.first()
            moviepost  = MoviePost.objects.select_related('user').get(id=moviepost_id)
            movie      = Movie.objects.get(id=movie_id)
            
            if user != moviepost.user:
                return JsonResponse({"message":"INVALID_USER"}, status=401)
            
            s3r   = boto3.resource('s3',
                                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
            s3r.Object(AWS_STORAGE_BUCKET_NAME,moviepost.storage_path).delete()
            
            key       = "moviepost/" + "%s/" %(movie.id) +"%s-" %(user.id)+ str(uuid.uuid4())
            image_url = S3_IMAGE_URL + key
            s3r.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=key,Body=image_file,ContentType='jpg')
            
            moviepost.content      = content
            moviepost.images_url   = image_url
            moviepost.storage_path = key
            moviepost.save()
            
            return JsonResponse({"message": "updated!"}, status=201)    
        
        except KeyError:
            return JsonResponse({'message:','key_error'},status=400)
    
    #@decorator
    def delete(self,request,movie_id,moviepost_id):
        
        # user     = request.user #decorator
        user       = User.objects.first()
        moviepost  = MoviePost.objects.select_related('user').get(id=moviepost_id)
        
        if user != moviepost.user:
            return JsonResponse({"message":"INVALID_USER"}, status=401)
        
        s3r   = boto3.resource('s3',
                                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
        s3r.Object(AWS_STORAGE_BUCKET_NAME,moviepost.storage_path).delete()
        moviepost.delete()
        
        return JsonResponse({"message":"deleted!"}, status=204)
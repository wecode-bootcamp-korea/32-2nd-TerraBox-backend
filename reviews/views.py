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

from core.decorators    import access_token_check
from reviews.models     import MoviePost
from movies.models      import Movie
from users.models       import User

class MoviePostView(View):
    @access_token_check
    def post(self,request,movie_id):
        try:
            image_file = request.FILES.__getitem__('image')
            content    = request.POST.get('content')
            user       = request.user
            user       = User.objects.first()
            movie      = Movie.objects.get(id=movie_id)
            
            s3r        = boto3.resource('s3',
                                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
            key        = "moviepost/" + "%s/" %(movie.id) +"%s-" %(user.id)+ str(uuid.uuid4())
            image_url  = S3_IMAGE_URL + key
            s3r.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=key,Body=image_file,ContentType='jpeg')
            
            MoviePost.objects.create(
                movie         = movie,
                user          = user,
                content       = content,
                images_url    = image_url,
                storage_path  = key
            )
            
            return JsonResponse({"message": "created!"}, status=201)

        except KeyError:
            return JsonResponse({'message:','key_error'},status=400)
        except Exception as e:
            return JsonResponse({'Error':e})
        
        
class MoviePostDetailView(View):
    
    @access_token_check
    def post(self,request,movie_id,moviepost_id):
        try:
            image_file = request.FILES.__getitem__('image')
            content    = request.POST['content']
            user       = request.user #decorator
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
    
    @access_token_check
    def delete(self,request,movie_id,moviepost_id):
        
        user     = request.user 
        moviepost  = MoviePost.objects.select_related('user').get(id=moviepost_id)
        
        if user != moviepost.user:
            return JsonResponse({"message":"INVALID_USER"}, status=401)
        
        s3r   = boto3.resource('s3',
                                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
        s3r.Object(AWS_STORAGE_BUCKET_NAME,moviepost.storage_path).delete()
        moviepost.delete()
        
        return JsonResponse({"message":"deleted!"}, status=204)

    
    

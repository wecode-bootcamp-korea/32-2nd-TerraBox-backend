import uuid
import boto3
import json

from django.views       import View
from django.http        import JsonResponse

from TerraBox.settings  import (
AWS_ACCESS_KEY_ID,
AWS_SECRET_ACCESS_KEY,
AWS_STORAGE_BUCKET_NAME,
S3_IMAGE_URL
)

from core.decorators    import access_token_check
from reviews.models     import MoviePost, MovieReview
from movies.models      import Movie
from users.models       import User
from reviews.models     import UserPostLike, UserReviewLike


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
    
    def get(self,request,movie_id,moviepost_id):
        moviepost = MoviePost.objects.select_related('user').get(id=moviepost_id)
        movie     = Movie.objects.get(id=movie_id)
        moviepost = {
            "movie_name" : movie.name,
            "user"       : moviepost.user.nickname,
            "content"    : moviepost.content,
            "image_url"  : moviepost.images_url,
            'like'       : moviepost.userpostlike_set.all().count()
        }
        return JsonResponse({"moviepost":moviepost}, status=201)
    
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
        moviepost  = MoviePost.objects.get(id=moviepost_id)
        
        if user != moviepost.user:
            return JsonResponse({"message":"INVALID_USER"}, status=401)
        
        s3r   = boto3.resource('s3',
                                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
        s3r.Object(AWS_STORAGE_BUCKET_NAME,moviepost.storage_path).delete()
        moviepost.delete()
        
        return JsonResponse({"message":"deleted!"}, status=204)


class MoviePostLike(View):
    @access_token_check
    def post(self,request,movie_id,moviepost_id):
        user = request.user
        
        if UserPostLike.objects.filter(review_id=moviepost_id,user_id=user.id).exists():
            UserPostLike.objects.get(review_id=moviepost_id,user=user.id).delete()
            
            return JsonResponse({"message":"like_deleted!"}, status=204)
        
        UserPostLike.objects.create(review_id=moviepost_id,user_id=user.id)
        
        return JsonResponse({"message":"like_created!"}, status=201)
        

class ReviewView(View):
    @access_token_check
    def post(self,request,movie_id):
        try:
            data       = json.loads(request.body)
            content    = data['content']
            user       = request.user
            movie      = Movie.objects.get(id=movie_id)
            
            MovieReview.objects.create(
                movie         = movie,
                user          = user,
                content       = content,
            )
            
            return JsonResponse({"message": "created!"}, status=201)
            
        except KeyError:
            return JsonResponse({'message:':'key_error!'},status=400)


        
class ReviewDetailView(View):
    def get(self,request,movie_id,review_id):
        review    = MovieReview.objects.select_related('user').get(id=review_id)
        movie     = Movie.objects.get(id=movie_id)
        review = {
            "movie_name" : movie.name,
            "user"       : review.user.nickname,
            "content"    : review.content,
            'like'       : review.userreviewlike_set.all().count()
        }
        
        return JsonResponse({"review":review}, status=201)
    
    @access_token_check
    def patch(self,request,movie_id,review_id):
        try:
            data       = json.loads(request.body)
            content    = data.get('content')
            user       = request.user

            review = MovieReview.objects.get(id=review_id, user_id = request.user.id)
            
            review.content = content
            review.save()
            
            return JsonResponse({"message": "updated!"}, status=201)   
        except MovieReview.DoesNotExist:
            return JsonResponse({"message":"Review does not exist!"}, status=404)
        
        except KeyError:
            return JsonResponse({'message:','key_error'},status=400)
        
    @access_token_check
    def delete(self,request,movie_id,review_id):
        try:
            MovieReview.objects.filter(id=review_id, user_id = request.user.id).delete()
            
        except MovieReview.DoesNotExist:
            return JsonResponse({"message":"Review does not exist!"}, status=404)
        
        return JsonResponse({"message":"deleted!"}, status=204)


class ReviewLike(View):
    @access_token_check
    def post(self,request,movie_id,review_id):
        user = request.user
        
        if UserReviewLike.objects.filter(review_id=review_id,user_id=user.id).exists():
            UserReviewLike.objects.get(review_id=review_id,user=user.id).delete()
            
            return JsonResponse({"message":"like_deleted!"}, status=204)
        
        UserReviewLike.objects.create(review_id=review_id,user_id=user.id)
        
        return JsonResponse({"message":"like_created!"}, status=201)

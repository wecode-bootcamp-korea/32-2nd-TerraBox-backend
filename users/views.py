import json, jwt, requests

from django.http       import JsonResponse
from django.views      import View
from datetime          import datetime,timedelta
from TerraBox.settings import ALGORITHM,SECRET_KEY

from users.models import User

def get_kakao_info(token):
    kakao_url = "https://kapi.kakao.com/v2/user/me"
    header ={
        "Content-Type"  : "application/x-www-form-urlencoded",
        "Authorization" : token,
    }

    return requests.get(kakao_url,headers=header).json()

class KakaoLoginView(View):

    def post(self,request):
        try:
            token = f"Bearer {request.headers.get('Authorization')}"

            response          = get_kakao_info(token)
            kakao_id          = response.get('id')
            nickname          = response.get('properties').get('nickname')
            profile_image_url = response.get('kakao_account').get('profile').get('thumbnail_image_url')
            email             = response.get('kakao_account').get('email')
            
            user,created = User.objects.get_or_create(
                kakao_id=kakao_id, 
                defaults = {
                    "nickname"         :nickname,
                    "profile_image_url":profile_image_url,
                    "email"            :email,
                }
            )

            expiration = timedelta(seconds=3600)
            token_expiration_time = datetime.utcnow() + expiration
            
            jwt_access_token = jwt.encode({'id':user.id,'exp':token_expiration_time},SECRET_KEY,algorithm=ALGORITHM)

            return JsonResponse({'message':'success!',
            'JWT_ACCESS_TOKEN' :jwt_access_token,
            "profile_image_url":user.profile_image_url,
            "nickname":user.nickname,
            "email":user.email},status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
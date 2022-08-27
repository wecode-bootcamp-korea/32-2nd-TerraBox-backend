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


class GoogleLoginView(View):
    def post(self,request):
        try:
            token    = request.headers["Authorization"] # 프론트엔드에서 HTTP로 들어온 헤더에서 id_token(Authorization)을 변수에 저장
            url      = 'https://oauth2.googleapis.com/tokeninfo?id_token=' # 토큰을 이용해서 회원의 정보를 확인하기 위한 gogle api주소
            response = requests.get(url+token) #구글에 id_token을 보내 디코딩 요청
            user     = response.json() # 유저의 정보를 json화해서 변수에 저장
            
            expiration = timedelta(seconds=3600)
            token_expiration_time = datetime.utcnow() + expiration

            if User.objects.filter(google_id = user['sub']).exists(): #기존에 가입했었는지 확인
                user_info           = User.objects.get(google_id=user['sub']) # 가입된 데이터를 변수에 저장
                encoded_jwt         = jwt.encode({'id':user.id,'exp':token_expiration_time},SECRET_KEY,algorithm=ALGORITHM)
                none_member_type    = 1

                return JsonResponse({ # 프론트엔드에게 access token과 필요한 데이터 전달
                    'access_token'  : encoded_jwt.decode('UTF-8'),
                    'user_name'     : user['name'],
                    'user_type'     : none_member_type,
                    'user_pk'       : user_info.id
                }, status = 200)
            else:
                new_user_info = User( # 처음으로 소셜로그인을 했을 경우 회원의 정보를 저장함(email이 없을 수도 있다 하여, 있으면 저장하고, 없으면 None으로 표기)
                    social_login_id = user['sub'],
                    name            = user['name'],
                    email           = user.get('email', None)
                )
                new_user_info.save() # DB에 저장

                encoded_jwt         = jwt.encode({'id':user.id,'exp':token_expiration_time},SECRET_KEY,algorithm=ALGORITHM)
                
        
                return JsonResponse({ # DB에 저장된 회원의 정보를 access token과 같이 프론트엔드에게 전달
                'access_token'      : encoded_jwt.decode('UTF-8'),
                'user_name'         : new_user_info.name,
                'user_type'         : none_member_type,
                'user_pk'           : new_user_info.id,
                }, status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
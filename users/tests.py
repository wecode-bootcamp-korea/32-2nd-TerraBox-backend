from django.test     import TestCase,Client
from unittest.mock    import patch, MagicMock
from datetime        import datetime,timedelta
from users.models    import User
import json, jwt
from TerraBox.settings import *


class KaKaoSignTest(TestCase):
    def setUp(self):
        
        User.objects.create(
            id= 1,
            nickname = 'YB',
            kakao_id = 12345,
            email = "test@email.com",
            profile_image_url = 'http://test@profile_image'
        )
        # 필요없음 > 필요함. 없어도 될줄 알았는데, 없으면 db가 통일되어 있어서 , 기존에 아이디가 만들어졌다 사라져서 id=1 이 될 수 없음
        # 즉, id =2 가 되어서 jwt토큰이 맛탱이감
        # 아니면 id=2를 jwt토큰에 넣어주던가
        
    def tearDown(slef):
        User.objects.all().delete()

    @patch('users.views.requests') #users.views에 등장하는 모든 requests의 값을 magicmock이라는 객체로 바꿔줌
    def test_success_kakaologin_new_user(self,mocked_requests):
    #mocked_requests는 실제 view에 등장한느 request와 아무런 관련이 없다! 그냥 사용하기 위해 만들어준 객체일 뿐임
        client = Client()

        class MockedResponse:
            def json(self):
                return {
        "id": 12345,
        "connected_at": "2022-05-12T16:57:36Z",
        "properties": {
            "nickname": "YB"
        },
        "kakao_account": {
            "profile": {
                "nickname": "김영빈",
                "thumbnail_image_url": "http://test@profile_image",
                "profile_image_url": "http://test@profile_image",
            },
            "email": "test@email.com"
        }
    }
        mocked_requests.get = MagicMock(return_value=MockedResponse())
        #users.views.requests대신에 mocked_requests라는 게 들어가고,
        #mocked_requests.get에 Mockedresponse가 들어간다
        #mockedResponse는 결국 mockedResponse.json()와 같은 식으로 호출될 꺼니까, json함수를 넣어준 것임
        
        headers = {"HTTP_Authorization": "access_token"}
        response = client.post('/users/login',**headers)
        
        expiration = timedelta(seconds=3600)
        token_expiration_time = datetime.utcnow() + expiration
        
        jwt_access_token = jwt.encode({
            'id'  : 1,
            'exp' : token_expiration_time},SECRET_KEY,algorithm=ALGORITHM)
        
        self.assertEqual(response.status_code,201)
        #status code는 예외임. 그냥 code로 딸려나오는 듯
        
        #json response >> json으로 풀어줘야 함
        self.assertEqual(response.json(),{
            'message'           : 'success!',
            'JWT_ACCESS_TOKEN'  : jwt_access_token,
            'profile_image_url' : 'http://test@profile_image', #설정을 바보같이 해놔서 프로필이 아니라 썸네일을 가져옴
            'nickname'          : 'YB',
            'email'             : "test@email.com",
        })
        #client로 요청을 보낸 결과가 json response > json으로 풀어줌 > 풀어준 내용이 mockdata를 만들면서 의도한 내용과 일치하는지를 확인해주는 것임
        
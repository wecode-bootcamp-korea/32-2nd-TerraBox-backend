from django.test     import TestCase,Client
from unittest.mock    import patch, MagicMock
from datetime        import datetime,timedelta
from users.models    import User
import json, jwt
from TerraBox.settings import *


class KaKaoSignTest(TestCase):
    def setUp(self):
        pass
        # User.objects.create(
        #     id= 1,
        #     name = 'yb',
        #     kakao_id = 12345,
        #     email = 'test@test.com',
        #     profile_image = 'http://test@test'
        # )
    def tearDown(slef):
        User.objects.all().delete()

    @patch('users.views.requests') #users.views에 등장하는 모든 requests의 값을 magicmock이라는 객체로 바꿔줌
    def test_success_kakaologin_new_user(self,mocked_requests):
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
        
        print(response.json())
        
        #json response >> json으로 풀어줘야 함
        self.assertEqual(response.json(),{
            'message'           : 'success!',
            'JWT_ACCESS_TOKEN'  : jwt_access_token,
            'profile_image_url' : 'http://test@profile_image', #설정을 바보같이 해놔서 프로필이 아니라 썸네일을 가져옴
            'nickname'          : 'YB',
            'email'             : "test@email.com",
        })
        
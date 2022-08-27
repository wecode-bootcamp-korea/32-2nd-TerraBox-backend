from django.test       import TestCase, Client, TransactionTestCase
from datetime          import datetime,timedelta
from TerraBox.settings import *
from reviews.models    import MovieReview
from movies.models     import Movie
from users.models      import User
import jwt, json

#class ReviewViewTest(TestCase): #두개 이상일 때 에러가 발생함 > 이유는 잘 모르겠다.. 찾아봐야 할 듯?
class ReviewViewTest(TestCase):
    def setUp(self):
        Movie.objects.create(
            id             = 1,
            name           = 'test_name1',
            eng_name       = 'test_eng1',
            description    = 'des1',
            detail_text    = 'detail1',
            age_grade      = 'test@test.com',
            is_subtitle    = True,
            screening_type = 2,
            preview_url    = 'test@previewb.com',
            running_time   = 120,
            )
        
        User.objects.create(
            id =1,
            kakao_id=123456,
            nickname = 'tester',
            email = 'test@user.com',
            profile_image_url = 'http://test.com',
        )

    def tearDown(self):
        Movie.objects.all().delete()
        User.objects.all().delete()
        MovieReview.objects.all().delete()
        

    def test_success_reviewview_post_create_new_review(self):
        client = Client()
        
        expiration = timedelta(seconds=3600)
        token_expiration_time = datetime.utcnow() + expiration
        jwt_access_token = jwt.encode({'id':User.objects.last().id,'exp':token_expiration_time},SECRET_KEY,algorithm=ALGORITHM)
        
        content = {
            'content' : 'test_content'
        }
        
        headers = {'HTTP_Authorization':jwt_access_token}
        response = client.post(
            '/movies/1/reviews',#요청 url. 맨앞에 / 꼭 붙여줘야 한다!
            json.dumps(content),#content를 json형태로 보내주기 위해 json.dumps로 해줘야 함
            content_type='application/json',#json형태로 보내주므로 content_type을 json으로 선택
            **headers,#토큰을 딕셔너리 키워그 방식으로 전달
        )
        
        self.assertEqual(response.status_code,201)#코드를 비교
        self.assertEqual(response.json(),{#메세지를 비교
            "message": "created!"
        })
        
    def test_fail_reviewview_post_create_key_error(self):
        client = Client()
        
        content = {
            'error_key' : 'test_content'
        }
        expiration = timedelta(seconds=3600)
        token_expiration_time = datetime.utcnow() + expiration
        jwt_access_token = jwt.encode({'id':User.objects.last().id,'exp':token_expiration_time},SECRET_KEY,algorithm=ALGORITHM)
        
        headers = {'HTTP_Authorization':jwt_access_token}
        response = client.post(
            '/movies/1/reviews',#요청 url. 맨앞에 / 꼭 붙여줘야 한다!
            json.dumps(content),#content를 json형태로 보내주기 위해 json.dumps로 해줘야 함
            content_type='application/json',#json형태로 보내주므로 content_type을 json으로 선택
            **headers,#토큰을 딕셔너리 키워그 방식으로 전달
        )

        self.assertEqual(response.status_code,400)#코드를 비교
        self.assertEqual(response.json(),{'message:':'key_error!'})
from django.test    import TestCase, Client
from django.conf    import settings
from unittest.mock    import patch, MagicMock
from users.models     import User
from django.conf      import settings
from we_eats.settings import SECRET_KEY, ALGORITHM
from datetime         import datetime, timedelta
class KakaoSignTest(TestCase):
    def setUp(self):
        User.objects.create(
            id            = 1,
            name          = "민석",
            kakao_id      = 123456789,
            profile_image = "http://test.jpg"
        )
    def tearDown(self):
        User.objects.all().delete()
    @patch("core.utils.requests")
    def test_kakao_signin_success(self, mocked_kakao_user_info):
        client = Client()
        class MockedResponse:
            def json(self):
                return {
                    "id": 123456789,
                    "properties": {
                        "nickname": "민석",
                        "profile_image": "http://test.jpg"
                    },
                }
        mocked_kakao_user_info.get = MagicMock(return_value=MockedResponse())
        headers  = {"HTTP_Authorization": "fake_access_token"}
        response = client.post("/users/login", **headers)
        access_token = jwt.encode({'id':1, 'exp':datetime.utcnow() + timedelta(days=1)}, SECRET_KEY, algorithm=ALGORITHM)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'access_token' : access_token})
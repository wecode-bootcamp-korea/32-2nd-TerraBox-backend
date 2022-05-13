from django.test import TestCase,Client
from django.unittest import mock,patch
import json, bcrypt

@patch('users.views.requests') #users.views에 등장하는 모든 requests의 값을 magicmock이라는 객체로 바꿔줌
def test_success_kakaologin(self,mocked_requests):
    client = Client()

    class MockedResponse:
        def json(self):
            return {
    "id": 2239940166,
    "connected_at": "2022-05-12T16:57:36Z",
    "properties": {
        "nickname": "김영빈"
    },
    "kakao_account": {
        "profile_nickname_needs_agreement": false,
        "profile_image_needs_agreement": false,
        "profile": {
            "nickname": "김영빈",
            "thumbnail_image_url": "http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_110x110.jpg",
            "profile_image_url": "http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_640x640.jpg",
            "is_default_image": true
        },
        "has_email": true,
        "email_needs_agreement": false,
        "is_email_valid": true,
        "is_email_verified": true,
        "email": "colock123@gmail.com"
    }
}
    mocked_requests.get = MagicMock(return_value=MockedResponse())
    #users.views.requests대신에 mocked_requests라는 게 들어가고,
    #mocked_requests.get에 Mockedresponse가 들어간다
    #mockedResponse는 결국 mockedResponse.json()와 같은 식으로 호출될 꺼니까, json함수를 넣어준 것임
    
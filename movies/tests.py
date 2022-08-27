from django.test import TestCase, Client
from .models     import Movie,MovieImage

class MovieListDetailTest(TestCase):
    def setUp(self):

        test_movies_list = [
            Movie(
            id             = 1,
            name           = 'test_name1',
            eng_name       = 'test_eng1',
            description    = 'des1',
            detail_text    = 'detail1',
            age_grade      = 'test@test.com',
            is_subtitle    = True,
            screening_type = 2,
            preview_url    = 'test@preview.com',
            running_time   = 120,
            ),
            Movie(
            id             = 2,
            name           = 'test_name2',
            eng_name       = 'test_eng2',
            description    = 'des2',
            detail_text    = 'detail2',
            age_grade      = 'test@test.com',
            is_subtitle    = True,
            screening_type = 2,
            preview_url    = 'test@preview.com',
            running_time   = 220,
            ),
        ]

        test_images_list = [
            MovieImage(
            movie_id=1,
            stillcut_url='test_img1'
            ),
            MovieImage(
            movie_id=2,
            stillcut_url='test_img2'
            ),
        ]

        Movie.objects.bulk_create(test_movies_list)
        MovieImage.objects.bulk_create(test_images_list)

    def tearDown(self):
        Movie.objects.all().delete()
    
    def test_success_get_product_list(self):
        client = Client()
        response = client.get('/movies')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{
            "result":[
                {
                    'id'           : 1,
                    'name'         : 'test_name1',
                    'stillcut_url' : 'test_img1'
                },
                {
                    'id'           : 2,
                    'name'         : 'test_name2',
                    'stillcut_url' : 'test_img2'
                }
            ],
        })
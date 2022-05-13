from django.db   import models
from core.models import TimeStampedModel

class User(TimeStampedModel):
    kakao_id                   = models.PositiveBigIntegerField(unique=True)
    nickname                   = models.CharField(max_length=50)
    profile_image_url          = models.CharField(max_length=200)
    profile_image_storage_path = models.CharField(max_length=200,null=True)
    email                      = models.CharField(max_length=150,null=True)

    class Meta:
        db_table = 'users'
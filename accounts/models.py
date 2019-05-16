from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movie.models import Movie
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40,blank=True)
    image = ProcessedImageField(
            blank = True,
            upload_to = 'profile/images', #저장위치
            processors=[ResizeToFill(600,600)],# 처리할 작업 목록
            format='JPEG',#포맷 저장
            options={'quality':90},#옵션
        )
        
# Create your models here.
class User(AbstractUser):
    from_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='to_user')
    movies = models.ManyToManyField(Movie, related_name='users')
    is_logined = models.BooleanField(default=True,blank=True)
    grade = models.IntegerField(default=0)
    
class Message(models.Model):
    message_from = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="messagefrom",on_delete=models.CASCADE)
    message_to = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="messageto",on_delete=models.CASCADE)
    content = models.TextField()
from django.db import models
from django.conf import settings

class Popular(models.Model):
    date = models.TextField()
    
class Genre(models.Model):
    name = models.TextField()
    genrenum = models.IntegerField()
    def __str__(self):
        return self.name
        
class Actor(models.Model):
    name = models.TextField()
    image = models.TextField()
    tmdbid = models.IntegerField()
    
class Movie(models.Model):
    title = models.TextField()
    popularity = models.TextField()
    image = models.TextField()
    original_title = models.TextField()
    original_language = models.TextField()
    release_date = models.IntegerField()
    tmdbrating = models.FloatField(blank=True)
    myrating = models.IntegerField()
    genre = models.ManyToManyField(Genre,related_name="movie",blank=True)
    showTm = models.IntegerField()
    overview = models.TextField()
    ispopular = models.ForeignKey(Popular,on_delete="SET_NULL",null=True)
    actors = models.ManyToManyField(Actor,through='Character')
    tmdbid = models.IntegerField()
    video = models.TextField()
    
    
class Character(models.Model):
    name = models.TextField()
    actor = models.ForeignKey(Actor,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
# Create your models here.

    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    PRIORITIES = ((i, str(i)+'★') for i in range(11))
    score = models.IntegerField(default=5, choices=PRIORITIES)
    likeusers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likecomments")
    dislikeusers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dislikecomments")
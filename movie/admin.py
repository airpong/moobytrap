from django.contrib import admin
from .models import Movie,Genre,Popular,Actor,Character
from accounts.models import Profile
# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Popular)
admin.site.register(Actor)
admin.site.register(Character)
admin.site.register(Profile)
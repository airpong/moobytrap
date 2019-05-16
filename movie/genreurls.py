from django.urls import path
from . import views

app_name = 'genre'

urlpatterns=[
    path('',views.genrelist,name="genrelist"),
    path('make/',views.genremake,name="genremake"),
    path('<int:genre_id>',views.genremovie,name="genremovie"),
]
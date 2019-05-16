from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

app_name = 'movies'

urlpatterns = [
    path('',views.index,name='index'),
    path('search/',views.moviesearch,name="moviesearch"),
    path('make/',views.makeMovieList,name="makeMovieList"),
    path('somemovie/',views.somemovie,name="somemovie"),
    path('weekdate/',views.weekmovie,name="weekmovie"),
    path('make/<int:movie_id>/',views.makeMovie,name="makeMovie"),
    path('<int:movie_id>/',views.moviedetail,name="moviedetail"),
    path('<int:movie_id>/comment/create/',views.commentcreate,name="commentcreate"),
    path('<int:movie_id>/comment/<int:comment_id>/delete/',views.commentdelete,name="commentdelete"),
    path('<int:comment_id>/comment/like/', views.commentlike, name="commentlike"),
    path('<int:comment_id>/comment/dislike/', views.commentdislike, name="commentdislike"),
    path('<int:movie_id>/comment/<int:comment_id>/update/',views.commentupdate,name="commentupdate"),
    path('docs/', get_swagger_view(title='api')),
    path('<int:movie_pk>/scores/', views.create_score),
    path('<int:movie_pk>/api/', views.getmovie),
]
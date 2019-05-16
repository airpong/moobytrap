from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.lists, name='lists'),
    path('<int:user_pk>/', views.detail, name='detail'),
    path('<int:user_pk>/follow', views.follow, name='follow'),
    path('<int:user_pk>/followers', views.followers, name='followers'),
    path('<int:user_pk>/followings', views.followings, name='followings'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('loginuser/',views.loginuser,name='loginuser'),
    path('test',views.test,name="test"),
    path('profile/create/',views.profile_create,name='profile_create'),
    path('profile/update/',views.profile_update,name='profile_update'),
    path('messageget/',views.messageget,name="messageget"),
    path('<int:movie_pk>/moviefollow/', views.moviefollow, name='moviefollow'),
    path('createmessage/<int:from_id>/<int:to_id>/',views.messagecreate,name="messagecreate"),
]

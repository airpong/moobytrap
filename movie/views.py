import os
import sys
import requests
import urllib
import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie,Genre, Comment, Popular, Actor, Character
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# 자신이 없다.....
from .forms import CommentForm
from .serializers import ScoreSerializer, MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@login_required
def index(request):
    today = Popular.objects.get(date='20190516')
    movies = Movie.objects.filter(ispopular=today)
    movie1 = movies[0:5]
    movie2 = movies[5:10]
    users = get_user_model().objects.all().order_by('-grade')[0:3]
    userrecomend = {}
    for user in users:
        userrecomend[user]=[]
        comments = user.comment_set.all().order_by('-score')[0:3]
        for comment in comments:
            userrecomend[user].append(comment.movie)
    comments = request.user.comment_set.all()
    genrelist = {}
    for comment in comments:
        for genre in comment.movie.genre.all():
            if genrelist.get(genre.name):
                genrelist[genre.name]+=1
            else:
                genrelist[genre.name]=1
    if not genrelist:
        targetgenre = "액션"
    else:
        targetgenre = max(genrelist,key=lambda x:genrelist[x])
    genre = Genre.objects.get(name=targetgenre)
    genremovie1 = genre.movie.all().order_by('-tmdbrating')[0]
    genremovie2 = genre.movie.all().order_by('-tmdbrating')[1]
    genremovie3 = genre.movie.all().order_by('-tmdbrating')[2]
    
    
    return render(request,'index.html',{'movie1':movie1,'movie2':movie2,'userrecommend':userrecomend,'genrerecommnd1':genremovie1,'genrerecommnd2':genremovie2,'genrerecommnd3':genremovie3,'genre':targetgenre})
@login_required    
def moviesearch(request):
    if request.user.username != 'admin':
        return redirect('movies:index')
    if request.method=="GET":
        return render(request,'search.html')
    else:
        movienm = request.POST.get('movienm')
        res = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key=f6975886ffe61184df0d21e79ee0aa7d&language=ko-KR&query={movienm}').json()
        result = []
        for movie in res['results']:
            if movie["poster_path"]:
                movie['image']='https://image.tmdb.org/t/p/w600_and_h900_bestv2'+movie["poster_path"]
            else:
                movie['image']=""
        return render(request,'resultshow.html',{'movies':res['results']})
        
def genrelist(request):
    genres = Genre.objects.all()
    return render(request,'genrelist.html',{'genres':genres})
    
def genremake(request):
    res = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=f6975886ffe61184df0d21e79ee0aa7d&language=ko-KR').json()
    for genre in res['genres']:
        gr = Genre(genrenum=genre['id'],name=genre['name'])
        gr.save()
    return redirect('genre:genrelist')
    
def weekmovie(request):
    date = '20190516'
    newrank = Popular(date=date)
    newrank.save()
    res = requests.get('https://api.themoviedb.org/3/movie/now_playing?api_key=f6975886ffe61184df0d21e79ee0aa7d&language=ko-KR&page=1').json()['results']
    for i in range(10):
        tmpmovie = makeMovieFunction(res[i]["id"])
        tmpmovie.ispopular = newrank
        tmpmovie.save()
        
    
def makeMovieFunction(movie_id):
    res = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f6975886ffe61184df0d21e79ee0aa7d&language=ko-KR').json()
    actors = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=f6975886ffe61184df0d21e79ee0aa7d')
    video = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=f6975886ffe61184df0d21e79ee0aa7d&language=ko-KR').json()
    try:
        print(res['id'])
        movie = Movie.objects.get(tmdbid=res['id'])
        return movie
    except:
        movieactor = makeactor(actors)
        movie = Movie()
        movie.title = res['title']
        movie.popularity = res['popularity']
        movie.image = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2'+res["poster_path"]
        movie.original_title = res['original_title']
        movie.original_language = res['original_language']
        movie.release_date = int(''.join(res['release_date'].split('-')))
        movie.tmdbrating = res['vote_average']
        movie.myrating = 0
        movie.showTm = res['runtime']
        movie.overview = res['overview']
        print(video)
        if video['results']:
            movie.video = "https://www.youtube.com/embed/"+video['results'][0]['key']
        movie.tmdbid = movie_id
        movie.save()
        for moviegenre in res['genres']:
            tmpgenre = get_object_or_404(Genre,genrenum=moviegenre['id'])
            movie.genre.add(tmpgenre)
        for actor in range(5):
            character = Character()
            
            character.name = actors.json()['cast'][actor]["character"]
            character.actor = movieactor[actor]
            character.movie = movie
            print("A",character)
            character.save()
            
        movie.save()
        return movie
        
def makeactor(actors):
    actors = actors.json()
    result = []
    for actor in range(5):
        try:
            actor = get_object_or_404(Actor,tmdbid=actors['cast'][actor]['id'])
            result.append(actor)
        except:
            tmpactor = Actor(name=actors['cast'][actor]['name'],tmdbid=actors['cast'][actor]['id'])
            tmpactor.image = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/"+actors['cast'][actor]['profile_path']
            tmpactor.save()
            result.append(tmpactor)
    return result
    
def makeMovie(request,movie_id):
    makeMovieFunction(movie_id)
    return redirect('movies:index')
    
def moviedetail(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    datestring = str(movie.release_date)
    tmdbrating = round(movie.tmdbrating)
    half = movie.tmdbrating*10%10
    popularity = format(int(movie.popularity.replace('.', '')), ',')
    comment_form = CommentForm()
    return render(request,'moviedetail.html',{'movie':movie, 'comment_form':comment_form, 'range':[2,4,6,8,10], 'datestring':datestring, 'tmdbrating':tmdbrating, 'half':half, 'popularity':popularity,})
    
def makeMovieList(request):
    for i in range(1,2):
        res = requests.get(f'https://api.themoviedb.org/3/movie/top_rated?api_key=f6975886ffe61184df0d21e79ee0aa7d&language=ko-KR&page={i}').json()
        for movie in res['results']:
            makeMovieFunction(movie['id'])
    return redirect('movies:index')
        
    
def genremovie(request,genre_id):
    genre = get_object_or_404(Genre,id=genre_id)
    movies = genre.movie.all().order_by('tmdbrating')
    return render(request,'somemovie.html',{'movies':movies})
# def movieapi():
#     client_id = "4aa7068731f45f102e26b2ed22438067"
#     abc=requests.get(f'http://www   .kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={client_id}&targetDt=20190511')
#     abc = abc.json()
#     result = []
#     for moviename in abc['boxOfficeResult']['dailyBoxOfficeList']:
#         result.append(moviename['movieNm'])
#     return result
    
# def naver(request):
#     lst = movieapi()
#     for moviename in lst:
#         encText = urllib.parse.quote(moviename)
#         res = requests.get(f'https://openapi.naver.com/v1/search/movie.json?query={encText}&display=10', headers={'X-Naver-Client-Id': 'NQJ4y1Kw8olmgRH7MTZW', 'X-Naver-Client-Secret': 'l9bIc2f2KA'})
#         data = res.json()
#         data['items'][0]['pubDate'] = int(data['items'][0]['pubDate'])
#         data['items'][0]['userRating'] = float(data['items'][0]['userRating'])
#         movie = Movie()
#         movie.title = data['items'][0]['title']
#         movie.link = data['items'][0]['link']
#         movie.image = data['items'][0]['image']
#         movie.subtitle = data['items'][0]['subtitle']
#         movie.pubDate = data['items'][0]['pubDate']
#         movie.director = data['items'][0]['director']
#         movie.actor = data['items'][0]['actor']
#         movie.userRating = data['items'][0]['userRating']
        
#         movie.save()
#     movies = Movie.objects.all()
#     for movie in movies:
#         print(movie.title)
    
#     return render(request, 'naver.html', {'data':data})


def commentcreate(request, movie_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user_id = request.user.id
        comment.movie_id = movie_id
        comment.save()
    return redirect('movies:moviedetail', movie_id)
    
def commentupdate(request,movie_id,comment_id):
    comment = Comment.objects.get(id=comment_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST,instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            return redirect('movies:moviedetail',movie_id)
    else:
        comment_form = CommentForm(instance=comment)
    return render(request, 'form.html',{'comment_form':comment_form})
        
@api_view(['POST'])
def create_score(request, movie_pk):
    serializer = ScoreSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie_id=movie_pk, user_id=request.user.id)
        return Response({"message":"작성되었습니다."})


@api_view(['GET'])
def getmovie(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

    
def commentdelete(request, movie_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('movies:moviedetail', movie_id)
    

def commentlike(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likeusers.all():
        comment.likeusers.remove(request.user)
        comment.user.grade -= 1
        comment.user.save()
    else:
        comment.likeusers.add(request.user)
        comment.user.grade += 1
        comment.user.save()
    return redirect('movies:moviedetail', comment.movie.id)
    
    
def commentdislike(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.dislikeusers.all():
        comment.dislikeusers.remove(request.user)
        comment.user.grade += 1
        comment.user.save()
    else:
        comment.dislikeusers.add(request.user)
        comment.user.grade -= 1
        comment.user.save()
    return redirect('movies:moviedetail', comment.movie.id)
    
def somemovie(request):
    keyword = request.GET.get('keyword')
    movies = Movie.objects.filter(title__contains=keyword)
    return render(request,'somemovie.html',{'movies':movies})
    

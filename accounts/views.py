from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .models import User,Profile,Message
from .forms import UserCustomCreationForm, UserCustomChangeForm,ProfileForm
from django.contrib.auth import get_user_model
from movie.models import Movie
from .serializers import MessageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
# Create your views here.
@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        user_form = UserCustomCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            Profile.objects.create(user=user)   #Profile 생성
            auth_login(request, user)
            return redirect('movies:index')
    else:
        user_form = UserCustomCreationForm()
    context = {'form': user_form}
    return render(request, 'accounts/forms.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            nowuser = get_object_or_404(get_user_model(),id=request.user.id)
            nowuser.is_logined = True
            nowuser.save()
            return redirect('movies:index')
    else:
        login_form = AuthenticationForm()
    context = {'form': login_form}
    return render(request, 'accounts/forms.html', context)

@login_required
def logout(request):
    nowuser = get_object_or_404(get_user_model(),id=request.user.id)
    nowuser.is_logined = False
    nowuser.save()
    auth_logout(request)
    return redirect('movies:index')
    
    
def lists(request):
    result = {}
    users = User.objects.all().order_by('-grade')
    for user in users:
        result[user]=[]
        comments = user.comment_set.all()
        for idx in range(min(2,len(user.comment_set.all()))):
            result[user].append(comments[idx])
    print(result)
    return render(request, 'accounts/lists.html', {'users':result})
    

def detail(request, user_pk):
    person = get_object_or_404(User, id=user_pk)
    recommends = {}
    for following in person.to_user.all():
        if max(following.comment_set.all(), key=lambda x: x.score, default=0):
            temp_max = max(following.comment_set.all(), key=lambda x: x.score).score
            temp = []
            for comment in following.comment_set.all():
                if comment.score == temp_max:
                    temp.append(comment)
            recommends.update({following.username:temp})
    
    jangba = person.movies.all()[0:8]
    jangba2 = []
    jang = []
    count = 0
    for movie in person.movies.all():
        if count >= 8:
            jang.append(movie)
            count += 1
            if count%8 == 0:
                jangba2.append(jang[:])
                jang = []
        else:
            count += 1
    jangba2.append(jang[:])

    return render(request, 'accounts/detail.html', {'person':person, 'recommends':recommends, 'jangba':jangba, 'jangba2':jangba2,})
    
    
def update(request):
    if request.method == 'POST':
        user_change_form = UserCustomChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('accounts:detail', request.user.id)
    else:
        user_change_form = UserCustomChangeForm(instance=request.user)
    return render(request, 'accounts/update.html', {
        'user_change_form':user_change_form,
    })


@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('movies:index')
    return render(request, 'accounts/delete.html')

    
def follow(request, user_pk):
    person = get_object_or_404(User, id=user_pk)
    if request.user in person.from_user.all():
        person.from_user.remove(request.user)
    else:
        person.from_user.add(request.user)
    return redirect('accounts:detail', user_pk)
    
    
def followers(request, user_pk):
    person = get_object_or_404(User, id=user_pk)
    return render(request, 'accounts/follow.html', {'person':person, 'follow':'followers'})
    
    
def followings(request, user_pk):
    person = get_object_or_404(User, id=user_pk)
    return render(request, 'accounts/follow.html', {'person':person, 'follow':'followings'})


def moviefollow(request, movie_pk):
    movie = get_object_or_404(Movie, id=movie_pk)
    if request.user in movie.users.all():
        movie.users.remove(request.user)
    else:
        movie.users.add(request.user)
    return redirect('movies:moviedetail', movie_pk)
    
def loginuser(request):
    users = get_user_model().objects.all()
    result = []
    for user in users:
        if user.is_logined:
            result.append(user)
    print(result)
    return render(request, 'accounts/loginuser.html', {'users':result})
    
    
def profile_create(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user_id = request.user.id
            profile.save()
            return redirect('accounts:detail',request.user.id)
    else:
        profile_form = ProfileForm()
    return render(request,'accounts/profile_create.html',{'profile_form':profile_form})
    
    
@login_required    
def profile_update(request):
    print('a')
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('accounts:detail',request.user.id)
    else:
        print('c')
        profile_form = ProfileForm(instance=profile)
    print('b')
    return render(request,'accounts/profile_update.html',{'profile_form':profile_form})    
def test(request):
    return render(request,'accounts/test.html')
    
@api_view(['POST'])
def messagecreate(request,from_id,to_id):
    serializer =  MessageSerializer(data=request.data)
    print("Abcd",serializer)
    if serializer.is_valid(raise_exception=True):
        print("Abcdefg")
        user1 = get_user_model().objects.get(id=from_id)
        user2 = get_user_model().objects.get(id=to_id)
        serializer.save(message_from=user1,message_to=user2)
        print("Abcdefghijklmn")
        return Response(serializer.data)
        
@api_view(['GET'])
def messageget(request):
    messages = Message.objects.filter(Q(message_from=request.user) | Q(message_to=request.user))
    serializer = MessageSerializer(messages,many=True)
    print(serializer.data)
    return Response(serializer.data)
    
    
    
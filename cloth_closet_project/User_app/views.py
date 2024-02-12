from django.shortcuts import render, redirect,get_object_or_404
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login,logout
# Create your views here.
from Cloth_app.forms import *
from User_app.models import *
from Cloth_app.models import *
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.urls import resolve
from django.contrib import messages
def index(request):
    return render(request, 'Main/index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = '登録できません'
    else:
        form = SignUpForm()
    return render(request,'user/signup.html', {'form': form, 'msg': msg})


def login_view(request):

    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_user:
                login(request, user)
                messages.success(request,'ログインしました')

                return redirect('customer')
            elif user is not None and user.is_company:
                login(request, user)
                messages.success(request,'ログインしました')

                return redirect('employee')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'user/signin.html', {'form': form, 'msg': msg})


def singout(rq):
    logout(rq)
    return redirect('login_view')

def admin(request):
    return render(request,'admin.html')


def customer(request):
    user = request.user

    follow_status = Follow.objects.filter(following=user).exists()

    posts = Stream.objects.filter(user=user)
    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)
        
    post_items = Post.objects.filter(user=user).order_by('-posted')


    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

    context = {
        'post_items': post_items,
        'follow_status': follow_status,
        # 'all_users': all_users,  # Not used in the context
        # 'users_paginator': users_paginator,  # Not used in the context
    }
    
    return render(request,'Seller/sellerhhome.html',context)


def employee(request):
    user = request.user

    follow_status = Follow.objects.filter(following=user).exists()

    posts = Stream.objects.filter(user=user)
    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)
        
    post_items = Post.objects.all().order_by('-posted')


    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

    context = {
        'post_items': post_items,
        'follow_status': follow_status,
        # 'all_users': all_users,  # Not used in the context
        # 'users_paginator': users_paginator,  # Not used in the context
    }
    return render(request, 'company/home.html', context)

def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')


    
    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'posts_paginator':posts_paginator,
        'follow_status':follow_status,
        # 'count_comment':count_comment,
    }
    return render(request, 'user/profile.html', context)

def CompanyUserProfile(request, username):
    user = get_object_or_404(User, username=username)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')


    
    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'posts_paginator':posts_paginator,
        'follow_status':follow_status,
        # 'count_comment':count_comment,
    }
    return render(request, 'company/company_profile.html', context)
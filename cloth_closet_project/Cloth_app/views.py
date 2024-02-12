from django.shortcuts import render,redirect,get_object_or_404
from Cloth_app.forms import *
from User_app.models import *
from Cloth_app.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required

def index(request):
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
    return render(request, 'main/home.html', context)



from django.shortcuts import redirect
@login_required

def NewPost(request):
    user = request.user

    # Check if the user is a customer
    if not user.is_authenticated or not user.is_user:
        return redirect('customer')  # Redirect to home or any other page

    tags_obj = []
    
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            description=form.cleaned_data.get('description')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption,description=description, user=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('customer')
    else:
        form = NewPostForm()
    context = {
        'form': form
    }
    return render(request, 'Post/newpost.html', context)

@login_required
def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, 'Post/postdetail.html', context)
@login_required

def companyPostDetail(request, id):
    post = get_object_or_404(Post, id=id)
    posts=Post.objects.filter(category=post.category)

    context = {
        'post': post,
                'posts': posts

        }
    return render(request, 'company/postdetail.html', context)


from django.db.models import Q
def search_view(request):
    query = request.GET.get("q")

    # Filter products by title, category, or description containing the query
    menu = Post.objects.filter(
        Q(caption__icontains=query) | 
        Q(description__icontains=query)
    )
    context = {
        "menu": menu,
        "query": query,
    }
    return render(request, "company/search-result.html", context)


@login_required
def category_list(rq):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(rq,'category/category.html',context)

@login_required
def category_Post_list(rq,cid):
    category=Category.objects.get(cid=cid)
    posts = Post.objects.filter(status=True, category=category)

    context={
        'category':category,
        'posts':posts
    }
    return render(rq,'category/category-post-list.html',context)

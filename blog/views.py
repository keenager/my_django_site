from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import BlogPost
from .forms import BlogPostForm
# Create your views here.


def index(request):
    posts = BlogPost.objects.all()
    for post in posts:
        print(post.pub_date.date())
        post.pub_date = post.pub_date.date()
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='common:login')
def post_create(request: HttpRequest):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post: BlogPost = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required(login_url='common:login')
def post_modify(request: HttpRequest, post_id):
    post: BlogPost = get_object_or_404(BlogPost, pk=post_id)

    if request.user != post.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('blog:post_detail', post_id)

    if request.method == 'POST':
        # instance 기준으로 form 생성하되 data 값으로 덮어쓰기
        form = BlogPostForm(data=request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.mod_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', post_id)
    else:
        form = BlogPostForm(instance=post)

    context = {
        'form': form
    }
    return render(request, 'blog/post_form.html', context)


@login_required(login_url='common:login')
def post_delete(request: HttpRequest, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.user != post.author:
        messages.error(request, '권한이 없습니다.')
        return redirect('blog:post_detail', post_id)

    post.delete()
    return redirect('blog:index')

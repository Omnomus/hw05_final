from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import CommentForm, PostForm
from posts.models import Follow, Group, Post, User


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGINATION_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, settings.PAGINATION_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'posts/group.html',
                  {'group': group, 'page': page})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('index')
    return render(request, 'posts/new.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, settings.PAGINATION_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user,
            author=author).exists()
    return render(
        request,
        'posts/profile.html',
        {'author': author, 'page': page, 'following': following})


@login_required
def add_comment(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=author)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.post = post
        instance.save()
    return redirect('post', username=username, post_id=post_id)


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=author)
    form = CommentForm()
    return render(
        request,
        'posts/post.html',
        {'post': post,
         'form': form})


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post_requested = get_object_or_404(Post, pk=post_id, author=author)
    if request.user != author:
        return redirect('post', username=username, post_id=post_requested.id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post_requested)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post', username=username, post_id=post_id)
    return render(
        request, 'posts/new.html',
        {'form': form,
         'post': post_requested})


@login_required
def follow_index(request):
    follows = Follow.objects.filter(user=request.user)
    followings = User.objects.filter(following__in=follows)
    post_list = Post.objects.filter(author__in=followings)
    paginator = Paginator(
        post_list, settings.PAGINATION_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page})


@login_required
def profile_follow(request, username):
    user = request.user
    author = User.objects.get(username=username)
    if user != author:
        Follow.objects.get_or_create(user=user, author=author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = User.objects.get(username=username)
    Follow.objects.get(user=user, author=author).delete()
    return redirect('profile', username=username)

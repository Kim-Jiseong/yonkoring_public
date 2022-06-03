from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from yk.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, response
import json

# Create your views here.
@login_required
def home(request):
    posts = Post.objects.all()

    ctx = {
        'posts':posts
    }

    return render(request, 'home.html', ctx)

def new(request):
    if request.method == "POST":
        new_post = Post.objects.create(
            content = request.POST['content'],
            author = request.user
        )
        return redirect('ykboard:detail', new_post.pk)
    return render(request, 'new.html')

def detail(request, post_pk):
    post = Post.objects.filter(pk=post_pk)[0]

    existing_like = Like.objects.filter(
            post = Post.objects.get(pk=post_pk),
            user = request.user
        )

    if request.method == "POST":
        existing_comment = Comment.objects.filter(
            post = Post.objects.filter(pk=post_pk)[0],
            author = request.user
        )

        # 댓글 유저 오더 만들기
        order_list = [0]
        order = 0
        for comment in Comment.objects.filter(post = Post.objects.filter(pk=post_pk)[0]):
            order_list.append(int(comment.order))
        if len(order_list):
            order = max(order_list)            

        # 글쓴이가 댓글 달았을 경우 
        if post.author == request.user:
            new_comment = Comment.objects.create(
                post = Post.objects.filter(pk=post_pk)[0],
                content = request.POST['comment'],
                author = request.user,
                order = -1
            )
        else:
            # 이미 이 게시물에 댓글을 달았으면
            if existing_comment.count():
                new_comment = Comment.objects.create(
                    post = Post.objects.filter(pk=post_pk)[0],
                    content = request.POST['comment'],
                    author = request.user,
                    order = existing_comment[0].order
                )
            else:
                new_comment = Comment.objects.create(
                    post = Post.objects.filter(pk=post_pk)[0],
                    content = request.POST['comment'],
                    author = request.user,
                    order = order + 1
                )
        # 대댓글일 경우
        if request.POST['reply_pk'] and request.POST['comment'][0] == '@':
            new_comment.reply = Comment.objects.filter(pk=request.POST['reply_pk'])[0]
            new_comment.save()

        return redirect('ykboard:detail', post_pk)
        

    ctx = {
        'post': post,
        'user': request.user,
        'existing_like': existing_like.count()
    }

    return render(request, 'detail.html', ctx)

@csrf_exempt
def like(request):
    if request.method == "POST":
        request_body = json.loads(request.body)
        post_pk = request_body['post_pk']

        existing_like = Like.objects.filter(
            post = Post.objects.get(pk=post_pk),
            user = request.user
        )

        # 좋아요 취소
        if existing_like.count() > 0:
            existing_like.delete()
            already_like = True
    
        # 좋아요 생성
        else:
            Like.objects.create(
                post = Post.objects.get(pk=post_pk),
            user = request.user
            )
            already_like = False
        
        post_likes = Like.objects.filter(post = Post.objects.get(pk=post_pk))

        response = {
            'like_count' : post_likes.count(),
            'already_like' : already_like
            
        }

        return HttpResponse(json.dumps(response))

def edit(request, post_pk):
    post = Post.objects.filter(pk=post_pk)[0]
    if request.method == "POST":
        Post.objects.filter(pk=post_pk).update(
            content = request.POST['content']
        )
        return redirect('ykboard:detail', post_pk)
    ctx = {
        'post':post
    }

    return render(request, 'edit.html', ctx)

def delete(request, post_pk):
    post = Post.objects.filter(pk=post_pk)[0]
    post.delete()

    ctx = {
        'post':post
    }

    return redirect('ykboard:home')

def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.filter(
        pk=comment_pk, 
        post=Post.objects.filter(pk=post_pk)[0]
        )
    
    comment_reply = comment[0].comments.filter()

    # 대댓글이 있을 때
    if comment_reply:
        comment.update(
            author = None,
            content = '삭제되었습니다.',
            order = -2
        )
    else:
        comment[0].delete()

    return redirect('ykboard:detail', post_pk)

def my_post(request):
    posts = Post.objects.filter(author=request.user)
    ctx = {
        'posts': posts
    }
    return render(request, 'my_post.html', ctx)

def my_comment(request):
    all_posts = Post.objects.filter()
    posts = []

    for post in all_posts:
        if len(post.comments.filter(author=request.user)) > 0:
            posts.append(post)

    ctx = {
        'posts': posts
    }
    return render(request, 'my_comment.html', ctx)

def yk_update(request):
    return render(request, 'yk_update.html')
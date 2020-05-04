from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from blogs.models import Post, Comment
import json


# 글 목록
def posts_list(request):
    posts = Post.objects.order_by('-created_at')

    return render(request, 'blogs/posts_list.html',  context={'posts': posts})


# 글 상세
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post.id)     # 댓글 가져오기
    is_liked = False                                    # 좋아요를 안누른 상태

    if post.likes.filter(id=request.user.id).exists():  # 좋아요를 누른 상태
        is_liked = True

    return render(request, 'blogs/post_detail.html', context={'post': post, 'comments': comments, 'is_liked': is_liked, 'total_likes': post.total_likes()})


@login_required
@require_POST
def post_like(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = post.likes.filter(id=request.user.id).exists()

    if is_liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', kwargs={'post_id': post.id}))

# 사용자 인증 여부 체크하기(Decorator)
@login_required
def post_write(request):
    errors = []
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title:
            errors.append('제목을 입력해주세요.')

        if not content:
            errors.append('내용을 입력해주세요.')

        if not errors:
            post = Post.objects.create(
                user=request.user, title=title, content=content, image=image)

            return redirect(reverse('post_detail', kwargs={'post_id': post.id}))

    return render(request, 'blogs/post_write.html', {'user': request.user, 'errors': errors})


@login_required
def comment_write(request):
    errors = []
    if request.method == 'POST':
        post_id = request.POST.get('post_id', '').strip()
        content = request.POST.get('content', '').strip()

        if not content:
            errors.append('댓글을 입력해주세요.')

        if not errors:
            comment = Comment.objects.create(
                user=request.user, post_id=post_id, content=content)

            return redirect(reverse('post_detail', kwargs={'post_id': comment.post_id}))

    return render(request, 'blogs/post_detail.html', {'user': request.user, 'errors': errors})

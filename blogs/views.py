from django.shortcuts import get_object_or_404, render, redirect

from blogs.models import Post


# 글 목록
def posts_list(request):
    posts = Post.objects.order_by('-created_at')

    return render(request, 'blogs/posts_list.html',  context={'posts': posts})


# 글 상세
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    return render(request, 'blogs/post_detail.html', context={'post': post})

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

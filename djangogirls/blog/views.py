from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts}) # 'posts'라는 걸 html에서 쓸 건데 이건 posts라는 변수로 할당


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    # 만약 폼에 입력된 데이터가 있으면(=method가 POST라면)
    if request.method == "POST":

        # 입력된 데이터를 가져옴ㅁ와서 PostForm으로 넘겨줌
        form = PostForm(request.POST)

        # 폼에 들어온 값들이 올바른지 확인
        if form.is_valid():

            # commit=False는 넘겨진 데이터를 바로 Post 모델에 저장하지 말라는 뜻 -> 작성자를 추가한 다음 저장하기 위해서
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # 새 블로그 글을 작성한 다음 post_detail 페이지로 이동
            return redirect('post_detail', pk=post.pk)

    # 없으면
    else:
        # 폼을 비운다
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
# url로부터 추가로 pk 변수를 받아서 처리
def post_edit(request, pk):
    # get_object_or_404(Post, pk=pk)를 호출하여 수정하고자 하는 글의 Post 모델 인스턴스로 가져옴(pk로 원하는 글을 찾음)
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
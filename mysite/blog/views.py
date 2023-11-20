from .models import Post
from .forms import EmailPostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.views.generic import ListView

# Create your views here.


# Представления списка
def post_list(request):
    posts_all = Post.published.all()
    # Разбиваем на 3 страницы
    paginator = Paginator(posts_all, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} рекомендую тебе почитать {post.title}"
            message = f"Читать {post.title} at {post_url}\n\n{cd['name']} комментария: {cd['comments']}"
            send_mail(subject, message, 'djangofortest777@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,
                  "blog/post/share.html",
                  {
                      'post': post,
                      'form': form,
                      'sent': sent,
                  })


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


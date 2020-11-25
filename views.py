from django.shortcuts import render, get_object_or_404

from .models import Post
# Create your views here.

def index(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    context = {
        'latest_post_list': latest_post_list,
    }

    return render(request, 'blog/index.html', context)

def detail(request, post_title_url):
    post = get_object_or_404(Post, post_title=post_title_url)
    
    context = {
        'post': post,
    }
    
    return render(request, 'blog/detail.html', context)

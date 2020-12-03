from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Post
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last five published BLOGS (not including blogs set to be published in the future"""
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    #Assigns the blog.post_url field to match agaist slug passed in url
    slug_field = 'post_url'

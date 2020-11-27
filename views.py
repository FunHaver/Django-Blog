from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Post
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last five published BLOGS"""
        return Post.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    #Assigns the blog.post_url field to match agaist slug passed in url
    slug_field = 'post_url'

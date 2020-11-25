from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    # ex: /blog/
    path('', views.index, name='index'),
    # ex: /blog/title
    path('<post_title_url>', views.detail, name='detail'),
]

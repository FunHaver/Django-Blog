from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    # ex: /blog/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /blog/title Lets django know that a slug (string) will be passed in the url to the view
    path('<slug:slug>', views.DetailView.as_view(), name='detail'),
]

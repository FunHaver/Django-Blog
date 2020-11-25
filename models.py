import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Post(models.Model):
    post_title = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    post_body = models.TextField()

    def __str__(self):
        return self.post_title
    
    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

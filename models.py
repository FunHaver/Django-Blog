import datetime

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Post(models.Model):
    post_title = models.CharField(max_length=200)
    #this slug field will be used as the url endpoint for the post
    post_url = models.SlugField(max_length=200, unique=True)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    post_body = models.TextField()

    def __str__(self):
        return self.post_title
    
    #save model method override. "Slugifies" the title row and inserts it into slug row
    def save(self, *args, **kwargs):
        self.post_url = self.post_url or slugify(self.post_title)
        super().save(*args, **kwargs)

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

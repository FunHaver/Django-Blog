from django.test import TestCase

# Create your tests here.

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Post, Author

def create_author(first, last):
    """Create a test author"""
    return Author.objects.create(first_name=first, last_name=last)

def create_post(post_author,post_title, post_body, days, url):
    """Create a post with the given post_author, post_body, and published the given number of days offset to now (negative for posts published in the past, positive for those published in the future).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(author=post_author, post_title=post_title, post_body=post_body, pub_date=time, post_url=url)

class PostModelTests(TestCase):
    
    def test_was_published_recently_with_future_post(self):
        """was_published_recently() returns False for posts whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(pub_date=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_was_published_recently_with_recent_post(self):
        """was_published_recently() returns True for posts whose pub_date is between now and 23 hours 59 min 59 secs ago """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_post = Post(pub_date=time)
        self.assertIs(recent_post.was_published_recently(), True)

    def test_was_published_recently_with_old_post(self):
        """was_published_recently returns False for posts whose pub_date is 24 hours or older """
        time = timezone.now() - datetime.timedelta(hours=24)
        old_post = Post(pub_date=time)
        self.assertIs(old_post.was_published_recently(), False)

class PostIndexViewTests(TestCase):
    def test_no_posts(self):
        """ if no posts exist, an appropriate message is displayed."""
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        
        self.assertQuerysetEqual(response.context['latest_post_list'],[])

    def test_past_post(self):
        create_post(post_author=create_author(first="test", last="author"), post_title="Past Post", post_body="Hello past post", days=-30, url="past-post")
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
                response.context['latest_post_list'],
                ['<Post: Past Post>']
        )
        

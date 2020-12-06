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

def create_post(post_title, post_body, days, url, default_author=True, **kwargs):
    """Create a post with the given post_author, post_body, and published the given number of days offset to now (negative for posts published in the past, positive for those published in the future).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    
    if default_author == True:
        author = create_author(first="Test", last="Author")
    else:
        author = create_author(first=kwargs.get('first', None), last=kwargs.get('last', None))

    return Post.objects.create(post_title=post_title, author=author, post_body=post_body, pub_date=time, post_url=url)

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
        """If there is a post in the past, it will display"""
        create_post(post_title="Past Post", post_body="Hello past post", days=-30, url="past-post")
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
                response.context['latest_post_list'],
                ['<Post: Past Post>']
        )
    def test_future_post(self):
        """If there is a post with a future pub date, it will not be displayed"""
        create_post(post_title="Future Post", post_body="Hello future post", days=+1, url="future-post")
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['latest_post_list'],[])

    def test_multiple_past_posts(self):
        """The blog index page may have multiple posts, set to test 5"""
        post_amount=5
        object_string_array = []
        
        for x in range(post_amount):
            x_str = str(x)
            create_post(post_title="Past post " + x_str, post_body="Hello past post " + x_str, days=-30+x, url="past-post-" + x_str)
            object_string_array.insert(0, "<Post: Past post " + x_str + ">")
        
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_post_list"], object_string_array)

class PostDetailViewTests(TestCase):
    def test_post_title(self):
        """The post detail page has a title displayed"""
        create_post(post_title="Testing Title", post_body="Testing title.", days=-2, url="testing-title")
        response = self.client.get(reverse("blog:detail",args=["testing-title"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testing Title")

    def test_post_author(self):
        """The post detail page has an author displayed"""
        create_post(post_title="Testing Author", post_body="Testing author", days=-2, default_author=False, first="Conor", last="Sullivan", url="testing-author")
        response = self.client.get(reverse("blog:detail", args=["testing-author"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Conor Sullivan")

    def test_post_body(self):
        """The post detail page contains a body"""
        create_post(post_title="Testing Body", post_body="Testing body", days=-2, url="testing-body")
        response = self.client.get(reverse("blog:detail", args=["testing-body"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testing body")

    def test_published_date(self):
        """The post detail page contains a published date"""
        create_post(post_title="Testing Published Date", post_body="Testing published date", days=-1, url="testing-published-date")
        response = self.client.get(reverse("blog:detail", args=["testing-published-date"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(timezone.now() + datetime.timedelta(days=-1)))

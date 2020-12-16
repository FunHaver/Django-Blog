from django.test import TestCase

from django.utils import timezone
from django.urls import reverse

from .models import Post, Author


def post_factory(opening_tag, closing_tag, tag_name):
    """Creates post with tags passed into post_body"""
    test_author = Author.objects.create(first_name="Test", last_name="Author")
    tagged_post_body = opening_tag + "Testing testing... > < < " + closing_tag
    tagged_post_url = "testing-tag-" + tag_name
    tagged_post_title = "Testing Tags" + tag_name
    
    return Post.objects.create(post_title=tagged_post_title, author=test_author, post_body=tagged_post_body, pub_date=timezone.now(), post_url=tagged_post_url)

class SiftHTMLTestCase(TestCase):
    def test_bold_tag_unescaped(self):
        """Bold tag uses non-escaped representation"""
        bold_post = post_factory("<b>", "</b>", "bold")
        response = self.client.get(reverse("blog:detail", args=[bold_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<b>")
        self.assertContains(response, "</b>")

    def test_italics_tag_unescaped(self):
        """Italics tag uses non-escaped representation"""
        italics_post = post_factory("<i>", "</i>", "italics")
        response = self.client.get(reverse("blog:detail", args=[italics_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<i>")
        self.assertContains(response, "</i>")

    def test_a_tag_unescaped(self):
        """A tag uses non-escaped representation"""
        
        a_post = post_factory('<a href="https://example.com">', "</a>", "a")
        response = self.client.get(reverse("blog:detail", args=[a_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<a href="https://example.com">')
        self.assertContains(response, "</a>")

    def test_script_tag_remains_escaped(self):
        """Script tag remains in escaped representation"""
        script_post = post_factory("<script>", "</script>", "script")
         
        response = self.client.get(reverse("blog:detail", args=[script_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "&lt;script&gt;")
        self.assertContains(response, "&lt;/script&gt;")

    def test_script_tag_remains_escaped_in_a_tag(self):
        """Script tag remains escaped if within an a tag"""
        script_post = post_factory("<a href=<script>alert('XSS')</script>\"google.com\">","</a>", "injected-script-tag")

        response = self.client.get(reverse("blog:detail", args=[script_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "&lt;script&gt;")
        self.assertContains(response, "&lt;/script&gt;")

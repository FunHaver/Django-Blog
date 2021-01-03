from django.test import TestCase

from django.utils import timezone
from django.urls import reverse

from .models import Post, Author


def post_factory(opening_tag, closing_tag, tag_name):
    """Creates post with tags passed into post_body"""
    test_author = Author.objects.create(first_name="Test", last_name="Author")
    tagged_post_body = opening_tag + "Testing testing..." + closing_tag
    tagged_post_url = "testing-tag-" + tag_name
    tagged_post_title = "Testing Tag " + tag_name
    
    post_object = Post.objects.create(post_title=tagged_post_title, author=test_author, post_body=tagged_post_body, pub_date=timezone.now(), post_url=tagged_post_url)
    return post_object

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

    def test_br_tag_unescaped(self):
        """br tag uses non-escaped representation"""
        br_post = post_factory("Paragraph<br>Paragraph Two", "", "br")
        response = self.client.get(reverse("blog:detail", args=[br_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<br>")

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

    def test_h1_tag(self):
        """Tests h1 tag"""

        header_post = post_factory("<h1>", "</h1>", "h1")
        response = self.client.get(reverse("blog:detail", args=[header_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\t<h1>")
        self.assertContains(response, ".</h1>")
    
    def test_h2_tag(self):
        """Tests h2 tag"""

        header_post = post_factory("<h2>", "</h2>", "h2")
        response = self.client.get(reverse("blog:detail", args=[header_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\t<h2>")
        self.assertContains(response, ".</h2>")

    def test_h3_tag(self):
        """Tests h3 tag"""

        header_post = post_factory("<h3>", "</h3>", "h3")
        response = self.client.get(reverse("blog:detail", args=[header_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\t<h3>")
        self.assertContains(response, ".</h3>")
    
    def test_h4_tag(self):
        """Tests h4 tag"""

        header_post = post_factory("<h4>", "</h4>", "h4")
        response = self.client.get(reverse("blog:detail", args=[header_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\t<h4>")
        self.assertContains(response, ".</h4>")

    def test_h5_tag(self):
        """Tests h5 tag"""

        header_post = post_factory("<h5>", "</h5>", "h5")
        response = self.client.get(reverse("blog:detail", args=[header_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\t<h5>")
        self.assertContains(response, ".</h5>")

    def test_h6_tag(self):
        """Tests h6 tag"""

        header_post = post_factory("<h6>", "</h6>", "h6")
        response = self.client.get(reverse("blog:detail", args=[header_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\t<h6>")
        self.assertContains(response, ".</h6>")

    def test_code_tag(self):
        """Tests code tag is unescaped"""
        code_post = post_factory("<code>", "</code>", "code")
        response = self.client.get(reverse("blog:detail", args=[code_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\t<code>")
        self.assertContains(response, ".</code>")

    def test_img_tag(self):
        """Tests img tag is unescaped"""
        image_post = post_factory('<img src="https://example.com/example.jpg">', "</img>", "image")
        response = self.client.get(reverse("blog:detail", args=[image_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '\t<img src="https://example.com/example.jpg">')
        self.assertContains(response, ".</img>")

class CarriageReturnToBreakTestCase(TestCase):
    def test_backslash_n_creates_br(self):
        """1 Newline character is replaced with 1 break tag"""
        newline_post = post_factory(chr(10), "", "newline")

        response = self.client.get(reverse("blog:detail", args=[newline_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<br>")
        self.assertEqual(str(response.content).count("<br>"), 1)

    def test_backslash_r_creates_br(self):
        """1 Newline character is replaced with 1 break tag"""
        newline_post = post_factory(chr(13), "", "register")

        response = self.client.get(reverse("blog:detail", args=[newline_post.post_url]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<br>")
        self.assertEqual(str(response.content).count("<br>"), 1)
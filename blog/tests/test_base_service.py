from django.test import TestCase
from blog.services.blog_service import BlogService

class BlogServiceTestCases(TestCase):
    def setUp(self):
        BlogService.__abstractmethods__=set()
        self.blog_service = BlogService()

    def test_abstract_blog_service_get_posts_raise_error(self):
        with self.assertRaises(NotImplementedError):
            self.blog_service.get_blog_posts()


    def test_abstract_blog_service_get_post_raise_error(self):
        with self.assertRaises(NotImplementedError):
            self.blog_service.get_blog_post(post_id=2)

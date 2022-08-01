import copy

from django.test import TestCase
from django.utils import dateparse
from unittest.mock import patch

from blog.services.buttercms import ButterCMSBlogService

class BlogServiceTestCases(TestCase):
    def setUp(self):
        self.blog_service_mock = patch('blog.services.buttercms.ButterCMS')
        self.blog_service_patch = self.blog_service_mock.start()
        self.blog_service = ButterCMSBlogService()

    def test_get_blog_posts_with_no_data(self):
        expected = {
            "error": "Could not fetch blog posts from ButterCMS",
            "code": 404,
        }
        self.blog_service_patch.return_value.posts.all.return_value = {}
        blog_posts = self.blog_service.get_blog_posts()

        self.assertEqual(blog_posts, expected)

    @patch('blog.services.buttercms.settings')
    def test_get_blog_posts_with_invalid_token(self, setting_patch):
        setting_patch.BUTTERCMS_API_TOKEN = None
        self.blog_service = ButterCMSBlogService()

        expected = {
            "no_token": True,
        }
        blog_posts = self.blog_service.get_blog_posts()

        self.assertEqual(blog_posts, expected)

    def test_get_blog_posts_successfully(self):
        mock_data = {
            'meta': {
                'next_page': None,
                'previous_page': None,
                'count': 1
            },
            'data': [{
                'status': 'published',
                'created': '2022-07-31T01:07:35.451431Z',
                'updated': '2022-07-31T01:07:35.463203Z',
                'published': '2022-07-31T01:07:00Z',
                'title': 'title',
                'slug': 'slug',
                'body': 'body',
                'summary': "summary",
                'seo_title': 'seo-title',
                'meta_description': "meta-description",
                'featured_image_alt': '',
                'url': 'post-13',
                'featured_image': 'https://cdn.buttercms.com/xiRbhKVHQPWutnz8vz7g',
                'author': {
                    'bio': '',
                    'slug': 'peter-olayinka',
                    'email': 'peterolayinka97@gmail.com',
                    'title': '',
                    'last_name': 'Olayinka',
                    'first_name': 'Peter',
                    'facebook_url': '',
                    'linkedin_url': '',
                    'instagram_url': '',
                    'pinterest_url': '',
                    'profile_image': 'https://d1ts43dypk8bqh.cloudfront.net/v1/avatars/8146c20d-3e36-4e56-8549-9635e9a59ece',
                    'twitter_handle': ''
                },
                'tags': [],
                'categories': []
            }, ]
        }
        self.blog_service_patch.return_value.posts.all.return_value = mock_data
        expected = copy.deepcopy(mock_data)
        iso_date = dateparse.parse_datetime(expected["data"][0]["published"])
        expected['data'][0].update({'published':  iso_date})
        blog_posts = self.blog_service.get_blog_posts()

        self.assertEqual(blog_posts, expected)

    def test_get_blog_post_with_no_slug(self):
        expected = {
            "error": "Could not fetch blog posts from ButterCMS",
            "code": 404,
        }
        blog_post = self.blog_service.get_blog_post(slug=None)

        self.assertEqual(blog_post, expected)

    def test_get_blog_post_with_no_data(self):
        expected = {
            "error": "Could not fetch blog posts from ButterCMS",
            "code": 404,
        }
        self.blog_service_patch.return_value.posts.get.return_value = {}
        blog_post = self.blog_service.get_blog_post(slug="test")

        self.assertEqual(blog_post, expected)

    def test_get_single_blog_post_successfully(self):
        mock_data = {'meta': {'next_post': {'slug': 'post-12', 'title': 'Post 12', 'featured_image': 'https://d2wzhk7xhrnk1x.cloudfront.net/f9Sen4QQcyVHSDZzI75w_butter-blog-post.jpg'}, 'previous_post': {'slug': 'post-10', 'title': 'Post 10', 'featured_image': None}}, 'data': {'created': '2022-07-31T01:06:37.611498Z', 'published': '2022-07-31T01:06:00Z', 'url': 'post-11', 'slug': 'post-11', 'featured_image': None, 'featured_image_alt': '', 'author': {'first_name': 'Peter', 'last_name': 'Olayinka', 'email': 'peterolayinka97@gmail.com', 'slug': 'peter-olayinka', 'bio': '', 'title': '', 'linkedin_url': '', 'facebook_url': '', 'instagram_url': '', 'pinterest_url': '', 'twitter_handle': '', 'profile_image': 'https://d1ts43dypk8bqh.cloudfront.net/v1/avatars/8146c20d-3e36-4e56-8549-9635e9a59ece'}, 'tags': [], 'categories': [], 'title': 'Post 11', 'body': '<p><span aria-label="CSS property name: flex" class="webkit-css-property">flex</span><span class="styles-name-value-separator">: </span><span is="ui-icon" class="expand-icon spritesheet-smallicons smallicon-triangle-right icon-mask"></span><span aria-label="CSS property value: 1" class="value">1</span><span>;</span></p>', 'summary': 'flex : 1 ;', 'updated': '2022-07-31T01:06:37.621916Z', 'seo_title': 'Post 11', 'meta_description': 'flex : 1 ;', 'status': 'published'}}
        expected = copy.deepcopy(mock_data)
        iso_date = dateparse.parse_datetime(expected["data"]["published"])
        expected['data'].update({'published':  iso_date})
        self.blog_service_patch.return_value.posts.get.return_value = mock_data
        blog_post = self.blog_service.get_blog_post(slug="test")

        self.assertEqual(blog_post, expected)

import copy

from django.urls import reverse
from django.test import TestCase
from django.utils import dateparse
from blog.services.buttercms import ButterCMSBlogService
from unittest.mock import patch

class BlogViewTestCases(TestCase):
    def setUp(self):
        self.blog_service_mock = patch('blog.services.buttercms.ButterCMS')
        self.blog_service_patch = self.blog_service_mock.start()
        self.blog_service = ButterCMSBlogService()

    @patch('blog.views.settings')
    def test_home_page_view(self, setting_patch):
        expected_template = ['blog/index.html'];
        expected_token = "fake-token"
        setting_patch.BUTTERCMS_API_TOKEN = expected_token

        url = reverse("home")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.template_name, expected_template)
        self.assertEqual(resp.context['butter_token'], expected_token)

    def test_blog_page_view_loads_successfully(self):
        mock_data = {
            'meta': {
                'next_page': None,
                'previous_page': None,
                'count': 1
            },
            'data': [{
                'published': '2022-07-31T01:07:00Z',
                'slug': 'slug',
            }, ]
        }
        self.blog_service_patch.return_value.posts.all.return_value = mock_data
        expected_template = ["blog/post_list.html"];
        expected_context_keys = ['view', 'meta', 'data']
        expected = copy.deepcopy(mock_data)
        iso_date = dateparse.parse_datetime(expected["data"][0]["published"])
        expected['data'][0].update({'published':  iso_date})

        url = reverse("blog")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.template_name, expected_template)
        self.assertEqual(list(resp.context_data.keys()), expected_context_keys)

    def test_get_blog_posts_raises_404_error(self):
        errror_code = {
            "error": "Could not fetch blog posts from ButterCMS",
            "code": 404,
        }
        self.blog_service_patch.return_value.posts.all.return_value = errror_code

        url = reverse("blog")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

    def test_blog_detail_page_view_loads_successfully(self):
        mock_data = {
            'meta': {
                'next_page': None,
                'previous_page': None,
                'count': 1
            },
            'data': {
                'published': '2022-07-31T01:07:00Z',
                'slug': 'slug',
            }
        }
        self.blog_service_patch.return_value.posts.get.return_value = mock_data
        expected_template = ["blog/post_detail.html"];
        expected_context_keys = ['slug', 'view', 'meta', 'data']
        expected = copy.deepcopy(mock_data)
        iso_date = dateparse.parse_datetime(expected["data"]["published"])
        expected['data'].update({'published':  iso_date})

        url = reverse("post_detail", args=["fake-slug"])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.template_name, expected_template)
        self.assertEqual(list(resp.context_data.keys()), expected_context_keys)

    def test_get_detail_blog_posts_raises_404_error(self):
        errror_code = {
            "error": "Could not fetch blog posts from ButterCMS",
            "code": 404,
        }
        self.blog_service_patch.return_value.posts.get.return_value = errror_code

        url = reverse("post_detail", args=["fake-slug"])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)

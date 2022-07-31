# This file/class is meant to house the code logic for the blog
# so that the business logic used to fetch blog post can be reused or easily changed.
# An example is rendering data directly from django, returning data via REST API
# and GraphQL all at the same time which uses the same logic.

from django.conf import settings
from django.utils import dateparse

from butter_cms import ButterCMS
from .blog_service import BlogService


class ButterCMSBlogService(BlogService):
    def __init__(self):
        self.auth_token = settings.BUTTERCMS_API_TOKEN
        self.butter_client = ButterCMS(self.auth_token)
        self.no_token = {
            "no_token": True,
        }
        self.code_404 = {
            "error": "Could not fetch blog posts from ButterCMS",
            "code": 404,
        }

    def get_blog_posts(self, *args, **kwargs):
        """
        Return a list of blog posts from ButterCMS.
        """
        # Check if API Token is set properly
        if not self.auth_token:
            return self.no_token

        blog_posts = self.butter_client.posts.all(params=kwargs)

        # If "data" is not in the payload, the page was not fetched successfully
        if blog_posts.get("data") is None:
            return self.code_404
        else:
            if blog_posts.get("data") is not None:
                for post in blog_posts.get("data", []):
                    post["published"] = dateparse.parse_datetime(post["published"])

        return blog_posts

    def get_blog_post(self, slug):
        """
        Return a blog post from ButterCMS. return 404 if the post is not found
        """
        # return 404 if slug is empty before hittig buttercms
        if not slug:
            return self.code_404

        blog_post = self.butter_client.posts.get(slug)

        # If "data" is not in the payload, the page was not fetched successfully
        if blog_post.get("data") is None:
            return self.code_404

        post_data = blog_post.get("data")
        post_data["published"] = dateparse.parse_datetime(post_data["published"])
        blog_post["data"] = post_data
        return blog_post

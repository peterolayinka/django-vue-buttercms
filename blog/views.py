from django.conf import settings
from django.shortcuts import render
from django.http import Http404
from django.utils import dateparse
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import TemplateView
from django.views.decorators.clickjacking import xframe_options_exempt
from .services.buttercms import ButterCMSBlogService

import logging

logger = logging.getLogger(__name__)


class HomePageview(ButterCMSBlogService, TemplateView):
    template_name = "blog/index.html"

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # passing down the ButterCMS token to the template
        # to prevent commiting it to the repo
        context["butter_token"] = settings.BUTTERCMS_API_TOKEN
        return self.render_to_response(context)

class BlogPageview(ButterCMSBlogService, TemplateView):
    template_name = "blog/post_list.html"

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        query = {
            "page_size": request.GET.get("page_size", 10),
            "page": request.GET.get("page", 1),
            "exclude_body": request.GET.get("exclude_body", True),
        }

        blog_posts = self.get_blog_posts(**query)
        # import pdb; pdb.set_trace()

        if "code" in blog_posts and blog_posts["code"] == 404:
            raise Http404

        context = {**context, **blog_posts}

        return self.render_to_response(context)


class BlogDetailview(ButterCMSBlogService, TemplateView):
    template_name = "blog/post_detail.html"

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        blog_post = self.get_blog_post(kwargs.get("slug"))

        if "code" in blog_post and blog_post["code"] == 404:
            raise Http404

        context = {**context, **blog_post}
        return self.render_to_response(context)

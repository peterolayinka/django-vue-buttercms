from abc import ABC, abstractmethod

class BlogService(ABC):
    @abstractmethod
    def get_blog_posts(self):
        raise NotImplementedError

    @abstractmethod
    def get_blog_post(self, post_id):
        raise NotImplementedError

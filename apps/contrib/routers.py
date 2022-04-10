from rest_framework import routers

from adhocracy4.api.routers import CustomRouterMixin


class CommentRouterMixin(CustomRouterMixin):

    prefix_regex = (
        r'comments/(?P<comment_pk>[\d]+)/{prefix}'
    )


class CommentDefaultRouter(CommentRouterMixin, routers.DefaultRouter):
    pass

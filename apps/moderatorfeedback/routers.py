from rest_framework import routers

from adhocracy4.api.routers import CustomRouterMixin


class FeedbackDetailRouterMixin(CustomRouterMixin):

    prefix_regex = (
        r'feedback/(?P<comment_pk>[\d]+)/{prefix}'
    )


class FeedbackDetailDefaultRouter(FeedbackDetailRouterMixin,
                                  routers.DefaultRouter):
    pass

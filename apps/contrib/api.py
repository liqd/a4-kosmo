from django.shortcuts import get_object_or_404

from adhocracy4.comments.models import Comment


class CommentMixin:
    """Use in combination with CommentRouter to fetch the comment."""

    def dispatch(self, request, *args, **kwargs):
        self.comment_pk = kwargs.get('comment_pk', '')
        return super().dispatch(request, *args, **kwargs)

    @property
    def comment(self):
        return get_object_or_404(
            Comment,
            pk=self.comment_pk
        )

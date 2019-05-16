from django.apps import AppConfig


class Config(AppConfig):
    name = 'apps.actions'
    label = 'liqd_product_actions'

    def ready(self):
        from adhocracy4.actions.models import configure_icon
        from adhocracy4.actions.models import configure_type
        from adhocracy4.actions.verbs import Verbs
        configure_type(
            'project',
            ('a4projects', 'project')
        )
        configure_type(
            'phase',
            ('a4phases', 'phase')
        )
        configure_type(
            'comment',
            ('a4comments', 'comment')
        )
        configure_type(
            'rating',
            ('a4ratings', 'rating')
        )
        configure_type(
            'item',
            ('liqd_product_budgeting', 'proposal'),
            ('liqd_product_ideas', 'idea'),
            ('liqd_product_mapideas', 'mapidea')
        )

        configure_icon('far fa-comment', type='comment')
        configure_icon('far fa-lightbulb', type='item')
        configure_icon('fas fa-plus', verb=Verbs.ADD)
        configure_icon('fas fa-pencil', verb=Verbs.UPDATE)
        configure_icon('fas fa-flag', verb=Verbs.START)
        configure_icon('fas fa-clock', verb=Verbs.SCHEDULE)

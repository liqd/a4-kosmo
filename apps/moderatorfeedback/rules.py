import rules

from adhocracy4.modules import predicates as module_predicates

rules.add_perm(
    'a4_candy_moderatorfeedback.add_moderatorcommentstatement',
    module_predicates.is_allowed_moderate_project
)

rules.add_perm(
    'a4_candy_moderatorfeedback.change_moderatorcommentstatement',
    module_predicates.is_allowed_moderate_project
)

rules.add_perm(
    'a4_candy_moderatorfeedback.delete_moderatorcommentstatement',
    module_predicates.is_allowed_moderate_project
)

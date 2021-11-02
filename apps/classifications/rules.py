import rules

from adhocracy4.modules import predicates as module_predicates
from adhocracy4.projects.predicates import is_moderator as is_project_moderator

rules.add_perm('a4_candy_classifications.view_userclassification',
               is_project_moderator)

rules.add_perm('a4_candy_classifications.view_aiclassification',
               is_project_moderator)

rules.add_perm('a4_candy_classifications.change_userclassification',
               module_predicates.is_context_moderator)

rules.add_perm('a4_candy_classifications.change_aiclassification',
               module_predicates.is_context_moderator)

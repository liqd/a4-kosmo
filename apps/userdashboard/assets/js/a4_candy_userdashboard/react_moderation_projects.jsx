var React = require('react')
var ReactDOM = require('react-dom')

import ModerationProjects from './ModerationProjects'

function init () {
  $('[data-aplus-widget="moderation_projects"').each(function(i, element) {
    const moderationProjects = element.getAttribute('data-moderation-projects')
    const projectApiUrl = element.getAttribute('data-project-api-url')
    ReactDom.render(
      <ModerationProjects
        moderationProjects={moderationProjects}
        projectApiUrl={projectApiUrl}
      />,
      element)
  })
}

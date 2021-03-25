import ModerationProjects from './ModerationProjects'
import React from 'react'
import ReactDOM from 'react-dom'

function init () {
  $('[data-aplus-widget="moderation_projects"').each(function (i, element) {
    const moderationProjects = element.getAttribute('data-moderation-projects')
    const projectApiUrl = element.getAttribute('data-project-api-url')
    ReactDOM.render(
      <ModerationProjects
        moderationProjects={moderationProjects}
        projectApiUrl={projectApiUrl}
      />,
      element)
  })
}

document.addEventListener('DOMContentLoaded', init, false)

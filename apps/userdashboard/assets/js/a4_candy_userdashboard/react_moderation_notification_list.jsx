import ModerationNotificationList from './ModerationNotificationList'
import React from 'react'
import ReactDOM from 'react-dom'

function init () {
  $('[data-aplus-widget="moderation_notification_list"]').each(function (i, element) {
    const aiclassificationApiUrl = element.getAttribute('data-aiclassification-api-url')
    const userclassificationApiUrl = element.getAttribute('data-userclassification-api-url')
    const projectTitle = element.getAttribute('data-project-title')
    const organisation = element.getAttribute('data-organisation')
    const projectUrl = element.getAttribute('data-project-url')
    ReactDOM.render(
      <ModerationNotificationList
        aiclassificationApiUrl={aiclassificationApiUrl}
        userclassificationApiUrl={userclassificationApiUrl}
        projectTitle={projectTitle}
        organisation={organisation}
        projectUrl={projectUrl}
      />,
      element)
  })
}

document.addEventListener('DOMContentLoaded', init, false)

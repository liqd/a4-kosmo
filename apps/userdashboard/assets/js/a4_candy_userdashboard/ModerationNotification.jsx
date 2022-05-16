import React, { useState } from 'react'
import django from 'django'
import api from './api'
import { ModerationStatementForm } from './ModerationStatementForm'
import { ModerationStatement } from './ModerationStatement'
import { ModerationNotificationActionsBar } from './ModerationNotificationActionsBar'
import { alert as Alert } from 'adhocracy4'

const translated = {
  statementAdded: django.pgettext('kosmo', 'Your statement was successfully delivered.'),
  statementEdited: django.pgettext('kosmo', 'Your statement was successfully updated.'),
  statementDeleted: django.pgettext('kosmo', 'Your statement was successfully deleted.'),
  anotherStatement: django.pgettext('kosmo', 'The comment has already been moderated. Your statement could not be saved.'),
  goToDiscussion: django.pgettext('kosmo', 'Go to discussion'),
  commentBlocked: django.pgettext('kosmo', 'Comment blocked successfully.'),
  commentUnblocked: django.pgettext('kosmo', 'Comment unblocked successfully.'),
  commentHighlighted: django.pgettext('kosmo', 'Comment highlighted successfully.'),
  commentUnhighlighted: django.pgettext('kosmo', 'Comment unhighlighted successfully.'),
  notificationArchived: django.pgettext('kosmo', 'Notification archived successfully.'),
  notificationUnarchived: django.pgettext('kosmo', 'Notification unarchived successfully.')
}

export const ModerationNotification = (props) => {
  const { notification } = props
  const [showStatementForm, setShowStatementForm] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [alert, setAlert] = useState()

  function getLink (string, url) {
    const splitted = string.split('{}')
    return (
      <span>
        {splitted[0]}
        <a target="_blank" rel="noreferrer" href={url}>{splitted[1]}</a>
        {splitted[2]}
      </span>
    )
  }

  // Return a react component to render the anchor, we should probably rather
  // extent the Alert component to handle
  function getStatementAdded (commentUrl) {
    return (
      <>
        {translated.statementAdded} <a href={commentUrl}>{translated.goToDiscussion}</a>
      </>
    )
  }

  // **** Start statement methods ****

  const handleStatementSubmit = async (payload) => {
    const [getResponse] = await api.fetch({
      url: notification.statement_api_url,
      method: 'GET'
    })

    if (getResponse.length > 0) {
      setShowStatementForm(false)
      setAlert({
        type: 'error',
        message: translated.anotherStatement,
        timeInMs: 3000
      })
    } else {
      // eslint-disable-next-line no-unused-vars
      const [response, error] = await api.fetch({
        url: notification.statement_api_url,
        method: 'POST',
        body: { statement: payload }
      })
      if (error) {
        setAlert({
          type: 'error',
          message: error,
          timeInMs: 3000
        })
      } else {
        props.loadData()
        setShowStatementForm(false)
        setAlert({
          type: 'success',
          message: getStatementAdded(),
          timeInMs: 3000
        })
      }
    }
  }

  const handleStatementEdit = async (payload) => {
    // eslint-disable-next-line no-unused-vars
    const [response, error] = await api.fetch({
      url: notification.statement_api_url + notification.moderator_statement.pk + '/',
      method: 'PUT',
      body: { statement: payload }
    })
    if (error) {
      props.onChangeStatus(error)
    } else {
      props.loadData()
      setShowStatementForm(false)
      setIsEditing(false)
      setAlert({
        type: 'success',
        message: translated.statementEdited,
        timeInMs: 3000
      })
    }
  }

  const handleStatementDelete = async () => {
    await api.fetch({
      url: notification.statement_api_url + notification.moderator_statement.pk + '/',
      method: 'DELETE'
    })
    props.loadData()
    setAlert({
      type: 'success',
      message: translated.statementDeleted,
      timeInMs: 3000
    })
  }

  function toggleModerationStatementForm (isEditing) {
    isEditing && setIsEditing(true)
    setShowStatementForm(!showStatementForm)
  }

  // **** End statement methods ****

  // **** Start notification methods ****

  async function toggleIsPending () {
    const url = notification.has_pending_notifications
      ? props.apiUrl + 'archive/'
      : props.apiUrl + 'unarchive/'
    const [response, error] =
      await api.fetch({
        url: url,
        method: 'GET'
      })
    const alertMessage = response && response.has_pending_notifications
      ? translated.notificationUnarchived
      : translated.notificationArchived

    if (error) {
      props.onChangeStatus(error)
    } else {
      props.onChangeStatus(alertMessage)
    }
  }

  async function toggleIsBlocked () {
    const [response, error] =
      await api.fetch({
        url: props.apiUrl,
        method: 'PATCH',
        body: { is_blocked: !notification.is_blocked }
      })
    const alertMessage = response && response.is_blocked
      ? translated.commentBlocked
      : translated.commentUnblocked

    if (error) {
      props.onChangeStatus(error)
    } else {
      props.onChangeStatus(alertMessage)
    }
  }

  async function toggleIsHighlighted () {
    const [response, error] =
      await api.fetch({
        url: props.apiUrl,
        method: 'PATCH',
        body: { is_moderator_marked: !notification.is_moderator_marked }
      })
    const alertMessage = response && response.is_moderator_marked
      ? translated.commentHighlighted
      : translated.commentUnhighlighted

    if (error) {
      props.onChangeStatus(error)
    } else {
      props.onChangeStatus(alertMessage)
    }
  }

  // **** End notification methods ****

  function translatedReportText (reportsFound) {
    const tmp = django.ngettext(
      'kosmo', '\'s {}comment{} has been reported 1 time since it\'s creation',
      'kosmo', '\'s {}comment{} has been reported %s times since it\'s creation',
      reportsFound
    )
    return (
      django.interpolate(tmp, [reportsFound])
    )
  }

  const {
    comment: commentText,
    comment_url: commentUrl,
    last_edit: created,
    is_modified: isModified,
    user_image: userImage,
    user_name: userName,
    user_profile_url: userProfileUrl,
    num_active_notifications: activeNotifications,
    time_of_last_notification: timeOfLastNotification
  } = notification
  const classificationText = django.pgettext('kosmo', 'Classification: ')
  const archiveText = django.pgettext('kosmo', ' Archive')

  let userImageDiv
  if (userImage) {
    const sectionStyle = {
      backgroundImage: 'url(' + userImage + ')'
    }
    userImageDiv = <div className="user-avatar user-avatar--small user-avatar--shadow mb-1 userindicator__btn-img" style={sectionStyle} />
  }

  let commentChangeLog
  if (isModified) {
    commentChangeLog = django.pgettext('kosmo', 'Last edited on ' + created)
  } else {
    commentChangeLog = django.pgettext('kosmo', 'Created on ' + created)
  }

  return (
    <>
      <li className="list-item">
        <div class="d-flex">
          {userImageDiv}
          <div>
            <i className="fas fa-exclamation-circle me-1" aria-hidden="true" />
            <strong>{userProfileUrl ? <a href={userProfileUrl}>{userName}</a> : userName}</strong>
            {getLink(translatedReportText(activeNotifications), commentUrl)}
            <div className="pt-1">{commentChangeLog}</div>
          </div>
          {notification.has_pending_notifications &&
            <div className="ms-auto">
              <button
                type="button"
                className="dropdown-toggle btn btn--none"
                aria-haspopup="true"
                aria-expanded="false"
                data-bs-toggle="dropdown"
              >
                <i className="fas fa-ellipsis-v" aria-hidden="true" />
              </button>
              <ul className="dropdown-menu dropdown-menu-end">
                <li key="1">
                  <button
                    className="dropdown-item"
                    type="button"
                    onClick={() => toggleIsPending()}
                  >
                    {archiveText}
                  </button>
                </li>
              </ul>
            </div>}
        </div>

        <div className="a4-comments__box--comment">
          <span className="sr-only">
            {classificationText}{notification.category_counts[0]}
          </span>
          {Object.entries(notification.category_counts).map((classification, i) => (
            <span
              className="badge a4-comments__badge a4-comments__badge--que"
              data-classification={classification[0]}
              key={i}
            >
              {`${classification[0]}: ${classification[1]}`}
            </span>))}
          <span>
            {timeOfLastNotification}
          </span>
        </div>
        <p>{commentText}</p>
        <ModerationNotificationActionsBar
          isPending={notification.has_pending_notifications}
          isEditing={notification.moderator_statement}
          isBlocked={notification.is_blocked}
          isHighlighted={notification.is_moderator_marked}
          onToggleForm={(isEditing) => toggleModerationStatementForm(isEditing)}
          onToggleBlock={() => toggleIsBlocked()}
          onToggleHighlight={() => toggleIsHighlighted()}
          onTogglePending={() => toggleIsPending()}
        />
        {showStatementForm &&
          <ModerationStatementForm
            onSubmit={(payload) => handleStatementSubmit(payload)}
            onEditSubmit={(payload) => handleStatementEdit(payload)}
            initialStatement={notification.moderator_statement}
            editing={isEditing}
          />}
        {notification.moderator_statement && !showStatementForm &&
          <ModerationStatement
            notificationIsPending={notification.has_pending_notifications}
            statement={notification.moderator_statement}
            onDelete={handleStatementDelete}
            onEdit={() => {
              setShowStatementForm(true)
              setIsEditing(true)
            }}
          />}
      </li>
      <div className="mb-3">
        <Alert {...alert} onClick={() => setAlert(null)} />
      </div>
    </>
  )
}

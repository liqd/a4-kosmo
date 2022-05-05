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
  const [loading, setLoading] = useState(false)

  function getLink (string, url) {
    const splitted = string.split('{}')
    return (
      <span>
        {splitted[0]}
        <a href={url}>{splitted[1]}</a>
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
    setLoading(true)
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
    setLoading(false)
  }

  const handleStatementEdit = async (payload) => {
    setLoading(true)
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
    setLoading(false)
  }

  const handleStatementDelete = async () => {
    setLoading(true)
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
    setLoading(false)
  }

  function toggleModerationStatementForm (e) {
    const newModerationStatementForm = !showStatementForm
    setShowStatementForm(newModerationStatementForm)
  }

  // **** End statement methods ****

  // **** Start notification methods ****

  async function toggleIsPending () {
    setLoading(true)
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
      props.loadData()
    }
    setLoading(false)
  }

  async function toggleIsBlocked () {
    setLoading(true)
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
      props.loadData()
    }
    setLoading(false)
  }

  async function toggleIsHighlighted () {
    setLoading(true)
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
      props.loadData()
    }
    setLoading(false)
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
        <div>
          <div className="row">
            <div className="col-sm-2 col-md-1">
              {userImageDiv}
            </div>
            <div className="col-sm-7 col-md-8">
              <div className="pb-1">
                <i className="fas fa-exclamation-circle me-1" aria-hidden="true" />
                <strong>{userProfileUrl ? <a href={userProfileUrl}>{userName}</a> : userName}</strong>
                {getLink(translatedReportText(activeNotifications), commentUrl)}
              </div>
              <div>{commentChangeLog}</div>
            </div>
            {notification.has_pending_notifications &&
              <div className="col">
                <div className="text-end">
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
                </div>
              </div>}

          </div>
          <div className="row">
            <div className="a4-comments__box--comment">
              <div className="col-12">
                <span className="sr-only">
                  {classificationText}{props.classifications}
                </span>
                {props.classifications.map((classification, i) => (
                  <span
                    className="badge a4-comments__badge a4-comments__badge--que"
                    key={i}
                  >
                    {classification}
                  </span>))}
                <span>
                  {timeOfLastNotification}
                </span>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-12">
              <p>{commentText}</p>
            </div>
          </div>
          {loading
            ? (
              <div className="d-flex justify-content-center my-3">
                <i className="fa fa-spinner fa-pulse" aria-hidden="true" />
              </div>)
            : (
              <ModerationNotificationActionsBar
                isPending={notification.has_pending_notifications}
                isDisabled={notification.moderator_statement}
                isBlocked={notification.is_blocked}
                isHighlighted={notification.is_moderator_marked}
                onToggleForm={() => toggleModerationStatementForm()}
                onToggleBlock={() => toggleIsBlocked()}
                onToggleHighlight={() => toggleIsHighlighted()}
                onTogglePending={() => toggleIsPending()}
              />)}
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
        </div>
      </li>
      <div className="mb-3">
        <Alert {...alert} onClick={() => setAlert(null)} />
      </div>
    </>
  )
}

import React, { Component } from 'react'
import django from 'django'
import api from './api'
import { ModerationStatementForm } from './ModerationStatementForm'
import { ModerationStatement } from './ModerationStatement'
import { alert as Alert } from 'adhocracy4'

const translated = {
  statementAdded: django.pgettext('kosmo', 'Your statement was successfully delivered.'),
  statementEdited: django.pgettext('kosmo', 'Your statement was successfully updated.'),
  statementDeleted: django.pgettext('kosmo', 'Your statement was successfully deleted.'),
  anotherStatement: django.pgettext('kosmo', 'The comment has already been moderated. Your statement could not be saved.'),
  goToDiscussion: django.pgettext('kosmo', 'Go to discussion'),
  commentBlocked: django.pgettext('kosmo', 'Comment blocked successfully.'),
  commentUnblocked: django.pgettext('kosmo', 'Comment unblocked successfully.'),
  notificationArchived: django.pgettext('kosmo', 'Notification archived successfully.'),
  notificationUnarchived: django.pgettext('kosmo', 'Notification unarchived successfully.')
}

export default class ModerationNotification extends Component {
  constructor (props) {
    super(props)

    this.state = {
      isPending: this.props.isPending,
      isBlocked: this.props.isBlocked,
      showModeratorStatementForm: false,
      moderatorStatement: undefined,
      isEditing: false,
      alert: undefined
    }
  }

  getLink (string, url) {
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
  // extent the Alert component to handle this.
  getStatementAdded (commentUrl) {
    return (
      <>
        {translated.statementAdded} <a href={commentUrl}>{translated.goToDiscussion}</a>
      </>
    )
  }

  hideAlert () {
    this.setState({ alert: undefined })
  }

  handleStatementSubmit = async (payload, commentUrl) => {
    const statementApiUrl =
      `/api/comments/${this.props.commentPk}/moderatorstatement/`

    const [getResponse] = await api.fetch({
      url: statementApiUrl,
      method: 'GET'
    })

    if (getResponse.length > 0) {
      this.setState({
        moderatorStatement: getResponse[0],
        showModeratorStatementForm: false,
        alert: {
          type: 'error',
          message: translated.anotherStatement,
          timeInMs: 3000
        }
      })
    } else {
      const [response, error] = await api.fetch({
        url: statementApiUrl,
        method: 'POST',
        body: { statement: payload }
      })
      if (error) {
        this.setState({
          alert:
            {
              type: 'error',
              message: error,
              timeInMs: 3000
            }
        })
      } else {
        this.setState({
          moderatorStatement: response,
          showModeratorStatementForm: false,
          alert: {
            type: 'success',
            message: this.getStatementAdded(commentUrl),
            timeInMs: 3000
          }
        })
      }
    }
  }

  handleStatementEdit = async (payload, pk) => {
    const statementApiUrl =
      `/api/comments/${this.props.commentPk}/moderatorstatement/${pk}/`

    const [response, error] = await api.fetch({
      url: statementApiUrl,
      method: 'PUT',
      body: { statement: payload }
    })
    if (error) {
      this.props.onChangeStatus(error)
    } else {
      this.setState({
        moderatorStatement: response,
        showModeratorStatementForm: false,
        isEditing: false,
        alert: {
          type: 'success',
          message: translated.statementEdited,
          timeInMs: 3000
        }
      })
    }
  }

  handleStatementDelete = async (pk) => {
    const statementApiUrl =
      `/api/comments/${this.props.commentPk}/moderatorstatement/${pk}/`

    await api.fetch({
      url: statementApiUrl,
      method: 'DELETE'
    })
    this.setState({
      moderatorStatement: undefined,
      alert: {
        type: 'success',
        message: translated.statementDeleted,
        timeInMs: 3000
      }
    })
  }

  async toggleIsPending () {
    const url = this.state.isPending
      ? this.props.apiUrl + 'archive/'
      : this.props.apiUrl + 'unarchive/'
    const [response, error] =
      await api.fetch({
        url: url,
        method: 'GET'
      })
    const alertMessage = response && response.has_pending_notifications
      ? translated.notificationUnarchived
      : translated.notificationArchived

    if (error) {
      this.props.onChangeStatus(error)
    } else {
      this.props.onChangeStatus(alertMessage)
      this.setState({ isPending: response.has_pending_notifications })
    }
  }

  async toggleIsBlocked () {
    const [response, error] =
      await api.fetch({
        url: this.props.apiUrl,
        method: 'PATCH',
        body: { is_blocked: !this.state.isBlocked }
      })
    const alertMessage = response && response.is_blocked
      ? translated.commentBlocked
      : translated.commentUnblocked

    if (error) {
      this.props.onChangeStatus(error)
    } else {
      this.props.onChangeStatus(alertMessage)
      this.setState({ isBlocked: response.is_blocked })
    }
  }

  toggleModerationStatementForm (e) {
    const newModerationStatementForm = !this.state.showModeratorStatementForm
    this.setState({
      showModeratorStatementForm: newModerationStatementForm
    })
  }

  translatedReportText (reportsFound) {
    const tmp = django.ngettext('kosmo', '\'s {}comment{} has been reported 1 time since it\'s creation', '\'s {}comment{} has been reported %s times since it\'s creation', reportsFound)
    return (
      django.interpolate(tmp, [reportsFound])
    )
  }

  componentDidMount () {
    const moderationStatementApiUrl =
      `/api/comments/${this.props.commentPk}/moderatorstatement/`

    api.fetch({
      url: moderationStatementApiUrl,
      method: 'GET'
    }).then(([response, error]) => {
      if (!error) {
        response.length > 0 && this.setState({
          moderatorStatement: response[0]
        })
      }
    })
  }

  render () {
    const { classifications, commentText, commentUrl, created, modified, userImage, userName, userProfileUrl, aiClassified } = this.props
    const classificationText = django.pgettext('kosmo', 'Classification: ')
    const aiText = django.pgettext('kosmo', 'AI')
    const blockText = django.pgettext('kosmo', ' Block')
    const unblockText = django.pgettext('kosmo', ' Unblock')
    const replyText = django.pgettext('kosmo', ' Add statement')
    const archiveText = django.pgettext('kosmo', ' Archive')
    const unarchiveText = django.pgettext('kosmo', ' Unarchive')
    const blockedText = django.pgettext('kosmo', 'This negative comment was blocked because it is spam')

    let userImageDiv
    if (userImage) {
      const sectionStyle = {
        backgroundImage: 'url(' + userImage + ')'
      }
      userImageDiv = <div className="user-avatar user-avatar--small user-avatar--shadow mb-1 userindicator__btn-img" style={sectionStyle} />
    }

    let commentChangeLog
    if (modified === null) {
      commentChangeLog = django.pgettext('kosmo', 'Created on ' + created)
    } else {
      commentChangeLog = django.pgettext('kosmo', 'Last edited on ' + created)
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
                <div><i className="fas fa-exclamation-circle me-1" aria-hidden="true" />
                  {userProfileUrl ? <a href={userProfileUrl}>{userName}</a> : userName}
                  {this.getLink(this.translatedReportText(1), commentUrl)}
                </div>
                <div>{commentChangeLog}</div>
              </div>
              {this.state.isPending &&
                <div className="col">
                  <div className="text-end">
                    <button
                      type="button" className="dropdown-toggle btn btn--none" aria-haspopup="true"
                      aria-expanded="false" data-bs-toggle="dropdown"
                    >
                      <i className="fas fa-ellipsis-v" aria-hidden="true" />
                    </button>
                    <ul className="dropdown-menu dropdown-menu-end">
                      <li key="1">
                        <button className="dropdown-item" type="button" onClick={() => this.toggleIsPending()}>{archiveText}</button>
                      </li>
                    </ul>
                  </div>
                </div>}

            </div>
            <div className="row">
              <div className="a4-comments__box--comment">
                <div className="col-12">
                  <span className="sr-only">{classificationText}{classifications}</span>
                  {classifications.map((classification, i) => (
                    <span className="badge a4-comments__badge a4-comments__badge--que" key={i}>{classification}</span>))}
                  {aiClassified && <span className="badge a4-comments__badge a4-comments__badge--que">{aiText}</span>}
                </div>
              </div>
            </div>
            <div className="row">
              <div className="col-12">
                <p>{commentText}</p>
              </div>
            </div>
            <div className={'mt-3 d-flex justify-content-' + (!this.state.isPending && !this.state.isBlocked ? 'end' : 'between')}>
              {this.state.isPending
                ? <>
                  <button className="btn btn--none" type="button" onClick={() => this.toggleModerationStatementForm()} disabled={this.state.moderatorStatement}>
                    <i className="fas fa-reply" aria-hidden="true" />
                    {replyText}
                  </button>
                  <button className="btn btn--none" type="button" onClick={() => this.toggleIsBlocked()}>
                    <i className="fas fa-ban" aria-hidden="true" />
                    {this.state.isBlocked ? unblockText : blockText}
                  </button>
                </> /* eslint-disable-line react/jsx-closing-tag-location */
                : <>{this.state.isBlocked && <div className="fw-bold"><i className="fas fa-exclamation-circle me-1" aria-hidden="true" />{blockedText}</div>}
                  <button className="btn btn--none" type="button" onClick={() => this.toggleIsPending()}><i className="fas fa-archive me-1" aria-hidden="true" />{unarchiveText}</button>
                </> /* eslint-disable-line react/jsx-closing-tag-location */}
            </div>
            {this.state.showModeratorStatementForm &&
              <ModerationStatementForm
                onSubmit={(payload) => this.handleStatementSubmit(payload, commentUrl)}
                onEditSubmit={(payload, pk) => this.handleStatementEdit(payload, pk)}
                initialStatement={this.state.moderatorStatement}
                editing={this.state.isEditing}
              />}
            {this.state.moderatorStatement && !this.state.showModeratorStatementForm &&
              <ModerationStatement
                statement={this.state.moderatorStatement}
                onDelete={this.handleStatementDelete}
                onEdit={() => this.setState({ showModeratorStatementForm: true, isEditing: true })}
              />}
          </div>
        </li>
        <div className="mb-3">
          <Alert {...this.state.alert} onClick={() => this.hideAlert()} />
        </div>
      </>
    )
  }
}

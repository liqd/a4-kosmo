import React, { Component } from 'react'
import django from 'django'
import api from './api'

import { ModerationStatementForm } from './ModerationStatementForm'

import { ModerationStatement } from './ModerationStatement'

export default class ModerationNotification extends Component {
  constructor (props) {
    super(props)

    this.state = {
      isPending: this.props.isPending,
      isBlocked: this.props.isBlocked,
      moderatorStatement: ''
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

  handleStatementSubmit = async (payload) => {
    const statementApiUrl =
      `/api/comments/${this.props.commentPk}/moderatorstatement/`

    const [response, error] = await api.fetch({
      url: statementApiUrl,
      method: 'POST',
      body: { statement: payload }
    })
    if (error) {
      this.props.onChangeStatus(error)
    } else {
      this.props.onChangeStatus('added')
      console.log(response)
    }
  }

  async toggleIsPending () {
    const [response, error] =
      await api.fetch({
        url: this.props.apiUrl,
        method: 'PATCH',
        body: { is_pending: !this.state.isPending }
      })

    const alertMessage = response && response.is_pending
      ? 'unarchived'
      : 'archived'

    if (error) {
      this.props.onChangeStatus(error)
    } else {
      this.props.onChangeStatus(alertMessage)
      this.setState({ isPending: response.is_pending })
    }
  }

  async toggleIsBlocked () {
    const [response, error] =
      await api.fetch({
        url: this.props.apiUrl,
        method: 'PATCH',
        body: { is_blocked: !this.state.isBlocked }
      })
    const alertMessage = response && response.comment.is_blocked
      ? 'blocked'
      : 'unblocked'

    if (error) {
      this.props.onChangeStatus(error)
    } else {
      this.props.onChangeStatus(alertMessage)
      this.setState({ isBlocked: response.comment.is_blocked })
    }
  }

  toggleModerationStatementForm (e) {
    const newModerationStatementForm = !this.state.moderationStatementForm
    this.setState({
      moderationStatementForm: newModerationStatementForm
    })
  }

  componentDidMount () {
    const moderationStatementApiUrl =
      `/api/comments/${this.props.commentPk}/moderatorstatement/`

    api.fetch({
      url: moderationStatementApiUrl,
      method: 'GET'
    }).then(([response, error]) => {
      if (error) {
        this.props.onChangeStatus(error)
      } else {
        response.length > 0 && this.setState({
          moderatorStatement: response[0].statement
        })
      }
    })
  }

  render () {
    const { classifications, commentText, commentUrl, created, userImage, userName, userProfileUrl, aiClassified } = this.props
    const offensiveTextReport = django.pgettext('kosmo', ' posted a {}comment{} that has been reported as %(classification)s')
    const offensiveTextAI = django.pgettext('kosmo', ' posted a {}comment{} that might be %(classification)s')
    /* eslint-disable */
    const offensiveTextReportInterpolated = django.interpolate(offensiveTextReport, { 'classification': classifications }, true)
    const offensiveTextAIInterpolated = django.interpolate(offensiveTextAI, { 'classification': classifications }, true)
    /* eslint-enable */
    const classificationText = django.pgettext('kosmo', 'Classification: ')
    const aiText = django.pgettext('kosmo', 'AI')
    const blockText = django.pgettext('kosmo', ' Block')
    const unblockText = django.pgettext('kosmo', ' Unblock')
    const replyText = django.pgettext('kosmo', ' Add Remark')
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

    return (
      <div>
        <div className="row">
          <div className="col-sm-2 col-md-1">
            {userImageDiv}
          </div>
          <div className="col-sm-7 col-md-8">
            <div><i className="fas fa-exclamation-circle me-1" aria-hidden="true" />
              {userProfileUrl ? <a href={userProfileUrl}>{userName}</a> : userName}
              {aiClassified ? this.getLink(offensiveTextAIInterpolated, commentUrl) : this.getLink(offensiveTextReportInterpolated, commentUrl)}
            </div>
            <div>{created}</div>
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
        {this.state.moderationStatementForm &&
          <ModerationStatementForm
            onStatementSubmit={this.handleStatementSubmit}
            initialStatement={this.state.moderatorStatement}
          />}
        {this.state.hasStatement &&
          <ModerationStatement
            statementText="test"
            statementEdited="Last edit was on 23.04.2022"
          />}
      </div>
    )
  }
}

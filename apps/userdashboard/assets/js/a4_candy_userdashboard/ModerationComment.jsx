import React, { Component } from 'react'
import django from 'django'

export default class ModerationComment extends Component {
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

  render () {
    const { classification, commentText, commentUrl, created, userImage, userName, userProfileUrl, aiClassified } = this.props
    const offensiveTextReport = django.pgettext('kosmo', ' posted a {}comment{} that has been reported as %(classification)s')
    const offensiveTextAI = django.pgettext('kosmo', ' posted a {}comment{} that might be %(classification)s')
    /* eslint-disable */
    const offensiveTextReportInterpolated = django.interpolate(offensiveTextReport, { 'classification': classification }, true)
    const offensiveTextAIInterpolated = django.interpolate(offensiveTextAI, { 'classification': classification }, true)
    /* eslint-enable */
    const classificationText = django.pgettext('kosmo', 'Classification: ')
    const aiText = django.pgettext('kosmo', 'AI')
    const blockText = django.pgettext('kosmo', ' Block')
    const unblockText = django.pgettext('kosmo', ' Unblock')
    const replyText = django.pgettext('kosmo', ' Add Remark')
    const archiveText = django.pgettext('kosmo', ' Archive')
    const unarchiveText = django.pgettext('kosmo', ' Unarchive')

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
          <div className="col-2 col-md-1">
            {userImageDiv}
          </div>
          <div className="col-7 col-md-8">
            <div><i className="fas fa-exclamation-circle me-1" aria-hidden="true" />
              {userProfileUrl ? <a href={userProfileUrl}>{userName}</a> : userName}
              {aiClassified ? this.getLink(offensiveTextAIInterpolated, commentUrl) : this.getLink(offensiveTextReportInterpolated, commentUrl)}
            </div>
            <div>{created}</div>
          </div>
          <div className="col">
            <div className="text-end">
              <button
                type="button" className="dropdown-toggle btn btn--link" aria-haspopup="true"
                aria-expanded="false" data-bs-toggle="dropdown"
              >
                <i className="fas fa-ellipsis-v" aria-hidden="true" />
              </button>
              <ul className="dropdown-menu dropdown-menu-end">
                <li key="1">
                  <button className="dropdown-item" type="button">{archiveText}</button>
                </li>
                <li key="2">
                  <button className="dropdown-item" type="button">{unarchiveText}</button>
                </li>
              </ul>
            </div>
          </div>

        </div>
        <div className="row">
          <div className="a4-comments__box--comment">
            <div className="col-12">
              <span className="sr-only">{classificationText}{classification}</span>
              <span className="badge a4-comments__badge a4-comments__badge--que">{classification}</span>
              {aiClassified && <span className="badge a4-comments__badge a4-comments__badge--que">{aiText}</span>}
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-12">
            <p>{commentText}</p>
          </div>
        </div>
        <div className="text-muted mt-3 d-flex justify-content-between">
          <button className="btn btn--none" type="button" disabled><i className="fas fa-reply" aria-hidden="true" />{replyText}</button>
          <button className="btn btn--none" type="button" disabled><i className="fas fa-ban" aria-hidden="true" />{blockText}</button>
          <button className="btn btn--none" type="button" disabled><i className="fas fa-ban" aria-hidden="true" />{unblockText}</button>
        </div>
      </div>
    )
  }
}

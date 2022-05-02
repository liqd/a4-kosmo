import React from 'react'
import django from 'django'

export const ModerationNotificationActionsBar = (props) => {
  const translated = {
    blockText: django.pgettext('kosmo', ' Block'),
    unblockText: django.pgettext('kosmo', ' Unblock'),
    replyText: django.pgettext('kosmo', ' Add statement'),
    unarchiveText: django.pgettext('kosmo', ' Unarchive'),
    blockedText: django.pgettext('kosmo', 'This negative comment was blocked because it is spam'),
    highlightText: django.pgettext('kosmo', 'Highlight'),
    unhighlightText: django.pgettext('kosmo', 'Unhighlight')
  }

  const {
    isPending,
    isDisabled,
    isBlocked,
    isHighlighted,
    onToggleForm,
    onToggleBlock,
    onToggleHighlight,
    onTogglePending
  } = props

  return isPending
    ? (
      <div className="my-3 d-flex justify-content-between">
        <button
          id="moderation-notification-actions-bar-button-reply"
          className="btn btn--none ps-0"
          type="button"
          onClick={onToggleForm}
          disabled={isDisabled}
        >
          <i className="fas fa-reply" aria-hidden="true" />
          {translated.replyText}
        </button>
        <div>
          <button
            id="moderation-notification-actions-bar-button-highlight"
            className="btn btn--none"
            type="button"
            onClick={onToggleHighlight}
            disabled={isBlocked}
          >
            <i className="icon-highlight" aria-hidden="true" />
            {isHighlighted ? translated.unhighlightText : translated.highlightText}
          </button>
          <button
            id="moderation-notification-actions-bar-button-block"
            className="btn btn--none"
            type="button"
            onClick={onToggleBlock}
            disabled={isHighlighted}
          >
            <i className="fas fa-ban" aria-hidden="true" />
            {isBlocked ? translated.unblockText : translated.blockText}
          </button>
        </div>
      </div>
      )
    : (
      <div className={'my-3 d-flex justify-content-' + (!isBlocked ? 'end' : 'between')}>
        {isBlocked &&
          <div className="fw-bold">
            <i className="fas fa-exclamation-circle me-1" aria-hidden="true" />
            {translated.blockedText}
          </div>}
        <button
          id="moderation-notification-actions-bar-button-pending"
          className="btn btn--none"
          type="button"
          onClick={onTogglePending}
        >
          <i className="fas fa-archive me-1" aria-hidden="true" />
          {translated.unarchiveText}
        </button>
      </div>
      )
}

import React from 'react'
import django from 'django'
import { HoverButton } from '../../../../../apps/contrib/assets/HoverButton'

export const ModerationNotificationActionsBar = (props) => {
  const translated = {
    blockText: django.pgettext('kosmo', 'Block'),
    unblockText: django.pgettext('kosmo', 'Unblock'),
    isBlockedText: django.pgettext('kosmo', 'Blocked'),
    replyText: django.pgettext('kosmo', 'Add statement'),
    blockedText: django.pgettext('kosmo', 'This negative comment was blocked because it is spam'),
    highlightText: django.pgettext('kosmo', 'Highlight'),
    unhighlightText: django.pgettext('kosmo', 'Unhighlight'),
    isHighlightedText: django.pgettext('kosmo', 'Highlighted'),
    unarchiveText: django.pgettext('kosmo', 'Unarchive'),
    archivedText: django.pgettext('kosmo', 'Archived')
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

  const highlightButtonHoverText = isHighlighted ? translated.unhighlightText : translated.highlightText
  const highlightButtonText = isHighlighted ? translated.isHighlightedText : translated.highlightText
  const blockButtonHoverText = isBlocked ? translated.unblockText : translated.blockText
  const blockButtonText = isBlocked ? translated.isBlockedText : translated.blockText

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
          <span className="ms-2">
            {translated.replyText}
          </span>
        </button>
        <div>
          <HoverButton
            id="moderation-notification-actions-bar-button-highlight"
            className="btn btn--none"
            onClick={onToggleHighlight}
            disabled={isBlocked}
            icon={<i className="icon-highlight" aria-hidden="true" />}
            text={highlightButtonText}
            hoverText={highlightButtonHoverText}
          />
          <HoverButton
            id="moderation-notification-actions-bar-button-block"
            className="btn btn--none"
            onClick={onToggleBlock}
            disabled={isHighlighted}
            icon={<i className="fas fa-ban" aria-hidden="true" />}
            text={blockButtonText}
            hoverText={blockButtonHoverText}
          />
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
        <HoverButton
          id="moderation-notification-actions-bar-button-pending"
          className="btn btn--none"
          onClick={onTogglePending}
          icon={<i className="fas fa-archive me-1" aria-hidden="true" />}
          text={translated.archivedText}
          hoverText={translated.unarchiveText}
        />
      </div>
      )
}

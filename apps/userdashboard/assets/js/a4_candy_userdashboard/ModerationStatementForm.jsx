import React, { useState } from 'react'
import django from 'django'

import Alert from '../../../../contrib/assets/Alert'

export const ModerationStatementForm = (props) => {
  const [statement, setStatement] =
    useState((props.editing && props.initialStatement.statement) || '')

  const translated = {
    placeholder: django.pgettext('kosmo', 'Write statement'),
    charCount: django.pgettext('kosmo', ' characters'),
    alertError: django.gettext('kosmo', 'Your statement could not be saved, please check if there is already one saved.'),
    submitLabel: django.pgettext('kosmo', 'submit statement'),
    submitEditLabel: django.pgettext('kosmo', 'update statement')
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (props.editing) {
      props.onEditSubmit(statement, props.initialStatement.pk)
    } else {
      props.onSubmit(statement)
    }
  }

  const removeAlert = (e) => {
    this.setState({
      alert: null
    })
  }

  return (
    <form className="general-form" onSubmit={handleSubmit}>
      <Alert onClick={() => removeAlert()}>{translated.alertError}</Alert>
      <textarea
        className="a4-comments__textarea--small form-group"
        placeholder={translated.placeholder}
        onChange={(e) => setStatement(e.target.value)}
        value={statement}
      />
      <div className="row">
        <label htmlFor="id-comment-form" className="col-6 a4-comments__char-count">
          {statement.length}/500{translated.charCount}
        </label>
        <div className="a4-comments__submit d-flex col-6">
          <button
            type="submit"
            className="btn a4-comments__submit-input ms-auto"
          >
            {props.editing ? translated.submitEditLabel : translated.submitLabel}
          </button>
        </div>
      </div>
    </form>
  )
}

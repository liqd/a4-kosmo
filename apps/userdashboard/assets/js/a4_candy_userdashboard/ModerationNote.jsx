import React, { Component } from 'react'
import django from 'django'

export default class ModerationNote extends Component {
  constructor (props) {
    super(props)

    this.state = {
      note: '',
      noteCharCount: 0
    }
  }

  handleTextChange (e) {
    this.setState({
      note: e.target.value,
      noteCharCount: e.target.value.length
    })
  }

  handleSubmit (e) {
    e.preventDefault()
    const note = this.state.note.trim()
    const data = {
      note: note,
      urlReplaces: {
        objectPk: this.props.subjectId,
        contentTypeId: this.props.subjectType
      }
    }
    this.props.onNoteSubmit(data, this.props.parentIndex)
  }

  render () {
    return (
      <div>
        <form id="id-note-form" className="general-form" onSubmit={this.handleSubmit.bind(this)}>
          <textarea
            id="textarea-top"
            className="a4-comments__textarea--small form-group"
            placeholder={django.gettext('Write note')}
            onChange={this.handleTextChange.bind(this)}
            value={this.state.note}
          />
          <div className="row">
            <label htmlFor="id-comment-form" className="col-6 a4-comments__char-count">{this.state.noteCharCount}/500{django.gettext(' characters')}</label>
            <div className="a4-comments__submit d-flex col-6">
              <button type="submit" value={django.gettext('post')} className="btn a4-comments__submit-input ms-auto">{django.gettext('add note')}</button>
            </div>
          </div>
        </form>
      </div>
    )
  }
}

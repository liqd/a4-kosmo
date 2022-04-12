import React from 'react'
import django from 'django'

export const ModerationStatement = (props) => {
  const { statement, last_edit: lastEdit, pk } = props.statement
  const translated = {
    delete: django.pgettext('kosmo', 'delete'),
    edit: django.pgettext('kosmo', 'edit'),
    statementTitle: django.pgettext('kosmo', 'Moderator\'s statement'),
    editWasOn: django.pgettext('kosmo', 'Last edit was on')
  }

  const formatDate = (date) => {
    const editDate = new Date(date)
    return editDate.toLocaleDateString()
  }

  return (
    <div className="userdashboard-mod-statement">
      <div className="row">
        <div className="col-7 col-md-8 userdashboard-mod-statement__header">
          <div>{translated.statementTitle}</div>
        </div>
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
                <button
                  className="dropdown-item"
                  type="button"
                  onClick={() => props.onDelete(pk)}
                >
                  {translated.delete}
                </button>
              </li>
              <li key="2">
                <button
                  className="dropdown-item"
                  type="button"
                  onClick={props.onEdit}
                >
                  {translated.edit}
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col">
          <p>
            {`${translated.editWasOn} ${formatDate(lastEdit)}`}
          </p>
        </div>
      </div>
      <div className="row">
        <div className="col-12">
          <p>{statement}</p>
        </div>
      </div>
    </div>
  )
}

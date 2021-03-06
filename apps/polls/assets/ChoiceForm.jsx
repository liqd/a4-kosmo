const React = require('react')
const django = require('django')
const ErrorList = require('../../contrib/assets/ErrorList')

const ChoiceForm = (props) => {
  return (
    <div className="form-group form-group--narrow form-inline">
      <div className="input-group">
        <label htmlFor={'id_choices-' + props.id + '-name'}>
          <span className="sr-only">{props.label}</span>
          <input
            id={'id_choices-' + props.id + '-name'}
            name={'choices-' + props.id + '-name'}
            type="text"
            className="form-control"
            value={props.choice.label}
            onChange={(e) => { props.onLabelChange(e.target.value) }}
          />
        </label>
        <div className="input-group-append">
          <button
            className="btn btn--light btn--append"
            onClick={props.onDelete}
            title={django.gettext('remove')}
            type="button"
          >
            <i
              className="fa fa-times"
              aria-label={django.gettext('remove')}
            />
          </button>
        </div>
      </div>
      <ErrorList errors={props.errors} field="label" />
    </div>
  )
}

module.exports = ChoiceForm

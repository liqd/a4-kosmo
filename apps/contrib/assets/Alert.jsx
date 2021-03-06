const React = require('react')
const django = require('django')

const Alert = ({ type, message, onClick }) => {
  if (type) {
    return (
      <div className={`alert alert--${type}`} role="alert">
        <div className="container">
          {message}
          <button className="alert__close" title={django.gettext('Close')} onClick={onClick}>
            <i className="fa fa-times" aria-label={django.gettext('Close')} />
          </button>
        </div>
      </div>
    )
  }

  return null
}

module.exports = Alert

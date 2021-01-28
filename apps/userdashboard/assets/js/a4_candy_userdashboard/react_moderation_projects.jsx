var React = require('react')
var ReactDOM = require('react-dom')

class ModerationProjects extends React.Component {
  render () {
    return (
      <div className="row mb-2">
        <div className="col-12">
          <h2>Projects</h2>
          <span>project</span>
        </div>
      </div>
    )
  }
}

module.exports.renderModerationProjects = function (el) {
  ReactDOM.render(
    <ModerationProjects />,
    el
  )
}

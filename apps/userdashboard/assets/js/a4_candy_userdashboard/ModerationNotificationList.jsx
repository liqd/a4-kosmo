import React, { Component } from 'react'
import django from 'django'

import ModerationNotification from './ModerationNotification'
import { FilterBar } from './FilterBar'
import { alert as Alert } from 'adhocracy4'

export default class ModerationNotificationList extends Component {
  constructor (props) {
    super(props)

    this.state = {
      moderationComments: [],
      filterItem: { filter: '', name: '' },
      isLoaded: false,
      alert: undefined
    }
  }

  componentDidMount () {
    this.loadData(this.state.filterItem.filter)
    this.timer = setInterval(() => this.loadData(this.state.filterItem.filter), 3000)
  }

  filterChangeHandle (filterItem) {
    this.setState({
      filterItem: filterItem,
      isLoaded: false
    })
    this.loadData(filterItem.filter)
  }

  async loadData (filter = undefined) {
    const url = filter
      ? this.props.moderationCommentsApiUrl + filter
      : this.props.moderationCommentsApiUrl
    const data = await fetch(url)
    const moderationComments = await data.json()

    this.setState(
      { moderationComments: moderationComments },
      () => this.setState({ isLoaded: true })
    )
  }

  handleAlert = (message, type = 'Notification') => {
    const alertMessage = typeof message === 'string'
      ? this.getSuccessAlert(message, type)
      : this.getErrorAlert(message)

    this.setState({
      alert: {
        ...alertMessage,
        onClick: () => this.hideAlert()
      }
    })
  }

  getSuccessAlert = (message) => {
    return {
      type: 'success',
      message: message
    }
  }

  getErrorAlert = (error) => {
    return {
      type: 'error',
      message: error.message
    }
  }

  hideAlert = () => {
    this.setState({ alert: undefined })
  }

  componentWillUnmount () {
    clearInterval(this.timer)
    this.timer = null
  }

  render () {
    const { isLoaded } = this.state
    const { projectTitle, organisation, projectUrl } = this.props
    const byText = django.pgettext('kosmo', 'By ')
    const aiText = django.pgettext('kosmo', 'AI')

    return (
      <div className="row mb-2">
        <div className="col-12">
          <Alert {...this.state.alert} />
          <h1 className="m-0">
            <a href={projectUrl}>{projectTitle}</a>
          </h1>
          <span className="text-muted">
            {byText}
            {organisation}
          </span>
          <div className="mt-3">
            <FilterBar
              onFilterChange={(filterItem) => this.filterChangeHandle(filterItem)}
              selectedFilter={this.state.filterItem.filter}
            />
          </div>
          {!isLoaded
            ? (
              <div className="d-flex justify-content-center">
                <i className="fa fa-spinner fa-pulse" aria-hidden="true" />
              </div>
              )
            : (
              <ul className="ps-0 mt-5">
                {this.state.moderationComments.map((item, i) => (
                  <ModerationNotification
                    key={i}
                    apiUrl={this.props.moderationCommentsApiUrl + item.pk + '/'}
                    classifications={Object.entries(item.category_counts).map(([k, v]) => `${k}: ${v}`)}
                    commentPk={item.pk}
                    commentText={item.comment}
                    commentUrl={item.comment_url}
                    created={item.last_edit}
                    isModified={item.is_modified}
                    isBlocked={item.is_blocked}
                    isPending={item.has_pending_notifications}
                    userImage={item.user_image}
                    userName={item.user_name}
                    userProfileUrl={item.user_profile_url}
                    aiClassified={item.category_counts[aiText] > 0}
                    onChangeStatus={(message, type) => this.handleAlert(message, type)}
                    activeNotifications={item.num_active_notifications}
                    moderatorStatement={item.moderator_statement}
                    statementApiUrl={item.statement_api_url}
                    loadData={() => this.loadData(this.state.filterItem.filter)}
                  />
                ))}
              </ul>
              )}
        </div>
      </div>
    )
  }
}

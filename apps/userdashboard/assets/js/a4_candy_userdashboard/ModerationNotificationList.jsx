import React, { Component } from 'react'
import django from 'django'

import ModerationNotification from './ModerationNotification'
import { FilterBar } from './FilterBar'
import Alert from '../../../../contrib/assets/Alert'

export default class ModerationNotificationList extends Component {
  constructor (props) {
    super(props)

    this.state = {
      notifications: [],
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
    const aiUrl = filter
      ? this.props.aiclassificationApiUrl + filter
      : this.props.aiclassificationApiUrl
    const aiFetch = await fetch(aiUrl)
    const aiNotifications = await aiFetch.json()
    aiNotifications && aiNotifications.forEach(nf => { nf.meta = { aiClassified: true } })

    const userUrl = filter
      ? this.props.userclassificationApiUrl + filter
      : this.props.userclassificationApiUrl
    const userFetch = await fetch(userUrl)
    const userNotifications = await userFetch.json()

    this.setState(
      { notifications: [...aiNotifications, ...userNotifications] },
      () => this.setState({ isLoaded: true })
    )
  }

  handleAlert = (message) => {
    const alertMessage = typeof message === 'string'
      ? this.getSuccessAlert(message)
      : this.getErrorAlert(message)

    this.setState({
      alert: {
        ...alertMessage,
        onClick: () => this.hideAlert()
      }
    })
  }

  getSuccessAlert = (message) => {
    const alertMessage = `Notification ${django.gettext(message)} successfully.`
    return {
      type: 'success',
      message: django.gettext(alertMessage)
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

  filterNotifications = () => {
    return this.state.notifications.filter(notification => {
      return this.state.filterItem.filter === ''
        ? true
        : this.state.filterItem.name === 'Pending'
          ? notification.is_pending
          : !notification.is_pending
    })
  }

  componentWillUnmount () {
    clearInterval(this.timer)
    this.timer = null
  }

  render () {
    const { isLoaded } = this.state
    const { projectTitle, organisation, projectUrl } = this.props
    const byText = django.pgettext('kosmo', 'By ')
    const filteredNotifications = this.filterNotifications()

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
                {filteredNotifications.map((item, i) => (
                  <li className="list-item" key={i}>
                    <ModerationNotification
                      apiUrl={item.api_url}
                      classifications={item.classifications}
                      commentPk={item.comment.pk}
                      commentText={item.comment_text}
                      commentUrl={item.comment.comment_url}
                      created={item.created}
                      isBlocked={item.comment.is_blocked}
                      isPending={item.is_pending}
                      userImage={item.comment.user_image}
                      userName={item.comment.user_name}
                      userProfileUrl={item.comment.user_profile_url}
                      aiClassified={item?.meta?.aiClassified}
                      onChangeStatus={(isPending) => this.handleAlert(isPending)}
                    />
                  </li>
                ))}
              </ul>
              )}
        </div>
      </div>
    )
  }
}

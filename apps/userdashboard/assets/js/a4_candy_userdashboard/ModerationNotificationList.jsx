import React, { Component } from 'react'
import django from 'django'

import ModerationNotification from './ModerationNotification'
import { FilterBar } from './FilterBar'

export default class ModerationNotificationList extends Component {
  constructor (props) {
    super(props)

    this.state = {
      notifications: [],
      filter: '',
      isLoaded: false
    }
  }

  componentDidMount () {
    this.loadData(this.state.filter)
    this.timer = setInterval(() => this.loadData(this.state.filter), 3000)
  }

  filterChangeHandle (filter) {
    this.setState({ filter: filter })
    this.setState({ isLoaded: false })
    this.loadData(filter)
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

    this.setState({ notifications: [...aiNotifications, ...userNotifications], isLoaded: true })
  }

  componentWillUnmount () {
    clearInterval(this.timer)
    this.timer = null
  }

  render () {
    const { isLoaded, notifications } = this.state
    const { projectTitle, organisation, projectUrl } = this.props
    const byText = django.pgettext('kosmo', 'By ')
    const loadingText = django.pgettext('kosmo', 'Loading...')

    return (
      <div className="row mb-2">
        <div className="col-12">
          <h1 className="m-0">
            <a href={projectUrl}>{projectTitle}</a>
          </h1>
          <span className="text-muted">
            {byText}
            {organisation}
          </span>
          <div className="mt-3">
            <FilterBar
              onFilterChange={(filter) => this.filterChangeHandle(filter)}
              selectedFilter={this.state.filter}
            />
          </div>
          {!isLoaded
            ? (
              <div className="d-flex justify-content-center">
                <div className="spinner-border" role="status">
                  <span className="sr-only">{loadingText}</span>
                </div>
              </div>
              )
            : (
              <ul className="ps-0 mt-5">
                {notifications.map((item, i) => (
                  <li className="list-item" key={i}>
                    <ModerationNotification
                      apiUrl={item.api_url}
                      classification={item.classification}
                      commentText={item.comment_text}
                      commentUrl={item.comment.comment_url}
                      created={item.created}
                      isPending={item.is_pending}
                      userImage={item.comment.user_image}
                      userName={item.comment.user_name}
                      userProfileUrl={item.comment.user_profile_url}
                      aiClassified={item?.meta?.aiClassified}
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

import React, { Component } from 'react'
import django from 'django'

import { ModerationNotification } from './ModerationNotification'
import { Filter } from './Filter'
import { alert as Alert } from 'adhocracy4'

const pendingFilterItems = [
  { label: django.pgettext('kosmo', 'Pending'), value: 'true' },
  { label: django.pgettext('kosmo', 'Archived'), value: 'false' },
  { label: django.pgettext('kosmo', 'View all'), value: '' }
]

const classificationFilterItems = [
  { label: django.pgettext('kosmo', 'Offensive'), value: 'OFFENSIVE' },
  { label: django.pgettext('kosmo', 'Engaging'), value: 'ENGAGING' },
  { label: django.pgettext('kosmo', 'Fact claiming'), value: 'FACTCLAIMING' },
  { label: django.pgettext('kosmo', 'All categories'), value: '' }
]

const orderingFilterItems = [
  { label: django.pgettext('kosmo', 'Most recent reported'), value: 'new' },
  { label: django.pgettext('kosmo', 'Oldest reported'), value: 'old' },
  { label: django.pgettext('kosmo', 'Most reported'), value: 'most' }
]

export default class ModerationNotificationList extends Component {
  constructor (props) {
    super(props)

    this.state = {
      moderationComments: [],
      selectedFilters: { pending: '', classification: '', ordering: 'new' },
      isLoaded: false,
      alert: undefined
    }
  }

  componentDidMount () {
    this.loadData()
    setInterval(
      () => !this.timer && this.loadData(),
      3000
    )
  }

  pendingFilterChangeHandle (value) {
    this.setState({
      selectedFilters: {
        ...this.state.selectedFilters,
        pending: value
      },
      isLoaded: false
    },
    () => this.loadData()
    )
  }

  classificationFilterChangeHandle (value) {
    this.setState({
      selectedFilters: {
        ...this.state.selectedFilters,
        classification: value
      },
      isLoaded: false
    },
    () => this.loadData()
    )
  }

  orderingFilterChangeHandle (value) {
    this.setState({
      selectedFilters: {
        ...this.state.selectedFilters,
        ordering: value
      },
      isLoaded: false
    },
    () => this.loadData()
    )
  }

  getUrlParams () {
    return `?has_pending_notifications=${this.state.selectedFilters.pending}&classification=${this.state.selectedFilters.classification}&ordering=${this.state.selectedFilters.ordering}`
  }

  async loadData () {
    this.timer = true
    const url = this.props.moderationCommentsApiUrl + this.getUrlParams()
    const data = await fetch(url)
    const moderationComments = await data.json()
    this.timer = false
    this.setState({
      moderationComments: moderationComments,
      isLoaded: true
    })
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
          <div
            className="filter-bar justify-content-end"
            aria-label={django.pgettext('kosmo', 'Filter')}
          >
            <div className="mt-3">
              <Filter
                filterItems={classificationFilterItems}
                onFilterChange={(value) => this.classificationFilterChangeHandle(value)}
                selectedFilter={this.state.selectedFilters.classification}
                filterText={django.pgettext('kosmo', 'Filter')}
              />
            </div>
            <div className="mt-3 px-3">
              <Filter
                filterItems={pendingFilterItems}
                onFilterChange={(value) => this.pendingFilterChangeHandle(value)}
                selectedFilter={this.state.selectedFilters.pending}
                filterText={django.pgettext('kosmo', 'Filter')}
              />
            </div>
            <div className="mt-3">
              <Filter
                filterItems={orderingFilterItems}
                onFilterChange={(value) => this.orderingFilterChangeHandle(value)}
                selectedFilter={this.state.selectedFilters.ordering}
                filterText={django.pgettext('kosmo', 'Sorting')}
              />
            </div>
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
                    notification={item}
                    apiUrl={this.props.moderationCommentsApiUrl + item.pk + '/'}
                    onChangeStatus={(message, type) => this.handleAlert(message, type)}
                    loadData={() => this.loadData()}
                  />
                ))}
              </ul>
              )}
        </div>
      </div>
    )
  }
}

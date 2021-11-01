import React from 'react'
import django from 'django'

export const FilterBar = () => {
  return (
    <div className="filter-bar justify-content-end" role="group" aria-label={django.gettext('Filter')}>
      <div className="me-sm-1 mt-2 mt-sm-0">
        <div className="dropdown dropdown-menu-end">
          <button
            type="button"
            className="dropdown-toggle btn btn--light btn--select show"
            data-bs-toggle="dropdown"
          >
            {django.gettext('Filter')}
            <i className="fa fa-caret-down" aria-hidden="true" />
          </button>
          <ul className="dropdown-menu">
            <li>
              <a className="selected" href="/#">all</a>
            </li>
            <li>
              <a href="/#">pending</a>
            </li>
            <li>
              <a href="/#">archived</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
